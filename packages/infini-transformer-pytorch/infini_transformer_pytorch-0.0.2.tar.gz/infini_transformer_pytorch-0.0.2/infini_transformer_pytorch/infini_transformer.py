from typing import Tuple, List, Optional

import torch
from torch import nn, Tensor
import torch.nn.functional as F
from torch.nn import Module, ModuleList

from einops import einsum, rearrange, repeat, reduce
from einops.layers.torch import Rearrange

from rotary_embedding_torch import RotaryEmbedding

# constants

Memories = Tuple[Tensor, Tensor]

# helpers

def exists(v):
    return v

def default(v, d):
    return v if exists(v) else d

# classes

class RMSNorm(Module):
    def __init__(self, dim):
        super().__init__()
        self.scale = dim ** 0.5
        self.gamma = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        return F.normalize(x, dim = -1) * self.scale * self.gamma

class FeedForward(Module):
    def __init__(self, dim, mult = 4):
        super().__init__()
        dim_inner = int(mult * dim * 2 / 3)

        self.norm = RMSNorm(dim)
        self.proj_in = nn.Linear(dim, dim_inner * 2)
        self.proj_out = nn.Linear(dim_inner, dim)

    def forward(self, x):
        x = self.norm(x)
        x, gates = self.proj_in(x).chunk(2, dim = -1)
        x = F.gelu(gates) * x
        return self.proj_out(x)

# attention

class CausalAttention(Module):
    def __init__(
        self,
        dim,
        *,
        dim_head = 128,
        heads = 8,
        head_gate_init_value = 10.,
        use_mem_delta_rule = False
    ):
        super().__init__()
        dim_inner = dim_head * heads
        self.scale = dim_head ** -0.5
        self.norm = RMSNorm(dim)

        self.rotary_emb = RotaryEmbedding(dim_head)

        self.to_qkv = nn.Linear(dim, dim_inner * 3, bias = False)
        self.to_out = nn.Linear(dim_inner, dim, bias = False)

        self.split_heads = Rearrange('b n (qkv h d) -> qkv b h n d', qkv = 3, h = heads)
        self.merge_heads = Rearrange('b h n d -> b n (h d)')

        self.head_gates = nn.Parameter(torch.ones(heads) * head_gate_init_value)

        self.use_mem_delta_rule = use_mem_delta_rule

    def forward(
        self,
        x,
        past_memories: Optional[Memories] = None,
        eps = 1e-10
    ) -> Tuple[Tensor, Memories]:
        """
        ein notation:

        b - batch
        h - heads
        n - sequence
        i - source sequence (q)
        j - target sequence (kv)
        d - feature dimension
        dk - feature dimension keys (and queries)
        dv - feature dimension of values
        """

        x = self.norm(x)

        x = self.to_qkv(x)
        q, k, v = self.split_heads(x)

        q = q * self.scale

        # rotary

        q = self.rotary_emb.rotate_queries_or_keys(q)
        k = self.rotary_emb.rotate_queries_or_keys(k)

        # similarity

        sim = einsum(q, k, '... i d, ... j d -> ... i j')

        # causal mask

        i, j = sim.shape[-2:]
        causal_mask = torch.ones((i, j), device = sim.device, dtype = torch.bool).triu(j - i + 1)
        sim = sim.masked_fill(causal_mask, -torch.finfo(sim.dtype).max)

        # attend

        attn = sim.softmax(dim = -1)

        # aggregate values

        out = einsum(attn, v, '... i j, ... j d -> ... i d')

        # the main contribution of the paper
        # Katharopoulos linear attention to kv memory of shape (batch, heads, dim keys, dim values)
        # it makes sense the author would try this, as he is ex-shmidhuber lab (linear transformers are fast weights paper)

        q = F.elu(q) + 1
        k = F.elu(k) + 1

        # retrieve from past memories if present

        if exists(past_memories):
            past_memories_kv, past_memories_norm = past_memories

            mem_out_unnormed = einsum(q, past_memories_kv, 'b h n dk, b h dk dv -> b h n dv')
            mem_norm = einsum(q, past_memories_norm, 'b h n d, b h d -> b h n')

            mem_norm = rearrange(mem_norm, '... -> ... 1')
            mem_out = mem_out_unnormed / mem_norm.clamp(min = eps) # eq (3)

            # now combine the present output of queries with the outputs querying the past compressed key/value memories
            # in paper, they use a sigmoid gating scheme with learned gate per head

            gates = rearrange(self.head_gates, 'h -> h 1 1')
            gates = gates.sigmoid()

            out = out * gates + mem_out * (1. - gates)  # eq (6)

        # create the next memories

        if exists(past_memories) and self.use_mem_delta_rule:
            # eq (5) - the delta rule
            v_unnormed = einsum(k, past_memories_kv, 'b h n dk, b h dk dv -> b h n dv')
            v_norm = einsum(k, past_memories_norm, 'b h n d, b h d -> b h n')

            v_norm = rearrange(v_norm, '... -> ... 1')
            delta_v = v_unnormed / v_norm.clamp(min = eps)

            v = v - delta_v

        new_memories_kv = einsum(k, v, '... n dk, ... n dv -> ... dk dv')
        new_memories_norm = reduce(k, 'b h n d -> b h d', 'sum')

        if exists(past_memories):
            new_memories_kv = new_memories_kv + past_memories_kv          # eq (4)
            new_memories_norm = new_memories_norm + past_memories_norm    # eq (4)

        new_memories = (new_memories_kv, new_memories_norm)

        # merge heads and combine

        out = self.merge_heads(out)
        out = self.to_out(out)

        return out, new_memories

# main class

class InfiniTransformer(Module):
    def __init__(
        self,
        *,
        num_tokens,
        dim,
        depth,
        dim_head = 128,
        heads = 8,
        ff_mult = 4,
        use_mem_delta_rule = False  # in the paper, the delta rule didn't seem to do that much, but will include for completeness
    ):
        super().__init__()

        self.token_emb = nn.Embedding(num_tokens, dim)

        self.layers = ModuleList([])

        for _ in range(depth):

            attn = CausalAttention(
                dim = dim,
                dim_head = dim_head,
                heads = heads,
                use_mem_delta_rule = use_mem_delta_rule
            )

            ff = FeedForward(
                dim = dim,
                mult = ff_mult
            )

            self.layers.append(ModuleList([attn, ff]))

        self.norm = RMSNorm(dim)
        self.to_logits = nn.Linear(dim, num_tokens)

    def forward(
        self,
        x,
        past_memories: Optional[List[Memories]] = None,
        return_memories = False,
        detach_memories = False
    ):
        x = self.token_emb(x)

        new_memories = []
        past_memories_iter = iter(default(past_memories, []))

        for attn, ff in self.layers:
            past_memories = next(past_memories_iter, None)
            attn_out, layer_new_memories = attn(x, past_memories = past_memories)

            x = attn_out + x
            x = ff(x) + x

            new_memories.append(layer_new_memories)

        embed = self.norm(x)

        logits = self.to_logits(embed)

        if not return_memories:
            return logits

        if detach_memories:
            for (mem_kv, mem_norm) in new_memories:
                mem_kv.detach_()
                mem_norm.detach_()

        return logits, new_memories
