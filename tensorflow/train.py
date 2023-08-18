# -*- coding: utf-8 -*-
"""
模型训练
"""
import pandas as pd
import lstm as lstm
import tensorflow as tf
import json
import pickle
import numpy as np
from keras.preprocessing import sequence
import sklearn
from sklearn.model_selection import train_test_split

# 测试GPU是否可用
print(tf.config.list_physical_devices('GPU'))

# 数据集路径
DATA_FILE = 'data/data.csv'

# 训练轮数
EPOCH = 1
# 批次大小
BATCH_SIZE = 256*50


def load_data():
    """
    加载数据集
    """
    print("正在加载数据集...")
    data = pd.read_csv(DATA_FILE, names=['domain', 'label'])
    domains = data['domain']
    labels = data['label']
    print("数据集加载完成：", len(domains))
    return domains, labels


def train_model(X, labels, max_epoch, batch_size):
    """
    训练lstm模型
    X: 域名列表
    labels：标签列表
    max_epoch：训练伦茨
    batch_size：批处理大小
    """
    # 生成字符编码表
    valid_chars = {x: idx + 1 for idx, x in enumerate(set(''.join(X)))}

    # 最大特征数 = 字符编码表长度+1
    max_features = len(valid_chars) + 1
    # 获取数据集中最大数据长度
    maxlen = np.max([len(x) for x in X])

    print("maxlen:", maxlen)

    # 将数据转换为序列
    X = [[valid_chars[y] for y in x] for x in X]
    # 添加padding，统一数据维度
    X = sequence.pad_sequences(X, maxlen=maxlen)

    # 将标签转换为0/1，正常域名：0，DGA：1
    y = [0 if x == 'benign' else 1 for x in labels]

    # 保存字符编码表
    with open('save/valid_chars.pkl', 'wb') as f:
        pickle.dump(valid_chars, f)
        print("valid_chars.pkl 保存成功！")

    # 划分训练集和测试集，比例8：2，同时打乱顺序
    X_train, X_test, y_train, y_test, _, label_test = train_test_split(X, y, labels, test_size=0.2, shuffle=True)

    print('创建模型...')
    model = lstm.build_model(max_features, maxlen)

    # 从训练集中划分一部分作为验证集，占比5%
    X_train, X_holdout, y_train, y_holdout = train_test_split(X_train, y_train, test_size=0.05)

    # 初始化最佳迭代轮次和最佳auc得分
    best_iter = -1
    best_auc = 0.0

    print("开始训练...")
    for ep in range(max_epoch):
        # 使用训练集训练模型
        model.fit(X_train.tolist(), y_train, batch_size=batch_size, epochs=1)
        # 使用验证集预测
        t_probs = model.predict(X_holdout)
        # 计算验证集AUC得分
        t_auc = sklearn.metrics.roc_auc_score(y_holdout, t_probs)

        print('Epoch %d: auc = %f (best=%f)' % (ep, t_auc, best_auc))

        # 记录最佳AUC得分以及epoch
        if t_auc > best_auc:
            best_auc = t_auc
            best_iter = ep
        else:
            # 如果超过两个epoch性能没有提升，结束训练
            if (ep - best_iter) > 2:
                break

    # 使用测试集计算AUC得分
    probs = model.predict(X_test)
    t_auc = sklearn.metrics.roc_auc_score(y_test, probs)

    print('test: auc = %f' % (t_auc))

    return model


def run():
    # 加载数据集
    domains, labels = load_data()
    # 训练模型
    model = train_model(domains, labels, max_epoch=EPOCH, batch_size=BATCH_SIZE)

    print("正在保存模型...")
    # 保存模型配置->json
    json_string = model.to_json()
    with open('save/lstm.json', 'w') as outfile:
        json.dump(json_string, outfile)
    # 保存模型权重
    model.save_weights('save/lstm.h5')
    print("模型保存成功！ 保存路径：save/lstm.h5")


if __name__ == "__main__":
    run()
