"""
core 模块
功能：包含包的核心功能和基础类。
子模块/文件：
base_model.py：定义基础模型类，提供模型初始化、保存、加载等基础功能。
utils.py：包含一些通用的工具函数，如数据处理、模型评估等。
"""






# core/__init__.py

# 导入 core 子包中的关键模块
# from . import data_structures
# from . import utils
# from . import model_builder
#
# 如果需要，可以直接导入这些模块中的特定类或函数

from .utils import evaluate_accuracy_gpu
from .utils import train_custom
from .utils import try_gpu
from .utils import try_all_gpus
# from .data_structures import CustomDataStructure
# from .utils import some_utility_function
# from .model_builder import build_model
#
# __all__ 变量定义了当使用 from core import * 时导入哪些对象
# 注意：通常不推荐使用 from package import *
__all__ = [
    'evaluate_accuracy_gpu',
    'train_custom',
    'try_gpu',
    'try_all_gpus'
]