# custom_deep_learning/__init__.py

# 导出子模块，但不导出子模块中的具体函数或类
from . import core
from . import models
from . import layers
from . import datasets
from . import optimizers
from . import losses
from . import callbacks
from . import examples
from . import tools



__all__ = ['core', 'layers', 'datasets', 'optimizers', 'losses', 'callbacks', 'examples', 'tools']





# 你可以在这里添加一些文档字符串，描述这个包的功能和使用方式
"""  
自定义深度学习包，用于完成深度学习相关的操作和复现代码。  

子模块：  
    core: 包含包的核心功能和基础类。  
    models: 包含各种深度学习模型的实现。  
    layers: 包含自定义的神经网络层或模块。  
    datasets: 包含数据集的加载、预处理和增强功能。  
    optimizers: 包含优化器的实现或扩展。  
    losses: 包含损失函数的实现或扩展。  
    callbacks: 包含训练过程中的回调函数。  
    examples: 包含使用本包进行深度学习任务的示例代码。  
    tools:包含直接自定义工具
"""





"""
当规划一个自定义的深度学习包时，合理的包结构对于提高代码的可读性、可维护性和复用性至关重要。
以下是一个建议的包结构及其模块命名和功能描述：

包名: PepperPepper

模块:

core 模块
功能：包含包的核心功能和基础类。
子模块/文件：
base_model.py：定义基础模型类，提供模型初始化、保存、加载等基础功能。
utils.py：包含一些通用的工具函数，如数据处理、模型评估等。

models 模块
功能：包含各种深度学习模型的实现。
子模块/文件：
cnn.py：卷积神经网络（CNN）相关模型的实现。
rnn.py：循环神经网络（RNN）相关模型的实现。
transformer.py：Transformer模型及其变体的实现。
custom_model.py：用户自定义模型的示例或模板。

layers 模块
功能：包含自定义的神经网络层或模块。
子模块/文件：
attention.py：实现各种注意力机制层。
custom_layer.py：用户自定义层的示例或模板。

datasets 模块
功能：包含数据集的加载、预处理和增强功能。
子模块/文件：
image_datasets.py：图像数据集的处理，如CIFAR、ImageNet等。
text_datasets.py：文本数据集的处理，如IMDB、WikiText等。
custom_dataset.py：用户自定义数据集的示例或模板。

optimizers 模块
功能：包含优化器的实现或扩展。
子模块/文件：
custom_optimizer.py：用户自定义优化器的示例或模板。

losses 模块
功能：包含损失函数的实现或扩展。
子模块/文件：
custom_loss.py：用户自定义损失函数的示例或模板。

callbacks 模块
功能：包含训练过程中的回调函数，用于实现如学习率调整、模型保存等功能。
子模块/文件：
learning_rate_scheduler.py：学习率调整策略的实现。
custom_callback.py：用户自定义回调函数的示例或模板。

examples 模块
功能：包含使用custom_deep_learning包进行深度学习任务的示例代码。
子模块/文件：
image_classification.py：使用CNN进行图像分类的示例。
text_generation.py：使用Transformer进行文本生成的示例。
custom_task.py：用户自定义任务的示例。
这样的包结构使得每个模块都有其明确的功能和职责，方便用户根据需要进行查找和使用。同时，用户还可以根据具体需求在已有模块的基础上进行扩展或添加新的模块。
"""



"""
__init__.py 文件起到了非常关键的作用，它用于初始化包，并可以定义一些公共的导入或设置。以下是如何设计您的自定义包结构以及编写 __init__.py 文件的一些建议。

包结构设计
首先，根据您之前提供的模块列表，我们可以组织包结构如下：

custom_deep_learning/  
├── __init__.py  
├── core/  
│   ├── __init__.py  
│   ├── base_model.py  
│   └── utils.py  
├── models/  
│   ├── __init__.py  
│   ├── cnn.py  
│   ├── rnn.py  
│   ├── transformer.py  
│   └── custom_model.py  
├── layers/  
│   ├── __init__.py  
│   ├── attention.py  
│   └── custom_layer.py  
├── datasets/  
│   ├── __init__.py  
│   ├── image_datasets.py  
│   ├── text_datasets.py  
│   └── custom_dataset.py  
├── optimizers/  
│   ├── __init__.py  
│   └── custom_optimizer.py  
├── losses/  
│   ├── __init__.py  
│   └── custom_loss.py  
├── callbacks/  
│   ├── __init__.py  
│   ├── learning_rate_scheduler.py  
│   └── custom_callback.py  
└── examples/  
    ├── __init__.py  
    ├── image_classification.py  
    ├── text_generation.py  
    └── custom_task.py
"""


