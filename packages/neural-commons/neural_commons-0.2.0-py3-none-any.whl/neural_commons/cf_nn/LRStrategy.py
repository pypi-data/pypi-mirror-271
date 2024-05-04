import abc

import torch


class LRStrategy(abc.ABC):
    @abc.abstractmethod
    def requires_second_derivative(self) -> bool:
        pass

    @abc.abstractmethod
    def get_residual(self, is_final: bool, output: torch.Tensor, loss: torch.Tensor, grad1: torch.Tensor,
                     final_output_size: int) -> torch.Tensor:
        pass
