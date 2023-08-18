import pickle
import pandas as pd
from tqdm import tqdm


def convert_tmp():
    new_data = []
    with open("old_data.txt") as f:
        for line in tqdm(f.readlines()):
            new_line = line
            if "],charbot" in line:
                line = line.replace("[", "").replace("]", "").replace("'", "")
                line = line.split(",")
                assert len(line) == 4 and line[3] == 'charbot\n'
                new_line = line[1] + ',' + line[3]
                print(new_line)
            new_data.append(new_line)

    with open("data.csv", 'w') as f:
        f.writelines(new_data)

    return new_data


# 分割数据 -> 正常域名和DGA
def split_benign_and_dga(filename="data.csv"):
    benigns = []
    dgas = []
    with open(filename) as f:
        for line in f.readlines():
            if ',benign' in line:
                benigns.append(line.strip() + "\n")
            else:
                dgas.append(line.strip() + "\n")
    print(len(benigns), len(dgas))
    with open("benign.csv", 'w') as f:
        f.writelines(benigns)
    with open("dga.csv", 'w') as f:
        f.writelines(dgas)
    print("ok")

# 去除部分行前面的空格
def format_csv(filename="old_data.csv", outpath="data.csv"):
    datas = []
    with open(filename) as f:
        for line in f.readlines():
            datas.append(line.strip() + "\n")
    with open(outpath, 'w') as f:
        f.writelines(datas)
    print("ok")


# 将csv格式数据集转换成pkl格式
def data2pkl(filename="data.csv", outpath="../traindata.pkl"):
    data = pd.read_csv(filename, names=['domain', 'label'])
    domains = data['domain']
    labels = data['label']
    pickle.dump(zip(labels, domains), open(outpath, 'wb'))
    print("ok")

def add_data(add_file_list, source_path="data.csv"):
    """
    add_file_list: 需要添加的文件列表。每个item是一个元组，第一个元素：文件名，第二个元素：标签名
    """
    with open(source_path) as f:
        datas = f.readlines()
    print(len(datas))
    for file in add_file_list:
        with open(file[0]) as f:
            for line in f.readlines():
                datas.append(line.split(",")[0].strip() + ',' + file[1] + '\n')
    print(len(datas))
    with open(source_path, 'w') as f:
        f.writelines(datas)


if __name__ == '__main__':
    add_file_list = [('dga.txt', '360dga'), ('DGA1.txt', 'testdga'), ('zeus_dga_domains.txt', 'zeusdga')]
    add_data(add_file_list)

    # split_benign_and_dga(filename=save_path)
