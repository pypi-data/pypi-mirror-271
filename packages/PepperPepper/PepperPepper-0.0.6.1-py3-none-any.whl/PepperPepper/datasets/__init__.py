# datasets 模块
# 功能：包含数据集的加载、预处理和增强功能。
# 子模块/文件：
# image_datasets.py：图像数据集的处理，如CIFAR、ImageNet等。
# text_datasets.py：文本数据集的处理，如IMDB、WikiText等。
# custom_dataset.py：用户自定义数据集的示例或模板。










# datasets/__init__.py

# 导入 datasets 子包中的各个模块
# from . import mnist_dataset
# from . import cifar10_dataset
# from . import custom_dataset




# 如果需要，可以直接导入这些模块中的特定类或函数
from .image_datasets import load_data_minist
from .image_datasets import load_data_fashion_mnist
# from .cifar10_dataset import load_cifar10_data
# from .custom_dataset import load_custom_data
#
# __all__ 变量定义了当使用 from datasets import * 时导入哪些对象
# 注意：通常不推荐使用 from package import *
__all__ = [
    'load_data_minist',
    'load_data_fashion_mnist'
]


