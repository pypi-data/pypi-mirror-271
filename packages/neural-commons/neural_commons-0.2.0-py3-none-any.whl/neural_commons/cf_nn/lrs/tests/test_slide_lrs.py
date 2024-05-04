import unittest

import torch
from torch import autograd

from neural_commons.cf_nn.lrs import SlideLRS
from neural_commons.modules import MAELoss, RMSELoss


class TestSlideLRS(unittest.TestCase):
    def test_slide_mae(self):
        torch.manual_seed(7)
        output = torch.randn((7, 12)).requires_grad_()
        target = torch.rand_like(output)
        loss_fn = MAELoss()
        loss = loss_fn(output, target)
        grad1 = autograd.grad(loss, output)[0]
        lrs = SlideLRS(0, final_factor=0.85)
        residuals = lrs.get_residual(True, output, loss, grad1, final_output_size=1)
        result = output + residuals
        loss_final = loss_fn(result, target)
        self.assertLess(loss_final, loss * 0.8)

    def test_slide_rmse(self):
        output = torch.randn((9, 15)).requires_grad_()
        target = torch.rand_like(output)
        loss_fn = RMSELoss()
        lrs = SlideLRS(0)
        loss = loss_fn(output, target)
        grad1 = autograd.grad(loss, output)[0]
        residuals = lrs.get_residual(True, output, loss, grad1, final_output_size=1)
        result = output + residuals
        loss_final = loss_fn(result, target).item()
        self.assertAlmostEqual(0, loss_final, delta=0.01)
