import math

import torch


class AdaptiveSimpleNorm(torch.nn.Module):
    def __init__(self, momentum=0.1, eps=1e-10):
        super(AdaptiveSimpleNorm, self).__init__()
        self.momentum = momentum
        self.eps = eps
        self.mean = 0
        self.std = 1.0

    def forward(self, x):
        if self.training:
            x_mean = torch.mean(x).item()
            x_var = torch.mean((x - self.mean).pow(2)).item()
            x_std = math.sqrt(x_var + self.eps)
            m = self.momentum
            m1m = 1 - m
            self.mean = m1m * self.mean + m * x_mean
            self.std = m1m * self.std + m * x_std
        return (x - self.mean) / self.std
