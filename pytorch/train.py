import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
from utils import DomainDataset, LSTMModel

# 数据集路径
DATA_FILE = 'data/test.csv'

# 训练轮数
EPOCHS = 50
# 批次大小
BATCH_SIZE = 256


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


def train_model(X, labels, max_epochs, batch_size):
    """
    训练LSTM模型
    X: 域名列表
    labels：标签列表
    max_epochs：训练轮次
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
    X = [torch.tensor(x) for x in X]
    X = torch.nn.utils.rnn.pad_sequence(X, batch_first=True)

    # 将标签转换为0/1，正常域名：0，DGA：1
    y = [0 if x == 'benign' else 1 for x in labels]

    # 保存字符编码表
    with open('save/valid_chars.pkl', 'wb') as f:
        pickle.dump(valid_chars, f)
        print("valid_chars.pkl 保存成功！")

    # 划分训练集和测试集，比例8：2，同时打乱顺序
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

    # 创建训练集数据加载器
    train_dataset = DomainDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    print('创建模型...')
    model = LSTMModel(max_features)
    # 检测GPU是否可用，可用时使用GPU训练
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 将模型和测试集数据存入指定设备
    model.to(device)
    X_test = X_test.to(device)
    # 使用交叉熵损失函数
    criterion = nn.BCELoss()
    # 使用Adam优化器
    optimizer = torch.optim.Adam(model.parameters())

    # 初始化最佳迭代轮次和最佳auc得分
    best_iter = -1
    best_auc = 0.0

    print("开始训练...")
    for epoch in range(max_epochs):
        # 模型切换到训练模式，正常使用norm层和dropout层
        model.train()
        # 初始化训练损失
        train_loss = 0.0
        # 进度条，显示训练状态
        progress_bar = tqdm(train_loader, desc=f'Epoch {epoch + 1}/{max_epochs}', unit='batch')
        for domains, labels in progress_bar:
            # 将训练数据存放指定设备
            domains = domains.to(device)
            labels = labels.float().to(device)
            # 清空梯度
            optimizer.zero_grad()
            # 模型训练输出结果
            outputs = model(domains)
            # 计算loss
            loss = criterion(outputs.squeeze(), labels)
            # 反向传播计算梯度
            loss.backward()
            # 更新梯度
            optimizer.step()
            # 计算累计的训练损失
            train_loss += loss.item() * domains.size(0)
            # 更新进度条
            progress_bar.set_postfix(
                {'训练损失': train_loss / ((len(progress_bar) - 1) * train_loader.batch_size + domains.size(0))})

        # 使用验证集预测
        model.eval()
        with torch.no_grad():
            auc = 0.0
            # 进度条
            test_progress_bar = tqdm(range(0, len(X_test), batch_size), desc=f'Test {epoch + 1}', unit='batch')
            for i, batch_index in enumerate(test_progress_bar):
                # 取一个批次的数据
                batch = X_test[batch_index:batch_index + batch_size]
                # 模型预测
                val_outputs = model(batch)
                # 提取预测结果
                val_probs = val_outputs.squeeze().cpu().detach().numpy()
                # 计算AUC得分
                auc += roc_auc_score(y_test[batch_index:batch_index + batch_size], val_probs)
                # 多个批次AUC取均值
                ave_auc = auc / (i + 1)
                # 更新进度条
                test_progress_bar.set_postfix({'AUC': ave_auc})

        print('\nEpoch %d: auc = %f (best=%f)' % (epoch + 1, ave_auc, best_auc))

        # 记录最佳AUC得分以及epoch
        if ave_auc > best_auc:
            best_auc = ave_auc
            best_iter = epoch
        else:
            # 如果超过两轮性能没有提升，结束训练
            if (epoch - best_iter) > 2:
                break

    return model


def run():
    # 加载数据集
    domains, labels = load_data()
    # 训练模型
    model = train_model(domains, labels, max_epochs=EPOCHS, batch_size=BATCH_SIZE)

    print("正在保存模型...")
    torch.save(model.state_dict(), 'save/lstm.pth')
    print("模型保存成功！ 保存路径：save/lstm.pth")


if __name__ == "__main__":
    run()
