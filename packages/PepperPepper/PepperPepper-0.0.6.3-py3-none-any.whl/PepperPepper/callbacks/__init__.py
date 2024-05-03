# callbacks 模块
# 功能：包含训练过程中的回调函数，用于实现如学习率调整、模型保存等功能。
# 子模块/文件：
# learning_rate_scheduler.py：学习率调整策略的实现。
# custom_callback.py：用户自定义回调函数的示例或模板。














# callbacks/__init__.py

# 导入 callback 子包中的各个模块
# from . import logging_callback
# from . import model_checkpoint_callback
# from . import early_stopping_callback
#
# 如果需要，可以直接导入这些模块中的特定回调类
from .custom_callback import save_best_model
from .custom_callback import load_best_model
# from .logging_callback import LoggingCallback
# from .model_checkpoint_callback import ModelCheckpointCallback
# from .early_stopping_callback import EarlyStoppingCallback
#
# # __all__ 变量定义了当使用 from callback import * 时导入哪些对象
# # 注意：通常不推荐使用 from package import *
__all__ = [
    'save_best_model',
    'load_best_model'
]