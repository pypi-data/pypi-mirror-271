import math
from typing import Iterable, Optional
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

_sqrt_2 = math.sqrt(2)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def count_parameters_from_list(param_list: Iterable[nn.Parameter]):
    return sum(p.numel() for p in param_list)


def sin_pos_embeddings(seq_len: int, emb_dim: int) -> torch.Tensor:
    factors = torch.arange(1, emb_dim + 1)
    seq_range = torch.arange(0, seq_len)
    angles = math.pi * 2 * seq_range / seq_len
    return torch.sin(angles[:, None] * factors[None, :]) * _sqrt_2


def concatenate_tensors(list_of_tensors, dim: int = 0):
    if isinstance(list_of_tensors[0], tuple):
        concatenated_tuples = []
        for i in range(len(list_of_tensors[0])):
            concatenated_tensors = torch.cat([t[i] for t in list_of_tensors], dim=dim)
            concatenated_tuples.append(concatenated_tensors)
        return tuple(concatenated_tuples)
    else:
        return torch.cat(list_of_tensors, dim=dim)


def batched_apply(model: nn.Module, x: torch.Tensor, batch_size: int = 64, detached: bool = False):
    output_list = []
    num_items = x.size(0)
    for b0 in range(0, num_items, batch_size):
        input_batch = x[b0:b0 + batch_size]
        output_batch = model(input_batch)
        if detached:
            if isinstance(output_batch, tuple):
                output_batch = tuple([x.detach() for x in output_batch])
            else:
                output_batch = output_batch.detach()
        output_list.append(output_batch)
    output = concatenate_tensors(output_list)
    return output


def sample_tensor(tensor: torch.Tensor, count: int):
    perm = torch.randperm(tensor.size(0), device=tensor.device)
    return tensor[perm[:count]]


def sample_tensors(tensor1: torch.Tensor, tensor2: torch.Tensor, count: int):
    if tensor2.size(0) != tensor1.size(0):
        raise ValueError('Different batch sizes!')
    perm = torch.randperm(tensor1.size(0), device=tensor1.device)
    selection = perm[:count]
    return tensor1[selection], tensor2[selection],


def fixed_hash(text: str):
    h = 0
    for ch in text:
        h = (h * 281 ^ ord(ch) * 997) & 0xFFFFFFFF
    return h


def tensor_hash(t: torch.Tensor):
    return fixed_hash(str(t.cpu().tolist()))


def get_torch_dtype(dtype_str):
    if hasattr(torch, dtype_str):
        return getattr(torch, dtype_str)
    else:
        raise ValueError(f"Unknown dtype string: {dtype_str}")


def ridge_regression(x: torch.Tensor, y: torch.Tensor, bias: bool = True,
                     reg_lambda: float = 1e-5) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Performs ridge regression.
    Args:
        x: Input variables.
        y: Output variables.
        bias: Whether a bias parameter should be returned.
        reg_lambda: An L2 regularization parameter.
    Returns: A weight matrix of shape (in_features, out_features), and a bias parameter
    array of size (out_features) if the bias parameter is True.
    """
    with torch.no_grad():
        dev = x.device
        x_actual = x if not bias else torch.cat([x, torch.ones((x.size(0), 1),
                                                               device=dev)], dim=1)
        x_t = x_actual.t()
        sq_matrix = x_t @ x_actual
        weights = torch.inverse(
            sq_matrix + reg_lambda * torch.eye(x_t.size(0), device=dev)) @ x_t @ y
        # weights: (in_features, out_features)
        bias_param = torch.clone(weights[-1, :]) if bias else None
        if bias:
            weights = weights[:-1, :]
        return weights, bias_param,


def detach_tuple(tup: tuple[torch.Tensor, ...]) -> tuple[torch.Tensor, ...]:
    return tuple(t.detach() for t in tup)


def trim_outliers(tensor: torch.Tensor, zero_based: bool = False, z_score_threshold=3.0,
                  two_passes: bool = False, eps=1e-10):
    mean = 0 if zero_based else torch.mean(tensor).item()
    sd = torch.sqrt(torch.mean((tensor - mean).pow(2)))
    z_score = torch.abs(tensor - mean) / torch.clamp(sd, min=eps)
    is_outlier = z_score >= z_score_threshold
    if two_passes:
        sub_tensor = tensor[~is_outlier]
        if torch.numel(sub_tensor) == 0:
            raise ValueError("Unexpected: All elements are outliers.")
        mean = 0 if zero_based else torch.mean(sub_tensor).item()
        sd = torch.sqrt(torch.mean((sub_tensor - mean).pow(2)))
        z_score = torch.abs(tensor - mean) / torch.clamp(sd, min=eps)
        is_outlier = z_score >= z_score_threshold
    tensor_copy = torch.clone(tensor)
    tensor_copy[is_outlier] = mean + torch.sign(tensor_copy[is_outlier] - mean) * sd * z_score_threshold
    return tensor_copy
