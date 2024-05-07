from ..environment import torch
from ..environment import collections
from ..environment import random

"""
1.tokenize(lines, token='word')
简述：
tokenize函数将文本行列表（lines）作为输入， 列表中的每个元素是一个文本序列（如一条文本行）。
每个文本序列又被拆分成一个词元列表，词元（token）是文本的基本单位。
最后，返回一个由词元列表组成的列表，其中的每个词元都是一个字符串（string）。
"""
def tokenize(lines, token='word'):
    """将文本行拆分为单词或字符词元"""
    if token == 'word':
        return [line.split() for line in lines]
    elif token == 'char':
        return [list(line) for line in lines]
    else:
        print('错误：未知词元类型：' + token)





"""
2.Vocab
文本词表(vocabulary)
初始化词表对象。

Parameters:
        tokens (list): 用于构建词表的词元列表，默认为 None。
        min_freq (int): 词频阈值，低于该频率的词元将被过滤，默认为 0。
        reserved_tokens (list): 预留的特殊词元列表，默认为 None。

Attributes:
        _token_freqs (list): 按词频降序排列的词元及其频率的列表。
        idx_to_token (list): 索引到词元的映射列表。
        token_to_idx (dict): 词元到索引的映射字典。
"""
class Vocab:

    def __init__(self, tokens=None, min_freq=0, reserved_tokens=None):
        if tokens is None:
            tokens = []
        if reserved_tokens is None:
            reserved_tokens = []


        # 统计词元的频率
        counter = self.count_corpus(tokens)

        # 按出现频率排序
        self._token_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)

        # 初始化索引到词元的映射列表，加入预留词元 "<unk>"
        self.idx_to_token = ['<unk>'] + reserved_tokens

        # 初始化词元到索引的映射字典
        self.token_to_idx = {token: idx for idx, token in enumerate(self.idx_to_token)}

        # 将词频大于 min_freq 的词元添加到词表中
        for token, freq in self._token_freqs:
            if freq < min_freq:
                break
            if token not in self.token_to_idx:
                self.idx_to_token.append(token)
                self.token_to_idx[token] = len(self.idx_to_token) - 1

    def __len__(self):
        """返回词表中的词元数量"""
        return len(self.idx_to_token)

    def __getitem__(self, tokens):
        """
        返回给定词元的索引。

        Parameters:
            tokens (str or list): 单个词元或词元列表。

        Returns:
            idx (int or list): 词元对应的索引或索引列表。
        """
        # 如果 tokens 是单个词元，返回其索引；如果是词元列表，则返回对应的索引列表
        if not isinstance(tokens, (list, tuple)):
            return self.token_to_idx.get(tokens, self.unk)
        return [self.__getitem__(token) for token in tokens]

    def to_tokens(self, indices):
        """
        返回给定索引对应的词元。

        Parameters:
            indices (int or list): 单个索引或索引列表。

        Returns:
            tokens (str or list): 索引对应的词元或词元列表。
        """
        # 如果 indices 是单个索引，返回对应的词元；如果是索引列表，则返回对应的词元列表
        if not isinstance(indices, (list, tuple)):
            return self.idx_to_token[indices]
        return [self.idx_to_token[index] for index in indices]

    @property
    def unk(self):
        """返回未知词元的索引"""
        return 0

    @property
    def token_freqs(self):
        """返回词元及其频率的列表"""
        return self._token_freqs

    def count_corpus(self, tokens):  # 改为实例方法
        """
        统计词元的频率。

        Parameters:
            tokens (list): 用于统计的词元列表，可以是一维或二维列表。

        Returns:
            counter (collections.Counter): 词元及其频率的计数器。
        """
        # 如果 tokens 是二维列表，将其展平成一维列表
        if len(tokens) == 0 or isinstance(tokens[0], list):
            tokens = [token for line in tokens for token in line]

        # 统计词元的频率并返回计数器
        return collections.Counter(tokens)



