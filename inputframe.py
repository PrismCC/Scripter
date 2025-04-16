from collections import deque

import customtkinter as ctk

from colors import Colors


class InputFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=Colors.surface0.hex_tuple)
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=5)

        self.tab_button = ctk.CTkSegmentedButton(self, values=["文件系统", "路径", "脚本", "链接", "快捷键"],
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
        self.info_label = ctk.CTkTextbox(self, fg_color=Colors.surface1.hex_tuple, text_color=Colors.text.hex_tuple,
                                         state="disabled", height=300)
        self.info_label.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.info_list = deque(maxlen=20)

    def get_command(self, _event=None):
        command = self.command_entry.get()
        if command:
            self.parent.parse_command(command)
        self.command_entry.delete(0, ctk.END)

    def add_info(self, info: str):
        self.info_list.append(info)
        self.info_label.configure(state="normal")
        self.info_label.delete("1.0", ctk.END)
        for item in self.info_list:
            self.info_label.insert(ctk.END, item + "\n")
        self.info_label.configure(state="disabled")
