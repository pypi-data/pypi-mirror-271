# models 模块
# 功能：包含各种深度学习模型的实现。
# 子模块/文件：
# cnn.py：卷积神经网络（CNN）相关模型的实现。
# rnn.py：循环神经网络（RNN）相关模型的实现。
# transformer.py：Transformer模型及其变体的实现。
# custom_model.py：用户自定义模型的示例或模板。

# models/__init__.py
# 如果需要，您可以直接导入这些模块中的特定类或函数
from .cnn import LeNet5
from .cnn import AlexNet
from .cnn import VGGBlock
from .cnn import VGG16
from .cnn import MLPConv
from .cnn import NiNBlock
from .cnn import NiN
from .cnn import InceptionBlockV1
from .cnn import GoogLeNet



#from .rnn import RNNModel
#from .transformer import TransformerModel
#from .custom_model import CustomModel


# __all__ 变量定义了当使用 from models import * 时导入哪些对象
# 注意：通常不推荐使用 from package import *
__all__ = [
   'LeNet5',
   'AlexNet',
   'VGGBlock',
   'VGG16',
   'MLPConv',
   'NiNBlock',
   'NiN',
   'InceptionBlockV1',
   'GoogLeNet'
]