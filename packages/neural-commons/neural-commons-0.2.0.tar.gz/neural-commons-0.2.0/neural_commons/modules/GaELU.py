import torch
from torch import nn
import torch.nn.functional as F


class GaELU(nn.Module):
    def __init__(self):
        super(GaELU, self).__init__()

    def forward(self, x: torch.Tensor):
        p = torch.exp(-(x ** 2))
        return 1.23 * (F.elu(x) - p * 0.3)
