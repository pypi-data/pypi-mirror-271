import copy
import torch
from torch import nn
from neural_commons.modules import SMoEMixIn


class SMoE(nn.Module, SMoEMixIn):
    cluster_centroids: torch.Tensor

    def __init__(self, module: nn.Module, in_features: int, out_features: int,
                 num_experts: int = 64, ensemble_size: int = 3):
        if ensemble_size <= 0:
            raise ValueError(f"Invalid ensemble_size={ensemble_size}")
        if num_experts <= 0:
            raise ValueError(f"Invalid num_experts={num_experts}")
        if num_experts % 2 != 0:
            raise ValueError(f"num_experts(={num_experts}) must be an even number")
        if ensemble_size > num_experts:
            raise ValueError(f"ensemble_size={ensemble_size} > num_experts={num_experts}")
        super(SMoE, self).__init__()
        self.out_features = out_features
        self.experts = nn.ModuleList([copy.deepcopy(module) for _ in range(num_experts)])
        self.num_experts = num_experts
        self.ensemble_size = ensemble_size
        self.d_scale = nn.Parameter(torch.FloatTensor([[[0.1]]]))
        vectors = self.get_orthogonal_vectors(num_experts // 2, in_features)
        centroids = (torch.cat([vectors, -vectors], dim=0)
                     .detach().unsqueeze(0))
        # centroids: (1, num_experts, in_features,)
        self.register_buffer("cluster_centroids", centroids)

    def forward(self, x: torch.Tensor):
        es = self.ensemble_size
        # x: (batch_size, in_features)
        scaled_diff = self.d_scale * (x[:, None, :] - self.cluster_centroids)
        distance_sq = torch.mean(scaled_diff.pow(2), dim=2)
        # distance_sq: (batch_size, num_experts)
        sort_indexes = torch.argsort(distance_sq, dim=1)
        # sort_indexes: (batch_size, num_experts)
        picked_indexes = sort_indexes[:, :es]
        # picked_indexes: (batch_size, ensemble_size)
        select_distances = distance_sq[:, :es]
        select_weights = 1.0 / (1.0 + select_distances)
        # select_weights: (batch_size, ensemble_size)
        weight_sums = torch.sum(select_weights, dim=1, keepdim=True)
        select_weights /= weight_sums
        unique_weight_indexes = torch.unique(picked_indexes)
        batch_size = x.size(0)
        expert_out = torch.empty((batch_size, es, self.out_features), device=x.device)
        exec_indexes = []
        exec_results = []
        for wi in unique_weight_indexes:
            indexes = torch.where(picked_indexes == wi)
            row_idx, _ = indexes
            x_subset = x[row_idx]
            module = self.experts[wi.item()]
            result = module(x_subset)
            exec_indexes.append(indexes)
            exec_results.append(result)
        for (row_idx, e_idx), output in zip(exec_indexes, exec_results):
            expert_out[row_idx, e_idx, :] = output
        return torch.sum(expert_out * select_weights[:, :, None], dim=1)
