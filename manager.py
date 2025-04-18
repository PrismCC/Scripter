"""
manager.py
"""
import difflib
import os
import subprocess
import tomllib
from collections import deque
from pathlib import Path

import tomli_w

from data import *
from utils import IndexableDict


class Manager:
    """
    逻辑处理类
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
            self.symlink_dict = IndexableDict({k: Symlink(**v) for k, v in tomllib.load(f).items()})
        with self.url_path.open("rb") as f:
            self.url_dict = IndexableDict({k: Url(**v) for k, v in tomllib.load(f).items()})
        with self.script_path.open("rb") as f:
            self.script_dict = IndexableDict({k: Script(**v) for k, v in tomllib.load(f).items()})
        with self.shortcut_path.open("rb") as f:
            self.shortcut_dict = IndexableDict({k: Shortcut(**v) for k, v in tomllib.load(f).items()})

        self.file_path = Path.home()
        self.dir_items: list[Path] = []
        self.list_update_callback = None

        self.info_list = deque(maxlen=20)
        self.info_update_callback = None

        self.selected_index = 0
        self.list_length = 0
        self.roll_bar_callback = None
        self.preview_update_callback = None

        self.command_map = {
            "cd": lambda path: self.change_path(path),
            "lk": lambda name: self.jump_link(name),
            "sc": lambda name: self.run_script(name),
            "wb": lambda name: self.open_url(name),
            "tab": lambda tab_id: self.switch_tab(tab_id),
            "run": lambda: self.run(),
            "add_lk": lambda name, path: self.add_symlink(name, path),
            "add_sc": lambda name, path: self.add_script(name, path),
            "add_wb": lambda name, url: self.add_url(name, url),
        }

        self.tab = "文件系统"
        self.switch_tab_callback = None

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
        self.list_length = len(self.dir_items)
        # 将文件夹排在前面
        self.dir_items.sort(key=lambda x: (x.is_file(), x.name.lower()))
        if self.tab == "文件系统":
            # 重置选中项
            self.selected_index = 0
            # 调用回调函数
            item_list = [(item.name, 4 if item.is_dir() else 3) for item in self.dir_items]
            self.list_update_callback(str(self.file_path), item_list)
            self.preview_update_callback(self.get_preview_content())

    def jump_link(self, link_name: str):
        """
        将当前路径跳转到链接
        :param link_name: 链接名称
        """
        if link_name in self.symlink_dict:
            link = self.symlink_dict[link_name]
            self.change_path(link.path)
            self.add_info(f"链接 {link_name} 已跳转: {link.path}")
        else:
            self.add_info("链接不存在")

    def run_script(self, script_name: str):
        """
        运行脚本
        :param script_name: 脚本名称
        """
        if script_name in self.script_dict:
            script = self.script_dict[script_name]
            path = Path(script.path)
            if path.exists():
                subprocess.Popen(script.path, shell=True)
                self.add_info(f"脚本 {script_name} 已运行")
            else:
                self.add_info("脚本文件缺失")
        else:
            self.add_info("脚本不存在")

    def open_url(self, url_name: str):
        """
        打开网页
        :param url_name: 网页名称
        """
        if url_name in self.url_dict:
            url = self.url_dict[url_name]
            for link in url.urls:
                os.system(f"start {link}")
                self.add_info(f"网页 {link} 已打开")
        else:
            self.add_info("网页不存在")

    def switch_tab(self, tab_id: str):
        """
        切换标签页
        :param tab_id: 标签页ID
        """
        tabs = ["文件系统", "链接", "脚本", "网页", "快捷键"]
        tab_id = int(tab_id) - 1
        if tab_id < 0 or tab_id >= len(tabs):
            self.add_info("标签页ID错误")
        else:
            self.switch_tab_callback(tabs[tab_id])

    def run(self):
        """
        执行当前所选项
        :return:
        """
        if self.tab == "文件系统":
            if len(self.dir_items) == 0:
                return
            item: Path = self.dir_items[self.selected_index]
            if item.is_dir():
                self.change_path(str(item))
            else:
                os.startfile(str(item))
        elif self.tab == "链接":
            if len(self.symlink_dict) == 0:
                return
            item: str = self.symlink_dict.key_of_index(self.selected_index)
            self.jump_link(item)
        elif self.tab == "脚本":
            if len(self.script_dict) == 0:
                return
            item: str = self.script_dict.key_of_index(self.selected_index)
            self.run_script(item)
        elif self.tab == "网页":
            if len(self.url_dict) == 0:
                return
            item: str = self.url_dict.key_of_index(self.selected_index)
            self.open_url(item)
        else:
            if len(self.shortcut_dict) == 0:
                return
            item: str = self.shortcut_dict.value_of_index(self.selected_index).command
            self.parse_command(item)

    def add_symlink(self, name: str, path: str):
        """
        添加链接
        :param name: 链接名称
        :param path: 链接路径
        """
        if name in self.symlink_dict:
            self.add_info(f"链接 {name} 已更新: {path}")
        else:
            self.add_info(f"链接 {name} 已添加: {path}")
        self.symlink_dict[name] = Symlink(path=path)
        toml_data = {k: {"path": v.path} for k, v in self.symlink_dict.items()}
        with self.symlink_path.open("wb") as f:
            tomli_w.dump(toml_data, f)

    def add_script(self, name: str, path: str):
        """
        添加脚本
        :param name: 脚本名称
        :param path: 脚本路径
        """
        if name in self.script_dict:
            self.add_info(f"脚本 {name} 已更新: {path}")
        else:
            self.add_info(f"脚本 {name} 已添加: {path}")
        self.script_dict[name] = Script(path=path)
        toml_data = {k: {"path": v.path} for k, v in self.script_dict.items()}
        with self.script_path.open("wb") as f:
            tomli_w.dump(toml_data, f)

    def add_url(self, name: str, url: str):
        """
        添加网页
        :param name: 网页名称
        :param url: 网页链接
        """
        if name not in self.url_dict:
            self.url_dict[name] = Url(urls=[])
        self.url_dict[name].urls.append(url)
        toml_data = {k: {"urls": v.urls} for k, v in self.url_dict.items()}
        with self.url_path.open("wb") as f:
            tomli_w.dump(toml_data, f)
        self.add_info(f"网页组 {name} 已添加: {url}")

    def select_previous(self, _event=None):
        """
        选择上一项
        :param _event: 事件对象
        """
        if self.list_length == 0:
            return
        if self.selected_index > 0:
            self.selected_index -= 1
        else:
            self.selected_index = self.list_length - 1
        # 调用回调函数
        self.roll_bar_callback(self.selected_index)
        self.preview_update_callback(self.get_preview_content())

    def select_next(self, _event=None):
        """
        选择下一项
        :param _event: 事件对象
        """
        if self.list_length == 0:
            return
        if self.selected_index < self.list_length - 1:
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
        if self.tab == "文件系统":
            if len(self.dir_items) == 0:
                return "无可预览文件"
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
        if self.tab == "链接":
            if len(self.symlink_dict) == 0:
                return "无可预览链接"
            item: Symlink = self.symlink_dict.value_of_index(self.selected_index)
            return item.path
        if self.tab == "脚本":
            if len(self.script_dict) == 0:
                return "无可预览脚本"
            item: Script = self.script_dict.value_of_index(self.selected_index)
            script_path = Path(item.path)
            if script_path.exists():
                with script_path.open(encoding="utf-8") as f:
                    content = f.read()
                    return content
            else:
                return "脚本文件不存在"
        if self.tab == "网页":
            if len(self.url_dict) == 0:
                return "无可预览网页"
            item: Url = self.url_dict.value_of_index(self.selected_index)
            return "\n".join(item.urls)
        else:
            if len(self.shortcut_dict) == 0:
                return "无可预览快捷键"
            item: Shortcut = self.shortcut_dict.value_of_index(self.selected_index)
            return item.command

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
            if func in self.shortcut_dict.keys():
                shortcut = self.shortcut_dict[func]
                self.parse_command(shortcut.command)
            else:
                self.add_info("未知命令")

    def update_tab(self, tab_name: str):
        """
        更新标签页切换后的界面
        :param tab_name: 标签页名称
        :return:
        """
        self.tab = tab_name
        self.selected_index = 0

        # 更新路径栏与列表框
        if tab_name == "文件系统":
            path = str(self.file_path)
            item_list = [(item.name, 4 if item.is_dir() else 3) for item in self.dir_items]
        elif tab_name == "链接":
            path = "symlinks"
            item_list = [(item, 2) for item in self.symlink_dict.keys()]
        elif tab_name == "脚本":
            path = "scripts"
            item_list = [(item, 1) for item in self.script_dict.keys()]
        elif tab_name == "网页":
            path = "urls"
            item_list = [(item, 5) for item in self.url_dict.keys()]
        else:
            path = "shortcuts"
            item_list = [(item, 6) for item in self.shortcut_dict.keys()]
        self.list_length = len(item_list)
        self.list_update_callback(path, item_list)

        # 更新预览框
        self.preview_update_callback(self.get_preview_content())

    def completion(self, command: str) -> str:
        """
        补全命令
        :param command: 命令字符串
        :return: 加上最可能补全后的命令
        """
        command_l = command.strip().split(" ")
        if len(command_l) < 2:
            return command
        func = command_l[0]
        arg = command_l[1]
        if func == "cd":
            candidates = [item.name for item in self.dir_items]
        elif func == "lk":
            candidates = self.symlink_dict.get_key_list()
        elif func == "sc":
            candidates = self.script_dict.get_key_list()
        elif func == "wb":
            candidates = self.url_dict.get_key_list()
        else:
            return command
        match_list = difflib.get_close_matches(arg, candidates)
        if match_list:
            return f"{func} {match_list[0]}"
        else:
            return command
