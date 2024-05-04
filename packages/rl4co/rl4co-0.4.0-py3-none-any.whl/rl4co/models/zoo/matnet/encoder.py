import math

from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from einops import rearrange

from rl4co.models.nn.env_embeddings import env_init_embedding
from rl4co.models.nn.ops import Normalization


class MatNetCrossMHA(nn.Module):
    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        bias: bool = False,
        mixer_hidden_dim: int = 16,
        mix1_init: float = (1 / 2) ** (1 / 2),
        mix2_init: float = (1 / 16) ** (1 / 2),
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        assert self.embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"
        self.head_dim = self.embed_dim // num_heads

        self.Wq = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.Wkv = nn.Linear(embed_dim, 2 * embed_dim, bias=bias)

        # Score mixer
        # Taken from the official MatNet implementation
        # https://github.com/yd-kwon/MatNet/blob/main/ATSP/ATSP_MatNet/ATSPModel_LIB.py#L72
        mix_W1 = torch.torch.distributions.Uniform(low=-mix1_init, high=mix1_init).sample(
            (num_heads, 2, mixer_hidden_dim)
        )
        mix_b1 = torch.torch.distributions.Uniform(low=-mix1_init, high=mix1_init).sample(
            (num_heads, mixer_hidden_dim)
        )
        self.mix_W1 = nn.Parameter(mix_W1)
        self.mix_b1 = nn.Parameter(mix_b1)

        mix_W2 = torch.torch.distributions.Uniform(low=-mix2_init, high=mix2_init).sample(
            (num_heads, mixer_hidden_dim, 1)
        )
        mix_b2 = torch.torch.distributions.Uniform(low=-mix2_init, high=mix2_init).sample(
            (num_heads, 1)
        )
        self.mix_W2 = nn.Parameter(mix_W2)
        self.mix_b2 = nn.Parameter(mix_b2)

        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)

    def forward(self, q_input, kv_input, dmat):
        """

        Args:
            q_input (Tensor): [b, m, d]
            kv_input (Tensor): [b, n, d]
            dmat (Tensor): [b, m, n]

        Returns:
            Tensor: [b, m, d]
        """

        b, m, n = dmat.shape

        q = rearrange(
            self.Wq(q_input), "b m (h d) -> b h m d", h=self.num_heads
        )  # [b, h, m, d]
        k, v = rearrange(
            self.Wkv(kv_input), "b n (two h d) -> two b h n d", two=2, h=self.num_heads
        ).unbind(
            dim=0
        )  # [b, h, n, d]

        scale = math.sqrt(q.size(-1))  # scale factor
        attn_scores = torch.matmul(q, k.transpose(2, 3)) / scale  # [b, h, m, n]
        mix_attn_scores = torch.stack(
            [attn_scores, dmat[:, None, :, :].expand(b, self.num_heads, m, n)], dim=-1
        )  # [b, h, m, n, 2]

        mix_attn_scores = (
            (
                torch.matmul(
                    F.relu(
                        torch.matmul(mix_attn_scores.transpose(1, 2), self.mix_W1)
                        + self.mix_b1[None, None, :, None, :]
                    ),
                    self.mix_W2,
                )
                + self.mix_b2[None, None, :, None, :]
            )
            .transpose(1, 2)
            .squeeze(-1)
        )  # [b, h, m, n]

        attn_probs = F.softmax(mix_attn_scores, dim=-1)
        out = torch.matmul(attn_probs, v)
        return self.out_proj(rearrange(out, "b h s d -> b s (h d)"))


class MatNetMHA(nn.Module):
    def __init__(self, embed_dim: int, num_heads: int, bias: bool = False):
        super().__init__()
        self.row_encoding_block = MatNetCrossMHA(embed_dim, num_heads, bias)
        self.col_encoding_block = MatNetCrossMHA(embed_dim, num_heads, bias)

    def forward(self, row_emb, col_emb, dmat):
        """
        Args:
            row_emb (Tensor): [b, m, d]
            col_emb (Tensor): [b, n, d]
            dmat (Tensor): [b, m, n]

        Returns:
            Updated row_emb (Tensor): [b, m, d]
            Updated col_emb (Tensor): [b, n, d]
        """

        updated_row_emb = self.row_encoding_block(row_emb, col_emb, dmat)
        updated_col_emb = self.col_encoding_block(
            col_emb, row_emb, dmat.transpose(-2, -1)
        )
        return updated_row_emb, updated_col_emb


