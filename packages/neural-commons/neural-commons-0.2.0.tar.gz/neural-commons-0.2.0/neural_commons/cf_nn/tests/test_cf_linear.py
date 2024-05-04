import unittest

import torch
from torch import nn

from neural_commons.cf_nn import CFModule, CFLinear
from neural_commons.cf_nn.CFTrainer import CFTrainer
from neural_commons.cf_nn.lrs import MSELossLRS


class TestCFLinear(unittest.TestCase):
    def test_regression_with_bias(self):
        in_features = 32
        out_features = 24
        batch_size = 100
        ref_m = nn.Linear(in_features, out_features, bias=True)
        x = torch.randn((batch_size, in_features))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=True),
        )
        loss_fn = nn.MSELoss()
        with CFTrainer(opt_m, lrs=MSELossLRS()) as trainer:
            pred_y = opt_m(x)
            loss = loss_fn(pred_y, y)
            trainer.register_forward_pass((pred_y,), loss, max_displacement=2.0)
            loss_value = loss.item()
            print(f"Original loss: {loss_value}")
            trainer.train_step(update_rate=1.0, reg_lambda=0.0001)
        pred_y_2 = opt_m(x)
        loss = loss_fn(pred_y_2, y)
        loss_value = loss.item()
        print(f"Final loss: {loss_value}")
        self.assertAlmostEqual(0, loss_value, delta=0.01)

    def test_regression_without_bias(self):
        in_features = 24
        out_features = 32
        batch_size = 100
        ref_m = nn.Linear(in_features, out_features, bias=False)
        x = torch.randn((batch_size, in_features))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=False),
        )
        loss_fn = nn.MSELoss()
        with CFTrainer(opt_m, lrs=MSELossLRS()) as trainer:
            pred_y = opt_m(x)
            loss = loss_fn(pred_y, y)
            trainer.register_forward_pass((pred_y,), loss, max_displacement=2.0)
            loss_value = loss.item()
            print(f"Original loss: {loss_value}")
            trainer.train_step(update_rate=1.0, reg_lambda=0.0001)
        pred_y_2 = opt_m(x)
        loss = loss_fn(pred_y_2, y)
        loss_value = loss.item()
        print(f"Final loss: {loss_value}")
        self.assertAlmostEqual(0, loss_value, delta=0.01)

    def test_multi_layer(self):
        in_features = 24
        out_features = 32
        batch_size = 100
        ref_m = nn.Linear(in_features, out_features, bias=False)
        x = torch.randn((batch_size, in_features))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFLinear(in_features, 128),
            CFLinear(128, out_features),
        )
        loss_fn = nn.MSELoss()
        with CFTrainer(opt_m, lrs=MSELossLRS()) as trainer:
            pred_y = opt_m(x)
            loss = loss_fn(pred_y, y)
            trainer.register_forward_pass((pred_y,), loss, max_displacement=2.0)
            loss_value = loss.item()
            print(f"Original loss: {loss_value}")
            trainer.train_step(update_rate=1.0, reg_lambda=0.0001)
        pred_y_2 = opt_m(x)
        loss = loss_fn(pred_y_2, y)
        loss_value = loss.item()
        print(f"Final loss: {loss_value}")
        self.assertAlmostEqual(0, loss_value, delta=0.8)
