from ..environment import np, pd, plt,torch




"""
1.LeNet
abstract:
        LeNet5是一个经典的卷积神经网络，由多个卷积层、池化层和全连接层组成。它通过卷积操作提取图像中的局部特征，利用池化层进行特征下采样，并通过全连接层进行分类。LeNet最初用于手写数字识别任务，并展现出了良好的性能。其结构简洁明了，为后续更复杂的神经网络结构提供了基础，对深度学习领域的发展产生了重要影响。

struct:
        卷积编码器：由两个卷积层组成;
        全连接层密集块：由三个全连接层组成。

input: 
        28*28的单通道（黑白）图像通过LeNet,in_channels×28×28。

output: 
        最后一层输出为10的Linear层，分别代表十种数字的类别数。

"""
class LeNet5(torch.nn.Module):
    def __init__(self,in_channels=3 ,num_classes=10):
        super(LeNet5, self).__init__()
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, 6, 5, padding=2), # 输入通道数为in_channels，输出通道数为6，卷积核大小为5
            torch.nn.BatchNorm2d(6),
            torch.nn.Sigmoid(),
            torch.nn.AvgPool2d(kernel_size=2, stride=2), # 池化窗口2x2，步长2
            torch.nn.Conv2d(6, 16, 5), # 输入通道6，输出通道16，卷积核5x5
            torch.nn.BatchNorm2d(16),
            torch.nn.Sigmoid(),
            torch.nn.AvgPool2d(kernel_size=2, stride=2), # 池化窗口2x2，步长2
        )

        self.classifier = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(16 * 5 * 5, 120),
            torch.nn.BatchNorm1d(120),
            torch.nn.Sigmoid(),
            torch.nn.Linear(120, 84),
            torch.nn.BatchNorm1d(84),
            torch.nn.Sigmoid(),
            torch.nn.Linear(84, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        #x = x.view(x.size(0), -1)  # 确保这里的展平操作是正确的
        x = self.classifier(x)
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
        输入图像的大小是 in_channelsx224x224（AlexNet 的原始输入大小）。

output: 
        num_classes 参数用于指定分类的类别数，你可以根据你的任务需求进行修改。
"""
# 定义AlexNet模型类，继承自nn.Module
class AlexNet(torch.nn.Module):
    # 初始化函数，用于设置网络层
    def __init__(self, in_channels=3, num_classes=1000):
        super(AlexNet,self).__init__()  # 调用父类nn.Module的初始化函数

        # 定义特征提取部分
        self.features = torch.nn.Sequential(
            # 第一个卷积层，输入通道3（RGB），输出通道64，卷积核大小11x11，步长4，填充2
            torch.nn.Conv2d(in_channels, 64, kernel_size=11, stride=4, padding=2),
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
    def __init__(self, in_channels=3, num_classes=1000):
        """
        VGG16模型

        参数:
            num_classes (int, 可选): 分类的数量。默认为1000
        """
        super(VGG16, self).__init__()

        # 定义特征提取部分
        self.features = torch.nn.Sequential(
            VGGBlock(in_channels, 64, 2, pool=True),  # block1: 64 channels, 2 conv layers, maxpool
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
    def __init__(self, in_channels, num_channels , kernel_size=3, stride=1, padding=1):
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

    def __init__(self, in_channels=3, num_classes=10):
        super(NiN, self).__init__()
        # 初始卷积层
        self.features = torch.nn.Sequential(
            NiNBlock(in_channels, 96, kernel_size=11, stride=4, padding=0),  # 使用较大的卷积核和步长来减少空间维度
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










#8.InceptionBlock块v1版本
"""
简介：Inception块v1版本，也称为Inception-v1，是GoogLeNet网络中的一个核心组成部分，由Google团队在2014年提出。Inception-v1的主要特点是使用多尺度的卷积操作来捕捉图像中不同层次的特征。为了实现这一目标，Inception-v1引入了称为“Inception模块”的基本构建块。一个典型的Inception模块由四个并行的卷积分支组成，每个分支执行不同尺度的卷积操作。这些分支的输出在通道维度上进行拼接，形成模块的最终输出。
结构：
1x1卷积分支：使用1x1的卷积核对输入进行卷积，这种卷积方式可以减少神经网络的参数量，并压缩通道数，提高计算效率。
3x3卷积分支：使用3x3的卷积核对输入进行卷积，以捕获局部特征。
5x5卷积分支：使用5x5的卷积核对输入进行卷积，以捕获更大范围的特征。但是，直接使用5x5的卷积核会导致计算量较大，因此在实际实现中，可能会使用两个3x3的卷积层来替代。
最大池化分支：使用3x3的最大池化层对输入进行下采样，然后使用1x1的卷积层来改变通道数。这个分支的目的是捕获更抽象的特征。
"""
class InceptionBlockV1(torch.nn.Module):
    def __init__(self,
                 in_channels,   # 输入到Inception块的通道数
                 ch1,           # 路径1：1x1卷积分支的输出通道数
                 ch2,           # 路径2：ch2[0]为3x3卷积分支的第一个1x1卷积的输出通道数（用于降维），ch2[1]为3x3卷积分支的3x3卷积的输出通道数
                 ch3,           # 路径3：ch3[0]为5x5卷积分支的第一个1x1卷积的输出通道数（用于降维），ch3[1]5x5卷积分支的5x5卷积的输出通道数
                 ch4):          # 最大池化分支的1x1卷积的输出通道数（用于降维后投影到同一通道数）
        super(InceptionBlockV1,self).__init__()

        # 路径1，单1x1卷积层，直接对输入进行1x1卷积
        self.brach1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, ch1, kernel_size=1),
            torch.nn.ReLU(inplace=True)
        )



        # 路径2，1x1卷积 -> 3x3卷积分支，先进行1x1卷积降维，再进行3x3卷积
        self.brach2 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, ch2[0], kernel_size=1),      # 输入in_channels, 输出ch3x3red
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(ch2[0], ch2[1], kernel_size=3, padding=1), # 输入ch3x3red, 输出ch3x3
            torch.nn.ReLU(inplace=True)
        )



        # 路径3，1x1卷积 -> 5x5卷积分支
        self.brach3 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, ch3[0], kernel_size=1),      # 输入in_channels, 输出ch5x5red
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(ch3[0], ch3[1], kernel_size=5, padding=2), # 输入ch5x5red, 输出ch5x5
            torch.nn.ReLU(inplace=True)
        )


        # 路径4，3x3最大池化 -> 1x1卷积分支，先进行3x3最大池化，然后进行1x1卷积改变通道数
        self.brach4 = torch.nn.Sequential(
            torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            torch.nn.Conv2d(in_channels, ch4, kernel_size=1),
            torch.nn.ReLU(inplace=True)
        )



    def forward(self, x):
        branch1 = self.brach1(x)
        branch2 = self.brach2(x)
        branch3 = self.brach3(x)
        branch4 = self.brach4(x)

        # 拼接各分支的输出
        outputs = torch.cat((branch1, branch2, branch3, branch4), dim=1)
        return outputs











#9.GoogLeNet的复现
"""
简介：GoogLeNet的设计特点在于既有深度，又在横向上拥有“宽度”，并采用了一种名为Inception的核心子网络结构。这个网络名字中的“GoogLeNet”是对LeNet的致敬，LeNet是早期由Yann LeCun设计的卷积神经网络。
基本结构：
    Inception模块：这是GoogLeNet的核心子网络结构。Inception模块的基本组成结构有四个：1x1卷积、3x3卷积、5x5卷积和3x3最大池化。这四个操作并行进行以提取特征，然后将这四个操作的输出进行通道维度的拼接。这种设计使得网络能够捕捉不同尺度的特征。
    1x1卷积：在Inception模块中，1x1卷积起到了两个主要作用。首先，它可以在相同尺寸的感受野中叠加更多的卷积，从而提取到更丰富的特征。其次，它还可以用于降维，降低计算复杂度。当某个卷积层输入的特征数较多时，对输入先进行降维，减少特征数后再做卷积，可以显著减少计算量。
    辅助分类器：GoogLeNet在网络的不同深度处添加了两个辅助分类器。这些辅助分类器在训练过程中与主分类器一同进行优化，有助于提升整个网络的训练效果。
    全局平均池化：与传统的全连接层相比，全局平均池化能够减少网络参数，降低过拟合风险，并且具有更强的鲁棒性。
"""
class GoogLeNet(torch.nn.Module):
    def __init__(self, in_channels=3, num_classes=1000):
        super(GoogLeNet,self).__init__()


        # 第一个模块:使用64个通道、7x7卷积层。
        self.block1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )


        # 第二个模块:第一层卷积层是64个通道、1x1卷积层；第二个卷积层使用将通道数增加3x的3x3卷积层。
        self.block2 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, kernel_size=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 192, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )


        # 第三个模块：串联两个Inception块。具体操作请看相关论文
        self.block3 = torch.nn.Sequential(
            InceptionBlockV1(192, 64, (96, 128), (16, 32), 32),
            InceptionBlockV1(256, 128, (128, 192), (32, 96), 64),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )



        # 第四个模块：串联了5个Inception块
        self.block4 = torch.nn.Sequential(
            InceptionBlockV1( 480, 192, (96, 208), (16, 48), 64),
            InceptionBlockV1(512, 160, (112, 224), (24, 64), 64),
            InceptionBlockV1(512, 128, (128, 256), (24, 64), 64),
            InceptionBlockV1(512, 112, (114, 288), (32, 64), 64),
            InceptionBlockV1(528, 256, (160, 320), (32, 128), 128),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )


        # 第五个模块： 其中每条路径通道数的分配思路和第三、第四模块中的一致，只是在具体数值上有所不同。 需要注意的是，第五模块的后面紧跟输出层，该模块同NiN一样使用全局平均汇聚层，将每个通道的高和宽变成1。 最后我们将输出变成二维数组，再接上一个输出个数为标签类别数的全连接层。
        self.block5 = torch.nn.Sequential(
            InceptionBlockV1(832, 256, (160, 320), (32, 128), 128),
            InceptionBlockV1(832, 384, (192, 384), (48,128), 128),
            torch.nn.AdaptiveAvgPool2d((1, 1)),
            torch.nn.Flatten()
        )

        self.features = torch.nn.Sequential(self.block1, self.block2, self.block3, self.block4, self.block5)

        # 分类器（全连接层）
        self.classifier = torch.nn.Linear(1024, num_classes)





    def forward(self, x):
        # 前向传播：通过特征提取层
        x = self.features(x)

        # 展平特征图，准备进行全连接层
        x = self.classifier(x)

        # 输出分类结果
        return x

