import torch
import torch.nn as nn
import torch.nn.functional as F


def multi_dim_norm(x: torch.Tensor, dim: int = 1) -> torch.Tensor:
    return torch.norm(x, dim=dim, p=2, keepdim=True)
