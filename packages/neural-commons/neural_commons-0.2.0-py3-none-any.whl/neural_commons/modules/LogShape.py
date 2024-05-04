import logging

import torch
from torch import nn


class LogShape(nn.Module):
    def __init__(self, label: str, use_print: bool = False):
        super().__init__()
        self.use_print = use_print
        self.label = label

    def forward(self, x: torch.Tensor):
        message = f"{self.label}: {tuple(x.shape)}"
        if self.use_print:
            print(message)
        else:
            logging.warning(message)
        return x
