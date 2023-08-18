# -*- coding: utf-8 -*-
"""
模型预测
"""
import pickle
import numpy as np
import tensorflow.keras.preprocessing.sequence as sequence
import json
from keras.models import model_from_json
import warnings
import pymysql

warnings.filterwarnings("ignore")


# 固定随机种子
np.random.seed(1337)

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
                feature.append(-1)
        # 将单个域名转换成的序列加入X存储
        X.append(feature)
    # 把数据填充成定长的序列
    X = sequence.pad_sequences(X, maxlen=max_len)

    print('加载模型配置文件......')
    with open('save/lstm.json', 'r') as f:
        json_string = json.load(f)
    model = model_from_json(json_string)
    print('加载模型权重......')
    model.load_weights('save/lstm.h5')
    # 编译模型
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # 预测
    result = model.predict(X)

    # 大于 0.5 --> DGA，否则正常域名
    return result > 0.5

def load_data_from_mysql():
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
    # # 从mysql查询域名列表
    # domains = load_data_from_mysql()
    # print("域名列表：", domains)
    #
    # # 预测结果
    # results = lstm_predict(domains)
    # # print(results)
    #
    # for domain, predict in zip(domains, results):
    #     print(f"域名：{domain}\t是否是DGA：{'是' if predict[0] else '否'}")


    # 从文件中加载测试数据
    dgas = []
    with open('dga.txt') as f:
        for line in f.readlines():
            dgas.append(line.split(",")[0].strip())
    result = lstm_predict(dgas)
    total = len(result)
    accuracy = 0
    for res in result:
        if res > 0.5:
            accuracy += 1
    print(total, accuracy, accuracy / total)

    while True:
        print(lstm_predict([input(">> ")]))
