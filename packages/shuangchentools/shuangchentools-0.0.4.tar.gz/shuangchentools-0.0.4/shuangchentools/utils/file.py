"""
@Author: shuangchen
@Time: 2024/4/24
@File: file.py
@Description: 文件以及文件夹常用操作
"""
import os
import shutil


def clear_directory(directory: str, sub_directory: bool = True) -> None:
    """
    清除指定文件夹下所有文件，文件夹可选
    :param directory: 要清除其内容的文件夹路径
    :param sub_directory: 是否清除子文件夹
    """
    if sub_directory:
        shutil.rmtree(sub_directory)
    else:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
