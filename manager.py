"""
manager.py
"""
import tomllib
from collections import deque
from pathlib import Path

from data import *


class Manager:
    """逻辑处理类
    """

    def __init__(self):
        self.symlink_path = Path("./data/symlinks.toml")
        self.url_path = Path("./data/urls.toml")
        self.script_path = Path("./data/scripts.toml")
        self.shortcut_path = Path("./data/shortcuts.toml")

        def ensure_file(path: Path):
            """
            确保文件存在，如果不存在则创建
            :param path: 文件路径
            :return:
            """
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()

        ensure_file(self.symlink_path)
        ensure_file(self.url_path)
        ensure_file(self.script_path)
        ensure_file(self.shortcut_path)

        with self.symlink_path.open("rb") as f:
            self.symlink_dict = {k: Symlink(**v) for k, v in tomllib.load(f).items()}
        with self.url_path.open("rb") as f:
            self.url_dict = {k: Url(**v) for k, v in tomllib.load(f).items()}
        with self.script_path.open("rb") as f:
            self.script_dict = {k: Script(**v) for k, v in tomllib.load(f).items()}
        with self.shortcut_path.open("rb") as f:
            self.shortcut_dict = {k: Shortcut(**v) for k, v in tomllib.load(f).items()}

        self.file_path = Path.home()
        self.dir_items: list[Path] = []
        self.path_update_callback = None

        self.info_list = deque(maxlen=20)
        self.info_update_callback = None

        self.selected_index = 0
        self.roll_bar_callback = None
        self.preview_update_callback = None

        self.command_map = {
            "cd": lambda path: self.change_path(path),
        }

    def add_info(self, info: str):
        """
        添加提示信息
        信息队列已满时(长度为20) 会自动删除最早的提示信息
        :param info: 提示信息
        :return:
        """
        self.info_list.append(info)
        self.info_update_callback(self.info_list)

    def change_path(self, path: str):
        """
        改变当前路径
        :param path: 路径字符串 可以是相对路径或绝对路径
        """
        path = Path(path)
        # 如果是相对路径，转换为绝对路径
        if not path.is_absolute():
            path = self.file_path / path
            path = path.resolve()
        if path.exists() and path.is_dir():
            self.file_path = path
        else:
            self.add_info("路径不存在或不是目录")
            return
        self.dir_items = list(path.iterdir())
        # 将文件夹排在前面
        self.dir_items.sort(key=lambda x: (x.is_file(), x.name.lower()))
        # 重置选中项
        self.selected_index = 0
        # 调用回调函数
        item_list = [(item.name, item.is_dir()) for item in self.dir_items]
        self.path_update_callback(str(self.file_path), item_list)
        self.preview_update_callback(self.get_preview_content())

    def select_previous(self, _event=None):
        """
        选择上一个文件
        :param _event: 事件对象
        """
        if len(self.dir_items) == 0:
            return
        if self.selected_index > 0:
            self.selected_index -= 1
        else:
            self.selected_index = len(self.dir_items) - 1
        # 调用回调函数
        self.roll_bar_callback(self.selected_index)
        self.preview_update_callback(self.get_preview_content())

    def select_next(self, _event=None):
        """
        选择下一个文件
        :param _event: 事件对象
        """
        if len(self.dir_items) == 0:
            return
        if self.selected_index < len(self.dir_items) - 1:
            self.selected_index += 1
        else:
            self.selected_index = 0
        # 调用回调函数
        self.roll_bar_callback(self.selected_index)
        self.preview_update_callback(self.get_preview_content())

    def get_preview_content(self) -> str:
        """
        获取预览内容
        :return: 预览文本
        """
        preview_item = self.dir_items[self.selected_index]
        if preview_item.is_file():
            if preview_item.stat().st_size >= 1024 * 100:
                return "文件过大，无法预览"
            if b'\x00' in preview_item.read_bytes()[:1024]:
                return "该文件无法预览"
            try:
                with preview_item.open(encoding="utf-8") as f:
                    content = f.read()
                    return content
            except UnicodeDecodeError as _e:
                return "该文件无法预览"
        else:
            return "无法预览文件夹"

    def parse_command(self, command: str):
        """
        解析命令
        :param command: 命令字符串
        :return:
        """
        command = command.strip().split(" ")
        func = command[0]
        args = command[1:]
        if func in self.command_map:
            try:
                self.command_map[func](*args)
            except TypeError as e:
                self.add_info(f"参数错误: {e}")
        else:
            self.add_info("未知命令")
