import string
import random
from typing import Dict

import torch

from dltrain.forward import Forward, SimpleForward
from dltrain.delineator import Delineator, TrainEvalSetDelineator, RandomSplitDelineator
from dltrain.transform import Container
from dltrain.dataset import DLDataset

from torch.nn import Module, CrossEntropyLoss, MSELoss
from torch.optim import Optimizer, Adam
from torch import device
from torch.optim.lr_scheduler import LRScheduler

from ..options import TrainOptions
from .optimizer import OptimizerWizard
from .scheduler import SchedulerWizard
from .base import BaseWizard
from .criterion import CriterionWizard
from .evaluation_handler import EvaluationWizard
from .model import ModelWizard
from .transforms import TransformWizard
from ..dataset import DatasetWizard

__all__ = [
    'TaskBuilder'
]


class TaskBuilder:
    def __init__(self, task_name=None):
        self.task_name: str = task_name if task_name is not None else ''.join(
            random.choices(string.digits + string.ascii_letters, k=5))

        self._forward: Forward = SimpleForward()
        self._delineator: Delineator = None

        self.evaluation_handler = EvaluationWizard()
        self.optimizer = OptimizerWizard()
        self.base = BaseWizard()
        self.criterion = CriterionWizard()
        self.scheduler = SchedulerWizard()
        self.model = ModelWizard()
        self.transform = TransformWizard()
        self.dataset = DatasetWizard()

    def use_forward(self, forward: Forward):
        self._forward = forward

    def use_train_eval_set(self, train_set: DLDataset, eval_set: DLDataset):
        self._delineator = TrainEvalSetDelineator(train_set, eval_set)

    def use_random_split_dataset(self, dataset: DLDataset, train=0.8, eval=0.2):
        self._delineator = RandomSplitDelineator(dataset, train, eval)

    def build(self):
        options = TrainOptions()
        options.task_name = self.task_name

        # 载入优化器
        optimizer = self.optimizer.get_kwargs()
        if optimizer['type'] is not None and optimizer['parameters'] is not None:
            options.optimizer_type = optimizer['type']
            options.optimizer_parameters = optimizer['parameters']

        # 载入基本信息
        for key, value in self.base.get_kwargs().items():
            if key in options.__dict__:
                options.__dict__[key] = value

        # 载入损失函数
        options.criterion = self.criterion.get_kwargs()['criterion']

        # 载入验证手段
        handlers = self.evaluation_handler.get_kwargs()
        options.train_evaluation_handlers = handlers['train_evaluation_handlers']
        options.eval_evaluation_handlers = handlers['eval_evaluation_handlers']

        # 载入策略器
        scheduler = self.scheduler.get_kwargs()
        if scheduler['type'] is not None and scheduler['parameters'] is not None:
            options.scheduler_type = scheduler['type']
            options.scheduler_parameters = scheduler['parameters']

        # 载入模型
        model = self.model.get_kwargs()['model']
        options.model = model

        # 载入数据变换
        transform = self.transform.get_kwargs()
        options.features_transform = Container(transform['features_transform'])
        options.targets_transform = Container(transform['targets_transform'])

        # 数据集设置
        options.delineator = self._delineator

        # 设置前馈
        options.forward = self._forward

        return options
