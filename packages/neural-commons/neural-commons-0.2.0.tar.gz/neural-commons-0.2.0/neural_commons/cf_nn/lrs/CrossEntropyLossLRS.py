import datetime
import math
import os

import torch
from neural_commons.cf_nn import LRStrategy


class CrossEntropyLossLRS(LRStrategy):
    def __init__(self):
        super().__init__()

    def requires_second_derivative(self) -> bool:
        return False

    def get_residual(self, is_final: bool, output: torch.Tensor, loss: torch.Tensor, grad1: torch.Tensor,
                     final_output_size: int):
        batch_size = output.size(0)
        output_size = math.prod(output.shape[1:])
        fos = output_size if is_final else final_output_size
        base_result = 1.5 * batch_size * fos
        if is_final:
            lr = base_result
        else:
            factor_min = 1.0
            factor_max = 14.0
            partial_os = output_size / 3
            max_w = partial_os / (partial_os + final_output_size)
            factor = factor_min * (1 - max_w) + factor_max * max_w
            lr = factor * base_result
        return -lr * grad1
