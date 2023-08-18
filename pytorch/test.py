# -*- coding: utf-8 -*-
"""
模型预测
"""
import pickle
import numpy as np
import pymysql
import torch
from torch import nn
import warnings

from typing import List

from utils import LSTMModel

warnings.filterwarnings("ignore")

# 固定随机种子
np.random.seed(1337)

# 批处理大小
batch_size = 256
# 最大embedding长度，由训练训练数据长度确定
max_len = 68


def lstm_predict(inputs):
    """
    模型预测
    inputs: 需要预测的域名列表，list
    """
    # 加载valid_chars：字符编码表，在训练时产生
    with open('save/valid_chars.pkl', 'rb') as f:
        valid_chars = pickle.load(f)

    # 将输入数据转换为序列
    X = []
    # 遍历输入数据列表
    for x in inputs:
        feature = []
        # 遍历单个域名，获取每个字符
        for y in x.strip():
            if y in valid_chars:
                # 如果该字符存在字符编码表中，直接使用编码表中的序号
                feature.append(valid_chars[y])
            else:
                # 否则，用-1填充
                feature.append(0)
        # 将单个域名转换成的序列加入X存储
        X.append(feature)
    # 将数据转换为tensor
    X = [torch.tensor(x) for x in X]
    # 把数据填充成定长的序列
    X = torch.nn.utils.rnn.pad_sequence(X, batch_first=True)
    # 对序列进行截断或填充到指定长度
    if X.size(1) < max_len:
        X = nn.functional.pad(X, (0, max_len - X.size(1)), value=0)
    elif X.size(1) > max_len:
        X = X[:, :max_len]

    # 初始化LSTM模型
    model = LSTMModel(len(valid_chars) + 1)
    # 检测GPU可用性
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    X = X.to(device)
    # 加载模型权重
    model.load_state_dict(torch.load('save/lstm.pth', map_location=device))
    # 模型调成预测模式，禁用norm层和Dropout层
    model.eval()
    # 预测
    outputs = model(X)
    # 提取预测结果
    results = outputs.squeeze().cpu().detach().numpy()

    # 大于 0.5 --> DGA，否则正常域名
    return results > 0.5


def load_data_from_mysql() -> List[str]:
    # 建立数据库连接
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1',
        database='dga_test'
    )
    # 创建游标对象
    cursor = conn.cursor()
    # 查询10条domain
    query = "SELECT domain FROM dga LIMIT 10"
    cursor.execute(query)
    # 提取数据
    result = cursor.fetchall()
    # 提取域名列表
    domain_list = [row[0] for row in result]
    # 关闭游标和连接
    cursor.close()
    conn.close()

    return domain_list


if __name__ == '__main__':
    # 从mysql查询域名列表
    domains = load_data_from_mysql()
    print("域名列表：", domains)

    # 预测结果
    results = lstm_predict(domains)

    for domain, predict in zip(domains, results):
        print(f"域名：{domain}\t是否是DGA：{'是' if predict else '否'}")
