import math
from typing import Union
import torch
import torch.nn.functional as F
from neural_commons.cf_nn import CFModule
from neural_commons.helpers.torch_helper import ridge_regression

_size_2_t = Union[int, tuple[int, int]]
_sqrt_2 = math.sqrt(2)


class CFConv2d(CFModule):
    weight: torch.Tensor
    bias: torch.Tensor

    def __init__(self, in_channels: int, out_channels: int,
                 kernel_size: _size_2_t,
                 stride: _size_2_t = 1,
                 padding: _size_2_t = 0,
                 dilation: _size_2_t = 1,
                 bias: bool = True,
                 ):
        super().__init__()
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size,)
        if isinstance(stride, int):
            stride = (stride, stride,)
        if isinstance(dilation, int):
            dilation = (dilation, dilation,)
        bias_param = None if not bias else torch.randn((out_channels,)) / _sqrt_2
        scale = math.sqrt(in_channels * math.prod(kernel_size))
        if bias:
            scale *= _sqrt_2
        weight = torch.randn((out_channels, in_channels, *kernel_size)) / scale
        self.register_buffer("weight", weight)
        self.register_buffer("bias", bias_param)
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.padding = padding

    def forward(self, x: torch.Tensor):
        return torch.conv2d(x, self.weight, self.bias, self.stride, self.padding, self.dilation,
                            groups=1)

    def cf_learn(self, inputs: tuple[torch.Tensor, ...], output: torch.Tensor, residual: torch.Tensor,
                 reg_lambda: float = 1.0, **kwargs):
        has_bias = self.bias is not None
        x = inputs[0]
        # x: (batch_size, in_channels, height, width)
        # residual: (batch_size, out_channels, out_height, out_width)
        batch_size, _, height, width = x.shape
        unfolded_x = F.unfold(x, self.kernel_size, self.dilation, self.padding, self.stride)
        # unfolded_x: (batch_size, 9 * in_channels, height * width // 2)
        unfolded_x = torch.permute(unfolded_x, (0, 2, 1))
        # unfolded_x: (batch_size, out_height * out_width, 9 * in_channels)
        unfolded_dim_1 = unfolded_x.size(1)
        unfolded_x = unfolded_x.contiguous().view(batch_size * unfolded_dim_1, -1)
        # unfolded_x: (batch_size * out_height * out_width, 9 * in_channels)
        weight = self.weight.view(self.weight.size(0), -1)
        # weight: (out_channels, 9 * in_channels)
        unfolded_residual = torch.permute(residual, (0, 2, 3, 1))
        # unfolded_residual: (batch_size, out_height, out_width, out_channels)
        unfolded_residual = unfolded_residual.contiguous().view(batch_size * unfolded_dim_1, -1)
        # unfolded_residual: (batch_size * out_height * out_width, out_channels)
        w, b = ridge_regression(unfolded_x, unfolded_residual, bias=has_bias, reg_lambda=reg_lambda)
        weight = weight + w.t()
        self.weight = weight.view(*self.weight.shape)
        self.bias = None if b is None else self.bias + b
