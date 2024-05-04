import torch
from torch import nn


class MAELoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, yhat, y):
        return torch.mean(torch.abs(yhat - y))
