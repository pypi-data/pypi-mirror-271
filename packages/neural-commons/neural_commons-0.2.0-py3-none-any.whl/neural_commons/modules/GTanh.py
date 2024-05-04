import torch
from torch import nn


class GTanh(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        p = torch.exp(-(x ** 2))
        t = torch.tanh(x)
        return 2.4 * p + 0.2 * t - 1.6