"""  
3.seq_data_iter_random(corpus, batch_size, num_steps)
    使用随机抽样生成一个小批量子序列  

    参数:  
        corpus (list): 文本语料库，一个字符列表  
        batch_size (int): 每个小批量的样本数量  
        num_steps (int): 每个子序列的长度  

    返回:  
        生成器: 产生包含输入X和标签Y的小批量数据  
"""
def seq_data_iter_random(corpus, batch_size, num_steps):
    """使用随机抽样生成一个小批量子序列"""
    # 从随机偏移量开始对序列进行分区，随机范围包括num_steps-1
    corpus = corpus[random.randint(0, num_steps - 1):]

    # 减去1，是因为我们需要考虑标签
    num_subseqs = (len(corpus) - 1) // num_steps

    # 长度为num_steps的子序列的起始索引
    initial_indices = list(range(0, num_subseqs * num_steps, num_steps))

    # 在随机抽样的迭代过程中，
    # 来自两个相邻的、随机的、小批量中的子序列不一定在原始序列上相邻
    random.shuffle(initial_indices)


    def data(pos):
        # 返回从pos位置开始的长度为num_steps的序列
        return corpus[pos: pos + num_steps]


    num_batches = num_subseqs // batch_size
    for i in range(0, batch_size * num_batches, batch_size):
        # 在这里，initial_indices包含子序列的随机起始索引
        initial_indices_per_batch = initial_indices[i: i + batch_size]
        X = [data(j) for j in initial_indices_per_batch]
        Y = [data(j + 1) for j in initial_indices_per_batch]
        yield torch.tensor(X), torch.tensor(Y)














"""  
4.seq_data_iter_random(corpus, batch_size, num_steps)
    顺序抽样生成一个小批量子序列  

    参数:  
        corpus (list): 文本语料库，一个字符列表  
        batch_size (int): 每个小批量的样本数量  
        num_steps (int): 每个子序列的长度  

    返回:  
        生成器: 产生包含输入X和标签Y的小批量数据  
"""
def seq_data_iter_sequential(corpus, batch_size, num_steps):
    """使用顺序分区生成一个小批量子序列"""
    # 从随机偏移量开始划分序列
    offset = random.randint(0, num_steps)
    num_tokens = ((len(corpus) - offset - 1) // batch_size) * batch_size
    Xs = torch.tensor(corpus[offset: offset + num_tokens])
    Ys = torch.tensor(corpus[offset + 1: offset + 1 + num_tokens])
    Xs, Ys = Xs.reshape(batch_size, -1), Ys.reshape(batch_size, -1)
    num_batches = Xs.shape[1] // num_steps
    for i in range(0, num_steps * num_batches, num_steps):
        X = Xs[:, i: i + num_steps]
        Y = Ys[:, i: i + num_steps]
        yield X, Y
















# 5.SeqDataLoader
class SeqDataLoader:  # @save
    """
    加载序列数据的迭代器。
    这个类提供了两种加载序列数据的方式：随机抽样（seq_data_iter_random）和顺序抽取（seq_data_iter_sequential）。
    """

    def __init__(self, lines, token,batch_size, num_steps, use_random_iter, max_tokens):
        """
        初始化序列数据加载器。

        参数:
        - batch_size (int): 每个小批量的样本数量。
        - num_steps (int): 每个子序列的长度。
        - use_random_iter (bool): 是否使用随机抽样来生成子序列。
        - max_tokens (int): 加载语料库时使用的最大令牌数量。

        属性:
        - data_iter_fn (callable): 根据use_random_iter的值，选择随机或顺序的迭代函数。
        - corpus (list): 文本语料库，一个字符列表。
        - vocab (d2l.Vocab): 词汇表对象，用于将字符映射到索引。
        - batch_size (int): 每个小批量的样本数量。
        - num_steps (int): 每个子序列的长度。
        """
        if use_random_iter:
            # 如果use_random_iter为True，则使用随机抽样的迭代函数
            self.data_iter_fn = seq_data_iter_random
        else:
            # 否则，使用顺序抽取的迭代函数
            self.data_iter_fn = seq_data_iter_sequential

            # 加载语料库并限制最大令牌数量，同时获取词汇表对象
        tokens = tokenize(lines, token)
        self.vocab = Vocab(tokens)
        self.corpus = [self.vocab[token] for line in tokens for token in line]
        if max_tokens>0:
            self.corpus = self.corpus[:max_tokens]



        # 保存批大小和子序列长度
        self.batch_size, self.num_steps = batch_size, num_steps

    def __iter__(self):
        """
        实现迭代器协议，返回一个迭代器，该迭代器生成小批量数据。

        返回:
        - generator: 一个生成器，产生包含输入X和标签Y的小批量数据。
        """
        # 使用选定的迭代函数（随机或顺序）生成数据
        return self.data_iter_fn(self.corpus, self.batch_size, self.num_steps)

































