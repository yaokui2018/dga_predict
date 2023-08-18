# 遍历原始文件夹中的所有子文件夹
import os

names = []
for root, dirs, files in os.walk("../out"):
    for file_name in files:
        if ".py" in file_name:
            names.append(file_name.replace(".py", ""))
        print(file_name)
print(names)