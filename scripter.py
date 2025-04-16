from pathlib import Path

import customtkinter as ctk
import win32con
import win32gui

from colors import Colors
from inputframe import InputFrame
from outputframe import OutputFrame
from titlebar import TitleBar


class Scripter(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.x = None
        self.y = None
        self.title("Scripter")
        self.geometry("800x600")
        self.configure(fg_color=Colors.base.hex_tuple)

        self.overrideredirect(True)
        # 强制添加任务栏图标
        self.hwnd = win32gui.GetParent(self.winfo_id())
        win32gui.SetWindowLong(
            self.hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_APPWINDOW
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=19)
        self.columnconfigure((0, 1), weight=1)

        # top frame
        self.top_frame = TitleBar(self)
        self.top_frame.grid(row=0, column=0, padx=0, pady=0, columnspan=2, sticky="nsew")
        self.top_frame.bind("<ButtonPress-1>", self.start_move)
        self.top_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.top_frame.bind("<B1-Motion>", self.do_move)

        # left scrollable frame
        self.left_frame = OutputFrame(self)
        self.left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # right frame
        self.right_frame = InputFrame(self)
        self.right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # 属性变量
        self.path = Path.home()
        self.left_frame.update_path(self.path)
        self.func_map = {
            "cd": self.change_directory,
        }

        # 按键绑定
        self.bind_all("<Up>", self.left_frame.select_previous)
        self.bind_all("<Down>", self.left_frame.select_next)
        self.bind("<Alt-Tab>", lambda e: self.lift())
        self.bind("<Escape>", lambda e: self.destroy())

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, _event):
        self.x = None
        self.y = None

    def do_move(self, event):
        x = event.x - self.x
        y = event.y - self.y
        self.geometry(f"+{self.winfo_x() + x}+{self.winfo_y() + y}")

    def change_tab(self, tab_name: str):
        pass

    def parse_command(self, command: str):
        command = command.strip().split(" ")
        func = command[0]
        args = command[1:]
        if func in self.func_map:
            try:
                self.func_map[func](*args)
            except TypeError as e:
                self.add_info(f"参数错误: {e}")
        else:
            self.add_info("未知命令")

    def change_directory(self, path: str):
        path = Path(path)
        # 如果是相对路径，转换为绝对路径
        if not path.is_absolute():
            path = self.path / path
            path = path.resolve(strict=False)
        if path.exists() and path.is_dir():
            self.path = path
            self.left_frame.update_path(self.path)
        else:
            self.add_info("路径不存在或不是目录")

    def add_info(self, info: str):
        self.right_frame.add_info(info)
