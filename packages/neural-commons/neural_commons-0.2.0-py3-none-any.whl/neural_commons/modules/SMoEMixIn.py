from typing import Optional
import math
import torch


class SMoEMixIn:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_orthogonal_vectors(n: int, in_features: int):
        if n > in_features:
            q: Optional[torch.Tensor] = None
            while q is None or q.size(1) < n:
                q0, _ = torch.linalg.qr(torch.randn((in_features, in_features)))
                if q is None:
                    q = q0
                else:
                    q = torch.cat([q, q0], dim=1)
            q = torch.clone(q[:, :n])
        else:
            q, _ = torch.linalg.qr(torch.randn((in_features, n)))
        q = torch.transpose(q, 0, 1)
        return q * math.sqrt(in_features)
