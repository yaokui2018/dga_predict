# -*- coding: utf-8 -*-
"""
模型预测
"""
import os
import pickle
import random
import time

import numpy as np
import torch
import warnings

from torch import nn
from tqdm import tqdm

from utils import LSTMModel

warnings.filterwarnings("ignore")

# 固定随机种子
np.random.seed(1337)

batch_size = 256

# 最大embedding长度，由训练训练数据长度确定
max_len = 68


def lstm_predict(inputs):
    """
    模型预测
    inputs: 需要预测的域名列表，list
    """
    with open('save/valid_chars.pkl', 'rb') as f:
        valid_chars = pickle.load(f)

    X = []
    for x in inputs:
        feature = []
        for y in x.strip():
            if y in valid_chars:
                feature.append(valid_chars[y])
            else:
                feature.append(-1)
        X.append(feature)
    X = [torch.tensor(x) for x in X]
    X = torch.nn.utils.rnn.pad_sequence(X, batch_first=True)

    # 对序列进行截断或填充到指定长度
    if X.size(1) < max_len:
        X = nn.functional.pad(X, (0, max_len - X.size(1)), value=0)
    elif X.size(1) > max_len:
        X = X[:, :max_len]

    model = LSTMModel(len(valid_chars) + 1)
    model.load_state_dict(torch.load('save/lstm.pth'))
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    X = X.to(device)

    outputs = model(X)
    results = outputs.squeeze().cpu().detach().numpy()
    # print(results)

    return results


if __name__ == '__main__':
    domains = []
    labels = []
    # with open('data/data.csv') as f:
    #     for line in f.readlines():
    #         domains.append(line.split(",")[0].strip())
    #         labels.append(0 if line.split(",")[1].strip() == 'benign' else 1)
    with open('dga.txt') as f:
        for line in f.readlines()[:1000000]:
            domains.append(line.split(",")[0].strip())
            labels.append(1)
    time_start = time.time()
    test_progress_bar = tqdm(range(0, len(domains), batch_size), desc=f'Test', unit='batch')
    result = []
    for i, batch_index in enumerate(test_progress_bar):
        batch = domains[batch_index:batch_index + batch_size]
        outputs = lstm_predict(batch)
        result.extend(outputs)
    time_end = time.time()

    print(len(result), time_end - time_start)

    total = len(result)
    benign_ok_count = 0
    dga_ok_count = 0
    benign_error_count = 0
    dag_error_count = 0
    for res, label, domain in zip(result, labels, domains):
        if res > 0.5 and label == 1:
            dga_ok_count += 1
        elif res <= 0.5 and label == 0:
            benign_ok_count += 1
        else:
            if label == 0:
                benign_error_count += 1
            else:
                dag_error_count += 1
            # print(domain, label, res)
    accuracy = dga_ok_count + benign_ok_count
    print(total, accuracy, accuracy / total)
    print("err ", benign_error_count, dag_error_count)
    print("ok ", benign_ok_count, dga_ok_count)

    while True:
        # print(lstm_predict([input(">> "), 'goog1212120le.com']))
        result = lstm_predict(input(">>> ").split(","))
        print(result, result > 0.5)
