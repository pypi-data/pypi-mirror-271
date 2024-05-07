from ..environment import torch



'''
1.RNNModel
简述：循环神经网络模型
'''
class RNNModel(torch.nn.Module):
    def __init__(self, rnn_layer, vocab_size, **kwargs):
        super(RNNModel, self).__init__(**kwargs)
        self.rnn = rnn_layer  # 循环神经网络层，可以是nn.RNN、nn.LSTM或nn.GRU
        self.vocab_size = vocab_size  # 词表大小，用于全连接层输出
        self.num_hiddens = self.rnn.hidden_size  # 隐藏单元数，等于循环神经网络层的隐藏单元数

        # 如果RNN是双向的（之后将介绍），num_directions应该是2，否则应该是1
        if not self.rnn.bidirectional:
            self.num_directions = 1
            # 线性层，用于将RNN的输出映射到词表大小的空间上
            self.linear = torch.nn.Linear(self.num_hiddens, self.vocab_size)
        else:
            self.num_directions = 2
            # 如果是双向的RNN，线性层的输入维度是隐藏单元数的两倍
            self.linear = torch.nn.Linear(self.num_hiddens * 2, self.vocab_size)

    def forward(self, inputs, state):
        # 将输入转换为one-hot编码，并转换为浮点型张量
        X = torch.nn.functional.one_hot(inputs.T.long(), self.vocab_size)
        X = X.to(torch.float32)
        # 前向传播过程，获取RNN的输出和新的隐状态
        Y, state = self.rnn(X, state)
        # 全连接层首先将Y的形状改为(时间步数*批量大小,隐藏单元数)
        # 它的输出形状是(时间步数*批量大小,词表大小)。
        output = self.linear(Y.reshape((-1, Y.shape[-1])))
        return output, state

    def begin_state(self, device, batch_size=1):
        if not isinstance(self.rnn, torch.nn.LSTM):
            # nn.GRU以张量作为隐状态
            return  torch.zeros((self.num_directions * self.rnn.num_layers,
                                 batch_size, self.num_hiddens),
                                device=device)
        else:
            # nn.LSTM以元组作为隐状态
            return (torch.zeros((
                self.num_directions * self.rnn.num_layers,
                batch_size, self.num_hiddens), device=device),
                    torch.zeros((
                        self.num_directions * self.rnn.num_layers,
                        batch_size, self.num_hiddens), device=device))