import logging
import math
import time
from typing import Iterable, List, Union, Iterator

import torch
from torch import nn

_pulse = math.pi / 2.0


class TBCosineScheduleOptimizer:
    def __init__(self, parameters: Union[Iterator[nn.Parameter], List[dict]], lr: float, total_time: float,
                 min_lr_factor: float = 0.02, warmup_fraction: float = 0.03, start_time: float = None):
        warmup_time = total_time * warmup_fraction
        ramp_down_time = total_time - warmup_time
        warned_step: bool = False
        if start_time is None:
            start_time = time.time()

        def _get_lr(step: int):
            nonlocal warned_step
            elapsed = time.time() - start_time
            if elapsed < warmup_time:
                current_factor = elapsed / warmup_time
            else:
                elapsed_since_warmup = elapsed - warmup_time
                current_factor = (min_lr_factor +
                                  (1 - min_lr_factor) * math.cos(_pulse * elapsed_since_warmup /
                                                                 max(1.0, ramp_down_time)))
                if current_factor < 0:
                    current_factor = 0
                    if not warned_step:
                        logging.warning(f'Scheduler: step={step}, elapsed={elapsed}, total_time={total_time}')
                        warned_step = True
            return current_factor

        self.optimizer = torch.optim.Adam(parameters, lr=lr)
        self.scheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer,
                                                           lr_lambda=_get_lr)

    def zero_grad(self, set_to_none: bool = False):
        self.optimizer.zero_grad(set_to_none=set_to_none)

    def step(self):
        self.optimizer.step()
        self.scheduler.step()

    def get_lr(self, index: int = 0):
        return self.scheduler.get_last_lr()[index]

    def get_all_lrs(self) -> List[float]:
        return self.scheduler.get_last_lr()
