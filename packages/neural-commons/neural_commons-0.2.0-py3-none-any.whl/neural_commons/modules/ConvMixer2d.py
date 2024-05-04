import torch
from torch import nn

from neural_commons.modules import Permute


class ConvMixer2d(nn.Module):
    def __init__(self, num_channels: int, width: int, height: int,
                 hidden_factor=3, kernel_size=3, hidden_s=10):
        super().__init__()
        self.height = height
        self.width = width
        self.num_channels = num_channels
        padding = kernel_size // 2
        conv_params = dict(kernel_size=kernel_size, padding=padding)
        hidden_w = width * hidden_factor
        hidden_h = height * hidden_factor
        self.mixer = nn.Sequential(
            Permute(0, 2, 1, 3),
            # shape: (batch_size, cell_img_size, hidden1, cell_img_size)
            nn.Conv2d(width, hidden_w, **conv_params),
            nn.ELU(),
            nn.Conv2d(hidden_w, width, **conv_params),
            Permute(0, 3, 1, 2),
            # shape: (batch_size, cell_img_size, cell_img_size, hidden1)
            nn.Conv2d(height, hidden_h, **conv_params),
            nn.ELU(),
            nn.Conv2d(hidden_h, height, **conv_params),
            Permute(0, 3, 2, 1),
        )
        self.select = nn.Sequential(
            nn.Conv2d(num_channels * 2, hidden_s, **conv_params),
            nn.ELU(),
            nn.Conv2d(hidden_s, 1, **conv_params),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor):
        # x: (batch_size, channels, width, height)
        mixed_x = self.mixer(x)
        combined_x = torch.cat([x, mixed_x], dim=1)
        select_weight = self.select(combined_x)
        return mixed_x * select_weight + x * (1 - select_weight)


if __name__ == '__main__':
    _x = torch.randn((3, 16, 14, 18))
    m = ConvMixer2d(16, 14, 18)
    y = m(_x)
    print(y.shape)
