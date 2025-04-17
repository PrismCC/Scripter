"""
    包含四种数据类Symlink, Script, Url 和 Shortcut
"""

from dataclasses import dataclass


@dataclass
class Symlink:
    """
        符号链接类
        path: 链接指向的路径
    """
    path: str


@dataclass
class Script:
    """
        脚本类
        path: 脚本路径
    """
    path: str


@dataclass
class Url:
    """
        Url类
        urls: url数组
    """
    urls: list[str]


@dataclass
class Shortcut:
    """
        快捷方式类
        command: 命令内容
    """
    command: str
