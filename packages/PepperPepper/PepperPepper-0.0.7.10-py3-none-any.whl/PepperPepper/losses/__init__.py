# losses 模块
# 功能：包含损失函数的实现或扩展。
# 子模块/文件：
# custom_loss.py：用户自定义损失函数的示例或模板。












# # losses/__init__.py
#
# # 导入 losses 子包中的各个模块
# from . import mean_squared_error
# from . import categorical_crossentropy
# from . import custom_loss
#
# # 如果需要，可以直接导入这些模块中的特定损失函数或类
# from .mean_squared_error import mean_squared_error_loss
# from .categorical_crossentropy import categorical_crossentropy_loss
# from .custom_loss import custom_loss_function
#
# # __all__ 变量定义了当使用 from losses import * 时导入哪些对象
# # 注意：通常不推荐使用 from package import *
# __all__ = [
#     'mean_squared_error_loss',
#     'categorical_crossentropy_loss',
#     'custom_loss_function',
#     # ... 其他希望用户直接访问的关键损失函数或类 ...
# ]