from ..environment import np, pd, plt,torch




"""
1.LeNet
abstract:
        LeNet5是一个经典的卷积神经网络，由多个卷积层、池化层和全连接层组成。它通过卷积操作提取图像中的局部特征，利用池化层进行特征下采样，并通过全连接层进行分类。LeNet最初用于手写数字识别任务，并展现出了良好的性能。其结构简洁明了，为后续更复杂的神经网络结构提供了基础，对深度学习领域的发展产生了重要影响。

struct:
        卷积编码器：由两个卷积层组成;
        全连接层密集块：由三个全连接层组成。

input: 
        28*28的单通道（黑白）图像通过LeNet,1×28×28。
    
output: 
        最后一层输出为10的Linear层，分别代表十种数字的类别数。
"""
class LeNet5(torch.nn.Module):
    def __init__(self, num_classes=10):
        super(LeNet5, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 6, 5,padding=2)  # 输入通道数为1，输出通道数为6，卷积核大小为5
        self.conv2 = torch.nn.Conv2d(6, 16, 5)  # 输入通道数为6，输出通道数为16，卷积核大小为5
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 120)  # 输入特征数为16*5*5，输出特征数为120
        self.fc2 = torch.nn.Linear(120, 84)  # 输入特征数为120，输出特征数为84
        self.fc3 = torch.nn.Linear(84, num_classes)  # 输入特征数为84，输出特征数为类别数

    def forward(self, x):
        # 添加ReLU激活函数和最大池化层
        x = torch.nn.functional.sigmoid(self.conv1(x))
        x = torch.nn.functional.max_pool2d(x, kernel_size=2,stride=2)
        x = torch.nn.functional.sigmoid(self.conv2(x))
        x = torch.nn.functional.max_pool2d(x, kernel_size=2,stride=2)

        # 将卷积层的输出展平
        x = x.view(x.size(0), -1)

        x = torch.nn.functional.sigmoid(self.fc1(x))
        x = torch.nn.functional.sigmoid(self.fc2(x))
        x = self.fc3(x)

        return x


    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)
            elif isinstance(m, torch.nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)





