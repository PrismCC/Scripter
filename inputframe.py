"""
inputframe.py
"""
from collections import deque

import customtkinter as ctk

from colors import Colors


class InputFrame(ctk.CTkFrame):
    """
    右侧输入框
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color=Colors.surface0.hex_tuple)
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=5)

        self.tab_button = ctk.CTkSegmentedButton(self, values=["文件系统", "链接", "脚本", "网页", "快捷键"],
                                                 fg_color=Colors.surface0.hex_tuple, text_color=Colors.text.hex_tuple,
                                                 selected_color=Colors.base.hex_tuple,
                                                 selected_hover_color=Colors.mantle.hex_tuple,
                                                 unselected_color=Colors.surface2.hex_tuple,
                                                 unselected_hover_color=Colors.surface1.hex_tuple,
                                                 command=parent.change_tab)
        self.tab_button.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.tab_button.set("文件系统")

        # 命令栏
        self.command_entry = ctk.CTkEntry(self, placeholder_text="命令", fg_color=Colors.surface1.hex_tuple,
                                          text_color=Colors.text.hex_tuple, border_width=0, corner_radius=0)
        self.command_entry.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.command_entry.bind("<Return>", self.get_command)
        self.command_entry.focus()

        # 控制选项
        self.control_frame = ctk.CTkFrame(self, fg_color=Colors.surface1.hex_tuple)
        self.control_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # 提示信息
        self.info_box = ctk.CTkTextbox(self, fg_color=Colors.surface1.hex_tuple, text_color=Colors.text.hex_tuple,
                                       state="disabled", height=300)
        self.info_box.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        # 按键绑定
        self.command_entry.bind("<Tab>", lambda e: self.complete_command(e))

        # 属性变量
        self.get_command_callback = None
        self.complete_command_callback = None

    def get_command(self, _event=None):
        """
        获取命令栏输入的命令
        :param _event: 事件对象
        :return:
        """
        command = self.command_entry.get()
        if command:
            self.get_command_callback(command)
        self.command_entry.delete(0, ctk.END)

    def update_info(self, info_list: deque[str]):
        """
        更新提示信息
        :param info_list: 提示信息列表
        :return:
        """
        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", ctk.END)
        for line in info_list:
            self.info_box.insert(ctk.END, line + "\n")
        self.info_box.configure(state="disabled")

    def complete_command(self, _event=None) -> str:
        """
        自动补全命令
        :return: 事件对象
        """
        old_command = self.command_entry.get()
        self.command_entry.delete(0, ctk.END)
        new_command = self.complete_command_callback(old_command)
        self.command_entry.insert(0, new_command)
        return "break"
