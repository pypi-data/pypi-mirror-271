import math
import torch
import torch.nn.functional as F
from dataclasses import dataclass
from huggingface_hub import PyTorchModelHubMixin
from torch import nn, Tensor
from torch.nn import Parameter, init


@dataclass
class NeuralLayerConfig:
    in_features: int
    out_features: int
    bias: bool = True
    dtype: str = "float32"
    slopes_log_std: float = 0.1


class NeuralLayer(nn.Module, PyTorchModelHubMixin):
    __constants__ = ['in_features', 'out_features']
    in_features: int
    out_features: int
    weight: Tensor
    hp_params: Tensor

    def __init__(self, in_features: int, out_features: int, bias: bool = True,
                 slopes_log_std: float = 0.1) -> None:
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        slopes_t = torch.exp(torch.randn(self.out_features) * slopes_log_std)
        self.slopes = nn.Parameter(slopes_t.detach())
        setattr(self.slopes, "__skip_transplant__", True)
        self.weight = Parameter(torch.empty((self.out_features, self.in_features,)))
        if bias:
            self.bias = Parameter(torch.empty(self.out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        # Setting a=sqrt(5) in kaiming_uniform is the same as initializing with
        # uniform(-1/sqrt(in_features), 1/sqrt(in_features)). For details, see
        # https://github.com/pytorch/pytorch/issues/57109
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            init.uniform_(self.bias, -bound, bound)

    def forward(self, x: Tensor) -> Tensor:
        x = F.linear(x, self.weight, self.bias)
        positive = x >= 0
        return positive * x + (~positive) * x * self.slopes[None, :]

    def extra_repr(self) -> str:
        return f'in_features={self.in_features}, out_features={self.out_features}, bias={self.bias is not None}'