"""
2.AlexNet
abstract:
        AlexNet 是 2012 年 ImageNet 竞赛的冠军模型，由 Alex Krizhevsky、Ilya Sutskever 和 Geoffrey Hinton 提出。

struct:
        模型首先包含了一个特征提取部分 self.features，该部分由几个卷积层、ReLU 激活函数和最大池化层组成。然后，通过一个自适应平均池化层 self.avgpool 将特征图的大小减小到 6x6。最后，通过三个全连接层 self.classifier 进行分类。

input: 
        输入图像的大小是 3x224x224（AlexNet 的原始输入大小）。

output: 
        num_classes 参数用于指定分类的类别数，你可以根据你的任务需求进行修改。
"""
# 定义AlexNet模型类，继承自nn.Module
class AlexNet(torch.nn.Module):
    # 初始化函数，用于设置网络层
    def __init__(self, num_classes=1000):
        super(AlexNet,self).__init__()  # 调用父类nn.Module的初始化函数

        # 定义特征提取部分
        self.features = torch.nn.Sequential(
            # 第一个卷积层，输入通道3（RGB），输出通道64，卷积核大小11x11，步长4，填充2
            torch.nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            # ReLU激活函数，inplace=True表示直接修改原变量，节省内存
            torch.nn.ReLU(inplace=True),
            # 最大池化层，池化核大小3x3，步长2
            torch.nn.MaxPool2d(kernel_size=3, stride=2),

            # 第二个卷积层，输入通道64，输出通道192，卷积核大小5x5，填充2
            torch.nn.Conv2d(64, 192, kernel_size=5, padding=2),
            torch.nn.ReLU(inplace=True),
            torch.nn.MaxPool2d(kernel_size=3, stride=2),

            # 接下来的三个卷积层没有池化层
            torch.nn.Conv2d(192, 384, kernel_size=3, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(384, 256, kernel_size=3, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(256, 256, kernel_size=3, padding=1),
            torch.nn.ReLU(inplace=True),

            # 最后一个最大池化层
            torch.nn.MaxPool2d(kernel_size=3, stride=2),
        )

        # 自适应平均池化层，将特征图大小调整为6x6
        self.avgpool = torch.nn.AdaptiveAvgPool2d((6, 6))

        # 定义分类器部分
        self.classifier = torch.nn.Sequential(
            # Dropout层用于防止过拟合
            torch.nn.Dropout(),
            # 第一个全连接层，输入特征数量取决于上一个池化层的输出，输出4096
            torch.nn.Linear(256 * 6 * 6, 4096),
            torch.nn.ReLU(inplace=True),
            # 第二个Dropout层
            torch.nn.Dropout(),
            # 第二个全连接层，输出4096
            torch.nn.Linear(4096, 4096),
            torch.nn.ReLU(inplace=True),
            # 输出层，输出类别数由num_classes指定
            torch.nn.Linear(4096, num_classes),
        )


    def forward(self, x):
        # 数据通过特征提取部分
        x = self.features(x)
        # 数据通过自适应平均池化层
        x = self.avgpool(x)
        # 将数据展平为一维向量，以便输入到全连接层
        x = torch.flatten(x, 1)
        # 数据通过分类器部分
        x = self.classifier(x)
        # 返回最终分类结果
        return x


    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)
            elif isinstance(m, torch.nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)






# 3.定义一个VGG卷积块
class VGGBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, num_convs, pool=True):
        """
        VGG块，包含多个卷积层和一个可选的最大池化层

        参数:
            in_channels (int): 输入通道数
            out_channels (int): 输出通道数（每个卷积层的输出通道数）
            num_convs (int): 卷积层的数量
            pool (bool, 可选): 是否在块后添加最大池化层。默认为True
        """
        super(VGGBlock, self).__init__()

        # 创建多个卷积层，每个卷积层后面都跟着ReLU激活函数
        layers = []
        for _ in range(num_convs):
            layers.append(torch.nn.Conv2d(in_channels if _ == 0 else out_channels, out_channels, kernel_size=3, padding=1))
            layers.append(torch.nn.ReLU(inplace=True))

            # 如果有池化层，则添加
        if pool:
            layers.append(torch.nn.MaxPool2d(kernel_size=2, stride=2))

            # 将所有层组合成一个Sequential模块
        self.conv_block = torch.nn.Sequential(*layers)

    def forward(self, x):
        """
        前向传播

        参数:
            x (torch.Tensor): 输入张量

        返回:
            torch.Tensor: 输出张量
        """
        x = self.conv_block(x)
        return x






#4.定义VGG16模型
class VGG16(torch.nn.Module):
    def __init__(self, num_classes=1000):
        """
        VGG16模型

        参数:
            num_classes (int, 可选): 分类的数量。默认为1000
        """
        super(VGG16, self).__init__()

        # 定义特征提取部分
        self.features = torch.nn.Sequential(
            VGGBlock(3, 64, 2, pool=True),  # block1: 64 channels, 2 conv layers, maxpool
            VGGBlock(64, 128, 2, pool=True),  # block2: 128 channels, 2 conv layers, maxpool
            VGGBlock(128, 256, 3, pool=True),  # block3: 256 channels, 3 conv layers, maxpool
            VGGBlock(256, 512, 3, pool=True),  # block4: 512 channels, 3 conv layers, maxpool
            VGGBlock(512, 512, 3, pool=True)  # block5: 512 channels, 3 conv layers, maxpool
        )

        # 定义分类器部分（全连接层）
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(512 * 7 * 7, 4096),  # fully connected layer, 4096 output neurons
            torch.nn.ReLU(True),
            torch.nn.Dropout(),
            torch.nn.Linear(4096, 4096),
            torch.nn.ReLU(True),
            torch.nn.Dropout(),
            torch.nn.Linear(4096, num_classes)  # fully connected layer, num_classes output neurons for classification
        )

        # 初始化权重
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    torch.nn.init.constant_(m.bias, 0)
            elif isinstance(m, torch.nn.Linear):
                torch.nn.init.normal_(m.weight, 0, 0.01)
                torch.nn.init.constant_(m.bias, 0)

    def forward(self, x):
        """
        前向传播

        参数:
            x (torch.Tensor): 输入张量

        返回:
            torch.Tensor: 分类的logits
        """
        # 特征提取
        x = self.features(x)

        # 在将特征图送入全连接层之前，需要将其展平（flatten）
        # 假设输入图像的大小是3x224x224，经过5个池化层（每个池化层将尺寸减半）后，
        # 特征图的大小会变成 7x7
        x = x.view(x.size(0), -1)  # 展平操作，-1 表示让PyTorch自动计算该维度的大小

        # 送入分类器
        x = self.classifier(x)

        return x











