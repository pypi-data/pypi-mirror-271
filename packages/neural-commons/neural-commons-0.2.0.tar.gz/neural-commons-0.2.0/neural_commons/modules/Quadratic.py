import math
import torch
from torch import nn

_sqrt_2 = math.sqrt(2)


class Quadratic(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        self.linear = nn.Linear(in_features * 2, out_features, bias=bias)

    def forward(self, x: torch.Tensor):
        x_pow2 = (x.pow(2) - 1.0) / _sqrt_2
        x_expanded = torch.cat([x, x_pow2], dim=1)
        return self.linear(x_expanded)
