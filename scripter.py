"""
scripter.py
"""

import customtkinter as ctk
import win32con
import win32gui

from colors import Colors
from inputframe import InputFrame
from manager import Manager
from outputframe import OutputFrame
from titlebar import TitleBar


class Scripter(ctk.CTk):
    """
    Scripter 主窗口类
    """

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

        # 标题栏
        self.top_frame = TitleBar(self)
        self.top_frame.grid(row=0, column=0, padx=0, pady=0, columnspan=2, sticky="nsew")
        self.top_frame.bind("<ButtonPress-1>", self.start_move)
        self.top_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.top_frame.bind("<B1-Motion>", self.do_move)

        # 左侧输出框
        self.left_frame = OutputFrame(self)
        self.left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # 右侧输入框
        self.right_frame = InputFrame(self)
        self.right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # 属性变量
        self.manager = Manager()

        # 回调函数绑定
        self.right_frame.get_command_callback = self.manager.parse_command
        self.manager.list_update_callback = self.left_frame.update_list
        self.manager.preview_update_callback = self.left_frame.update_preview
        self.manager.info_update_callback = self.right_frame.update_info
        self.manager.roll_bar_callback = self.left_frame.roll_bar

        # 按键绑定
        self.bind_all("<Up>", self.manager.select_previous)
        self.bind_all("<Down>", self.manager.select_next)
        self.bind("<Alt-Tab>", lambda e: self.lift())
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<F1>", lambda e: self.change_tab("文件系统"))
        self.bind("<F2>", lambda e: self.change_tab("链接"))
        self.bind("<F3>", lambda e: self.change_tab("脚本"))
        self.bind("<F4>", lambda e: self.change_tab("网页"))
        self.bind("<F5>", lambda e: self.change_tab("快捷键"))

        # 初始化列表框
        self.manager.change_path(".")

    def start_move(self, event):
        """
        开始移动窗口
        :param event: 鼠标事件
        :return:
        """
        self.x = event.x
        self.y = event.y

    def stop_move(self, _event):
        """
        停止移动窗口
        :param _event: 鼠标事件
        :return:
        """
        self.x = None
        self.y = None

    def do_move(self, event):
        """
        移动窗口
        :param event: 鼠标事件
        :return:
        """
        x = event.x - self.x
        y = event.y - self.y
        self.geometry(f"+{self.winfo_x() + x}+{self.winfo_y() + y}")

    def change_tab(self, tab_name: str):
        """
        切换标签页
        :param tab_name: 标签页名称
        :return:
        """
        self.right_frame.tab_button.set(tab_name)
        self.manager.change_tab(tab_name)
