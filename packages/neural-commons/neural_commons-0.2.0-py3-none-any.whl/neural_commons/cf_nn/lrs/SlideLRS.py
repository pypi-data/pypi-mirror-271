import logging
import torch
from neural_commons.cf_nn import LRStrategy

_logger = logging.getLogger("neural-commons")


class SlideLRS(LRStrategy):
    def __init__(self, min_loss: float, final_factor: float = 1.0, non_final_factor: float = 1.0):
        super().__init__()
        if non_final_factor <= 0 or non_final_factor > 1:
            raise ValueError("non_final_factor must be in ]0, 1].")
        if final_factor <= 0 or final_factor > 1:
            raise ValueError("final_factor must be in ]0, 1].")
        self.final_factor = final_factor
        self.non_final_factor = non_final_factor
        self.min_loss = min_loss
        self.warned_low_loss = False

    def requires_second_derivative(self) -> bool:
        return False

    def get_residual(self, is_final: bool, output: torch.Tensor, loss: torch.Tensor, grad1: torch.Tensor,
                     final_output_size: int, eps=1e-30):
        deficit = loss.item() - self.min_loss
        if deficit < 0:
            deficit = 0
            if not self.warned_low_loss:
                _logger.warning(f"SlideLRS: Loss ({loss.item()}) is less than min_loss ({self.min_loss}).")
                self.warned_low_loss = True
        factor = self.final_factor if is_final else self.non_final_factor
        deficit *= factor
        denominator = torch.clamp(torch.sum(grad1.pow(2)), min=eps)
        lr = (deficit / denominator).item()
        return -lr * grad1
