"""
@Author: shuangchen
@Time: 2024/5/5
@File: command.py
@Description: 异步执行多个外部命令/程序
"""

import asyncio
from typing import Optional
from dataclasses import dataclass


@dataclass
class Command:
    """
    exe_path: 命令/程序的路径
    log_path: 日志文件的路径
    args: 传递给命令/程序的命令行参数列表，默认为None
    """
    exe_path: str
    log_path: str
    args: Optional[list[str]] = None


async def __run_cpp_program(command: Command):
    """
    异步运行程序
    :param command: 命令/程序
    """
    exec_command = [command.exe_path]
    if command.args is not None:
        exec_command.extend(command.args)

    with open(command.log_path, 'w') as log:
        process = await asyncio.create_subprocess_exec(
            *exec_command,
            stdout=log,
            stderr=log,
        )
        await process.wait()


async def __main(commands: list[Command]):
    tasks = []
    for command in range(commands):
        tasks.append(asyncio.create_task(__run_cpp_program(command)))
    await asyncio.gather(*tasks)


def run(commands: list[Command]):
    asyncio.run(__main(commands))
