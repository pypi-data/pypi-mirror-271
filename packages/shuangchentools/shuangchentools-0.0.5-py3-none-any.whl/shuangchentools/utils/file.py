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


def read_last_n_lines(filename: str, n: int):
    """
    读取文件最后n行
    :param filename: 文件名
    :param n: 最后n行
    """
    lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.rstrip('\n'))
            if len(lines) > n:
                lines.pop(0)
    lines.reverse()
    return lines


def read_first_n_lines(filename: str, n: int):
    """
    读取文件前n行
    :param filename: 文件名
    :param n: 前n行
    """
    lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            lines.append(line.rstrip('\n'))
            if i + 1 == n:
                break
    return lines
