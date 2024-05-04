import logging
import math
from typing import Iterable, List, Union, Iterator

import torch
from torch import nn

_pulse = math.pi / 2.0


class CosineScheduler:
    def __init__(self, init_value: float, final_value: float, total_steps: int,
                 warmup_fraction: float = 0.03):
        self.final_value = final_value
        self.init_value = init_value
        self._actual_total_steps = total_steps + 1
        self._num_warmup_steps = self._actual_total_steps * warmup_fraction
        self._warned_step: bool = False
        self._index = 0

    def step(self):
        self._index += 1

    @property
    def value(self) -> float:
        step_x = self._index + 0.5
        if step_x < self._num_warmup_steps:
            current_factor = step_x / self._num_warmup_steps
        else:
            current_factor = math.cos(_pulse * (step_x - self._num_warmup_steps) /
                                      max(1.0, self._actual_total_steps -
                                          self._num_warmup_steps))
            if current_factor < 0:
                current_factor = 0
                if not self._warned_step:
                    logging.warning(f'CosineScheduler: step={self._index}, total_steps={self._actual_total_steps}')
                    self._warned_step = True
        return current_factor * self.init_value + (1 - current_factor) * self.final_value