#5.MLPConv层
class MLPConv(torch.nn.Module):
    """
    MLPConv层，包含一个1x1卷积层模拟MLP的行为
    """
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(MLPConv,self).__init__()
        # 第一个1x1卷积层，用于减少通道数
        self.conv1 = torch.nn.Conv2d(in_channels, hidden_channels, kernel_size=1, bias=True)

        # ReLU激活函数
        self.relu = torch.nn.ReLU(inplace=True)

        # 第二个1x1卷积层，用于恢复到输出通道数
        self.conv2 = torch.nn.Conv2d(hidden_channels, out_channels, kernel_size=1, bias=True)



    def forward(self, x):
        # 通过第一个1x1卷积层
        x = self.conv1(x)
        # 应用ReLU激活函数
        x = self.relu(x)
        # 通过第二个1x1卷积层
        x = self.conv2(x)
        # 应用ReLU激活函数
        x = self.relu(x)
        return x






#6.NiN块
class NiNBlock(torch.nn.Module):
    """
    NiN块，包含一个标准的卷积层和一个MLPConv层
    """
    def __init__(self, in_channels, num_channels, kernel_size=3, stride=1, padding=1):
        super(NiNBlock, self).__init__()
        # 标准的卷积层
        self.conv = torch.nn.Conv2d(in_channels, num_channels, kernel_size=kernel_size, stride=stride, padding=padding, bias=True)
        # MLPConv层
        self.mlpconv = MLPConv(num_channels, num_channels // 2, num_channels)





    def forward(self, x):
        # 通过标准的卷积层
        x = self.conv(x)
        # 通过MLPConv层
        x = self.mlpconv(x)
        return x






#7.Network in Network模型
class NiN(torch.nn.Module):
    """
    Network in Network模型
    输入图片大小为224x224
    """

    def __init__(self, num_classes=10):
        super(NiN, self).__init__()
        # 初始卷积层
        self.features = torch.nn.Sequential(
            NiNBlock(3, 96, kernel_size=11, stride=4, padding=0),  # 使用较大的卷积核和步长来减少空间维度
            torch.nn.MaxPool2d(kernel_size=3, stride=2),  # 最大池化层
            NiNBlock(96, 256, kernel_size=5, stride=1, padding=2),
            torch.nn.MaxPool2d(kernel_size=3, stride=2),
            NiNBlock(256, 384, kernel_size=3, stride=1, padding=1),
            torch.nn.MaxPool2d(kernel_size=3, stride=2),
            torch.nn.Dropout(p=0.5),  # 引入Dropout层防止过拟合
            NiNBlock(384, num_classes, kernel_size=3, stride=1, padding=1),
            # 使用全局平均池化替代全连接层
            torch.nn.AdaptiveAvgPool2d((1, 1)),
            torch.nn.Flatten()
        )

    def forward(self, x):
        # 通过特征提取层
        x = self.features(x)
        return x
