class MatNetMHALayer(nn.Module):
    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        bias: bool = False,
        feedforward_hidden: int = 512,
        normalization: Optional[str] = "instance",
    ):
        super().__init__()
        self.MHA = MatNetMHA(embed_dim, num_heads, bias)

        self.F_a = nn.ModuleDict(
            {
                "norm1": Normalization(embed_dim, normalization),
                "ffn": nn.Sequential(
                    nn.Linear(embed_dim, feedforward_hidden),
                    nn.ReLU(),
                    nn.Linear(feedforward_hidden, embed_dim),
                ),
                "norm2": Normalization(embed_dim, normalization),
            }
        )

        self.F_b = nn.ModuleDict(
            {
                "norm1": Normalization(embed_dim, normalization),
                "ffn": nn.Sequential(
                    nn.Linear(embed_dim, feedforward_hidden),
                    nn.ReLU(),
                    nn.Linear(feedforward_hidden, embed_dim),
                ),
                "norm2": Normalization(embed_dim, normalization),
            }
        )

    def forward(self, row_emb, col_emb, dmat):
        """
        Args:
            row_emb (Tensor): [b, m, d]
            col_emb (Tensor): [b, n, d]
            dmat (Tensor): [b, m, n]

        Returns:
            Updated row_emb (Tensor): [b, m, d]
            Updated col_emb (Tensor): [b, n, d]
        """

        row_emb_out, col_emb_out = self.MHA(row_emb, col_emb, dmat)

        row_emb_out = self.F_a["norm1"](row_emb + row_emb_out)
        row_emb_out = self.F_a["norm2"](row_emb_out + self.F_a["ffn"](row_emb_out))

        col_emb_out = self.F_b["norm1"](col_emb + col_emb_out)
        col_emb_out = self.F_b["norm2"](col_emb_out + self.F_b["ffn"](col_emb_out))
        return row_emb_out, col_emb_out


class MatNetMHANetwork(nn.Module):
    def __init__(
        self,
        embed_dim: int = 128,
        num_heads: int = 8,
        num_layers: int = 3,
        normalization: str = "batch",
        feedforward_hidden: int = 512,
        bias: bool = False,
    ):
        super().__init__()
        self.layers = nn.ModuleList(
            [
                MatNetMHALayer(
                    num_heads=num_heads,
                    embed_dim=embed_dim,
                    feedforward_hidden=feedforward_hidden,
                    normalization=normalization,
                    bias=bias,
                )
                for _ in range(num_layers)
            ]
        )

    def forward(self, row_emb, col_emb, dmat):
        """
        Args:
            row_emb (Tensor): [b, m, d]
            col_emb (Tensor): [b, n, d]
            dmat (Tensor): [b, m, n]

        Returns:
            Updated row_emb (Tensor): [b, m, d]
            Updated col_emb (Tensor): [b, n, d]
        """

        for layer in self.layers:
            row_emb, col_emb = layer(row_emb, col_emb, dmat)
        return row_emb, col_emb


class MatNetEncoder(nn.Module):
    def __init__(
        self,
        embed_dim: int = 256,
        num_heads: int = 16,
        num_layers: int = 5,
        normalization: str = "instance",
        feedforward_hidden: int = 512,
        init_embedding: nn.Module = None,
        init_embedding_kwargs: dict = None,
        bias: bool = False,
    ):
        super().__init__()

        if init_embedding is None:
            init_embedding = env_init_embedding(
                "matnet", {"embed_dim": embed_dim, **init_embedding_kwargs}
            )

        self.init_embedding = init_embedding
        self.net = MatNetMHANetwork(
            embed_dim=embed_dim,
            num_heads=num_heads,
            num_layers=num_layers,
            normalization=normalization,
            feedforward_hidden=feedforward_hidden,
            bias=bias,
        )

    def forward(self, td):
        row_emb, col_emb, dmat = self.init_embedding(td)
        row_emb, col_emb = self.net(row_emb, col_emb, dmat)

        embedding = (row_emb, col_emb)
        init_embedding = None
        return embedding, init_embedding  # match output signature for the AR policy class
