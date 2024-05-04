import torch
from typing import Union
from torch import nn, Tensor


class NeuralLayer2d(nn.Module):
    def __init__(self, in_channels: int, out_channels: int,
                 kernel_size: Union[int, tuple[int, int]],
                 slopes_log_std=0.1,
                 **kwargs):
        super().__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels,
                              kernel_size=kernel_size, **kwargs)
        slopes_t = torch.exp(torch.randn(out_channels) * slopes_log_std)
        self.slopes = nn.Parameter(slopes_t.detach())
        setattr(self.slopes, "__skip_transplant__", True)

    def forward(self, x: Tensor) -> Tensor:
        x = self.conv(x)
        positive = x >= 0
        return positive * x + (~positive) * x * self.slopes[None, :, None, None]
