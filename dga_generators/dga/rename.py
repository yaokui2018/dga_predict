import os
import shutil

# 指定原始文件夹路径和目标文件夹路径
original_folder = 'domain_generation_algorithms'  # 替换为原始文件夹的路径
destination_folder = 'out'  # 替换为目标文件夹的路径

# 遍历原始文件夹中的所有子文件夹
for root, dirs, files in os.walk(original_folder):
    for dir_name in dirs:
        # 构建子文件夹的完整路径
        dir_path = os.path.join(root, dir_name)
        print(dir_path)

        # 定义 dga.py 文件的路径
        source_file = os.path.join(dir_path, 'dga.py')

        # 检查 dga.py 文件是否存在
        if os.path.isfile(source_file):
            # 获取子文件夹的名称
            new_name = dir_path.replace('\\', '').replace(original_folder, '')

            # 构建新的 dga.py 文件的路径
            new_file = os.path.join(destination_folder, new_name + '.py')

            # 复制 dga.py 文件到目标文件夹并重命名
            shutil.copy(source_file, new_file)
