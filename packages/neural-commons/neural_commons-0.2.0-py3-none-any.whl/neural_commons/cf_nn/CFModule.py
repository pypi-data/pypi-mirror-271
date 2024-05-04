import torch
from abc import abstractmethod
from torch import nn


class CFModule(nn.Module):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def cf_learn(self, inputs: tuple[torch.Tensor, ...], output: torch.Tensor, residual: torch.Tensor, **kwargs):
        """
        Applies a learning process that changes the parameters of the module instance.
        The learning process is expected to be quick.
        Args:
            inputs: The inputs provided to the module.
            output: The original output of the module.
            residual: The residuals that should be added to the original output to obtain the desired output.
            **kwargs: Custom parameters of the learning process.
        """
        pass
