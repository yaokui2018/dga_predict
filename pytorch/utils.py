# -*- coding: utf-8 -*-
# Author: 薄荷你玩
# Date: 2023/08/13

import torch
import torch.nn as nn
from torch.utils.data import Dataset


# 方便数据集中的样本，继承 PyTorch 的 Dataset 类
class DomainDataset(Dataset):
    def __init__(self, domains, labels):
        self.domains = domains
        self.labels = labels

    def __len__(self):
        return len(self.domains)

    def __getitem__(self, idx):
        domain = self.domains[idx]
        label = self.labels[idx]
        return domain, label


# LSTM 模型
class LSTMModel(nn.Module):
    def __init__(self, max_features, hidden_dim=128, num_layers=1, drop_out=0.5):
        super(LSTMModel, self).__init__()
        # embedding 层
        self.embedding = nn.Embedding(max_features, hidden_dim)
        # lstm层
        self.lstm = nn.LSTM(hidden_dim, hidden_dim, batch_first=True, num_layers=num_layers)
        # 丢弃层
        self.dropout = nn.Dropout(drop_out)
        # 全连接层
        self.fc = nn.Linear(hidden_dim, 1)
        # 激活层
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 将输入索引序列转换成embedding向量
        embedded = self.embedding(x)
        # 将embedding向量输入到 LSTM 层中，获取所有时间步的隐藏状态值
        output, _ = self.lstm(embedded)
        # 对隐藏状态值在第一个维上进行求平均
        output = torch.mean(output, dim=1)
        # 对输出进行 Dropout 操作，防止过拟合
        output = self.dropout(output)
        # 将输出输入到全连接层，得到一个标量值
        output = self.fc(output)
        # 将标量值通过 Sigmoid 函数进行压缩，映射到 [0, 1] 范围内，表示概率
        output = self.sigmoid(output)
        return output
