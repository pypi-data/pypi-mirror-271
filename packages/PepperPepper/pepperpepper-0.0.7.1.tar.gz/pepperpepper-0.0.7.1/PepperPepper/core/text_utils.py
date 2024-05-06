from ..environment import torch
from ..environment import collections

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

        def count_corpus(tokens):
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


