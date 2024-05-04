import math
import torch
import torch.nn.functional as F
from neural_commons.helpers.torch_helper import ridge_regression
from neural_commons.cf_nn import CFModule


_sqrt_2 = math.sqrt(2)


class CFLinear(CFModule):
    __constants__ = ["in_features", "out_features"]
    weight: torch.Tensor
    bias: torch.Tensor

    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        scale = math.sqrt(in_features)
        if bias:
            scale *= _sqrt_2
        weight = torch.randn((out_features, in_features)) / scale
        bias_param = torch.randn((out_features,)) / _sqrt_2 if bias else None
        self.register_buffer("weight", weight)
        self.register_buffer("bias", bias_param)
        self.in_features = in_features
        self.out_features = out_features

    def forward(self, x: torch.Tensor):
        return F.linear(x, self.weight, self.bias)

    def cf_learn(self, inputs: tuple[torch.Tensor, ...], output: torch.Tensor, residual: torch.Tensor,
                 reg_lambda: float = 1.0, **kwargs):
        has_bias = self.bias is not None
        x = inputs[0]
        w, b = ridge_regression(x, residual, bias=has_bias, reg_lambda=reg_lambda)
        self.weight = self.weight + w.t()
        self.bias = None if b is None else self.bias + b

    def extra_repr(self) -> str:
        return f'in_features={self.in_features}, out_features={self.out_features}, bias={self.bias is not None}'
