# optimizers 模块
# 功能：包含优化器的实现或扩展。
# 子模块/文件：
# custom_optimizer.py：用户自定义优化器的示例或模板。









# # optimizers/__init__.py
#
# # 导入 optimizers 子包中的各个模块
# from . import sgd
# from . import adam
# from . import rmsprop
# from . import custom_optimizer
#
# # 如果需要，可以直接导入这些模块中的特定优化器类
# from .sgd import SGD
# from .adam import Adam
# from .rmsprop import RMSprop
# from .custom_optimizer import CustomOptimizer
#
# # __all__ 变量定义了当使用 from optimizers import * 时导入哪些对象
# # 注意：通常不推荐使用 from package import *
# __all__ = [
#     'SGD',
#     'Adam',
#     'RMSprop',
#     'CustomOptimizer',
#     # ... 其他希望用户直接访问的关键优化器类 ...
# ]