"""
outputfrome.py
"""

import customtkinter as ctk

from colors import Colors


class OutputFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=Colors.surface0.hex_tuple)
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=4)

        # 路径栏
        self.path_label = ctk.CTkLabel(self, text="路径", text_color=Colors.text.hex_tuple, height=10, anchor="w")
        self.path_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # 列表框
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=Colors.surface1.hex_tuple, height=300)
        self.list_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # 预览框
        self.preview_box = ctk.CTkTextbox(self, fg_color=Colors.surface1.hex_tuple, text_color=Colors.text.hex_tuple,
                                          state="disabled")
        self.preview_box.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # 属性变量
        self.label_list: list[ctk.CTkLabel] = []
        self.last_index = 0

    def update_path(self, path: str, item_list: list[tuple[str, bool]]):
        """
        更新路径栏和列表框
        :param path: 新路径字符串
        :param item_list: 列表框内容 [(文件名, 是否是目录), ...]
        :return:
        """
        self.path_label.configure(text=path)

        self.list_frame.destroy()
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=Colors.surface1.hex_tuple, height=300)
        self.list_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.label_list.clear()

        for item, is_dir in item_list:
            item_label = ctk.CTkLabel(self.list_frame, text=item,
                                      text_color=Colors.teal.hex_tuple if is_dir else Colors.blue.hex_tuple,
                                      fg_color=Colors.surface2.hex_tuple, height=10, anchor="w")
            self.label_list.append(item_label)
            item_label.pack(padx=5, pady=2, fill="x")
        if item_list:
            self.label_list[0].configure(fg_color=Colors.surface0.hex_tuple)
        self.last_index = 0

    def update_preview(self, content: str):
        """
        更新预览框内容
        :param content: 预览内容
        :return:
        """
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", ctk.END)
        self.preview_box.insert(ctk.END, content)
        self.preview_box.configure(state="disabled")

    def roll_bar(self, index: int):
        """
        滚动到指定索引
        :param index: 索引
        """
        self.list_frame._parent_canvas.yview_moveto(max(0, index - 5) * 1.0 / len(self.label_list))
        self.label_list[self.last_index].configure(fg_color=Colors.surface2.hex_tuple)
        self.label_list[index].configure(fg_color=Colors.surface0.hex_tuple)
        self.last_index = index
