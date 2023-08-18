# -*- coding: utf-8 -*-
"""
 LSTM 模型
"""
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM

def build_model(max_features, maxlen):
    """
    构建LSTM模型
    max_features：特征数
    maxlen：最大输入长度
    """
    # keras序贯模型
    model = Sequential()
    # embedding层
    model.add(Embedding(max_features, 128, input_length=maxlen))
    # LSTM层
    model.add(LSTM(128))
    # Dropout层
    model.add(Dropout(0.5))
    # 全连接层
    model.add(Dense(1))
    # 激活层
    model.add(Activation('sigmoid'))
    # 建立模型
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model

