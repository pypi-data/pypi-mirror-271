import torch.nn as nn
from neural_commons.modules import Quadratic


class RndNonLinearFunction(nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        hidden_size = max(input_size, output_size) * 15
        self.layers = nn.Sequential(
            Quadratic(input_size, hidden_size),
            Quadratic(hidden_size, output_size),
        )

    def forward(self, x):
        return self.layers(x) * 3
