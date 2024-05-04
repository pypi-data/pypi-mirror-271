import unittest

import torch
from torch import nn

from neural_commons.cf_nn import CFConv2d, CFTrainer
from neural_commons.cf_nn.lrs import MSELossLRS


class TestCFConv2d(unittest.TestCase):
    def test_kernel1_stride1_bias(self):
        batch_size = 7
        in_channels = 4
        out_channels = 8
        kernel_size = 1
        stride = 1
        padding = 0
        height = 9
        width = 11
        ref_m = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding,
                          bias=True)
        x = torch.randn((batch_size, in_channels, height, width))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFConv2d(in_channels, out_channels, kernel_size, stride, padding,
                     bias=True),
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

    def test_kernel3_padding1_stride1_bias(self):
        batch_size = 7
        in_channels = 4
        out_channels = 8
        kernel_size = 3
        stride = 1
        padding = 1
        height = 11
        width = 9
        ref_m = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding,
                          bias=True)
        x = torch.randn((batch_size, in_channels, height, width))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFConv2d(in_channels, out_channels, kernel_size, stride, padding,
                     bias=True),
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

    def test_kernel3_padding0_stride1_bias(self):
        batch_size = 21
        in_channels = 8
        out_channels = 4
        kernel_size = 3
        stride = 1
        padding = 0
        height = 12
        width = 9
        ref_m = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding,
                          bias=True)
        x = torch.randn((batch_size, in_channels, height, width))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFConv2d(in_channels, out_channels, kernel_size, stride, padding,
                     bias=True),
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

    def test_kernel3_padding1_stride2_bias(self):
        batch_size = 7
        in_channels = 8
        out_channels = 4
        kernel_size = 3
        stride = 2
        padding = 1
        height = 12
        width = 9
        ref_m = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding,
                          bias=True)
        x = torch.randn((batch_size, in_channels, height, width))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFConv2d(in_channels, out_channels, kernel_size, stride, padding,
                     bias=True),
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

    def test_kernel3_5_padding1_2_stride2_3_no_bias(self):
        batch_size = 7
        in_channels = 8
        out_channels = 4
        kernel_size = (3, 5,)
        stride = (2, 3,)
        padding = (1, 2,)
        height = 12
        width = 9
        ref_m = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding,
                          bias=False)
        x = torch.randn((batch_size, in_channels, height, width))
        y = ref_m(x)
        opt_m = nn.Sequential(
            CFConv2d(in_channels, out_channels, kernel_size, stride, padding,
                     bias=False),
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
