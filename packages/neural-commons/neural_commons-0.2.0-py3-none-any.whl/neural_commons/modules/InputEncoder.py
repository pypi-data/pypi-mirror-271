from dataclasses import dataclass
import torch
from huggingface_hub import PyTorchModelHubMixin
from torch import nn
from neural_commons.modules import NeuralLayer, AdaptiveSimpleNorm


@dataclass
class InputEncoderConfig:
    in_features: int
    out_features: int
    hidden_factor: int = 3
    tag: str = ""
    latent_std: float = None


class InputEncoder(nn.Module, PyTorchModelHubMixin):
    def __init__(self, config: InputEncoderConfig):
        super(InputEncoder, self).__init__()
        super(PyTorchModelHubMixin, self).__init__()
        if isinstance(config, dict):
            config = InputEncoderConfig(**config)
        in_features = config.in_features
        out_features = config.out_features
        hidden_factor = config.hidden_factor
        hidden1 = out_features * hidden_factor
        self.config = config
        self.latent_std = config.latent_std
        self.encoder = nn.Sequential(
            NeuralLayer(in_features, hidden1),
            NeuralLayer(hidden1, hidden1),
            nn.Linear(hidden1, out_features),
        )

    def forward(self, x: torch.Tensor):
        y = self.encoder(x)
        if self.latent_std is not None:
            y = y / self.latent_std
        return y
