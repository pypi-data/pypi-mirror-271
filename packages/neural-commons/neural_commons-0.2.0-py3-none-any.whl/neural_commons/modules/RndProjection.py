import torch
import torch.nn.functional as F
from torch import nn, Generator


class RndProjection(nn.Module):
    weight: torch.Tensor

    def __init__(self, in_features: int, out_features: int, seed: int = 1001):
        super().__init__()
        weight = self.build_weight_matrix(in_features, out_features, seed=seed)
        self.register_buffer('weight', weight)

    @staticmethod
    def build_weight_matrix(in_features: int, out_features: int, seed: int = 1001):
        # Needs to build a matrix of shape (out_features, in_features,)
        # Given input of shape (b, in_features), multiply by the transpose, and get (b, out_features,)
        return RndProjection._build_weight_impl(in_features, out_features, seed=seed)

    @staticmethod
    def _build_weight_impl(in_features: int, out_features: int, seed: int):
        g = Generator()
        g.manual_seed(seed)
        in_count = 0
        q_list = []
        while in_count < in_features:
            rnd_matrix = torch.randn((out_features, out_features), generator=g)
            q, _ = torch.linalg.qr(rnd_matrix, mode='complete')
            in_count += out_features
            q_list.append(q)
        q_t = torch.cat(q_list, dim=1)
        q_t = torch.clone(q_t[:, :in_features])
        return q_t

    def forward(self, x: torch.Tensor):
        return F.linear(x, self.weight, bias=None)


if __name__ == '__main__':
    torch.set_grad_enabled(True)
    _ol = RndProjection(384, 512)
    _x = torch.randn((5, 384))
    _y = _ol(_x)
    print(_y.size())
    print(torch.std(_y).item())
    print('_x norm: ', torch.norm(_x, dim=1))
    print('_y norm: ', torch.norm(_y, dim=1))


