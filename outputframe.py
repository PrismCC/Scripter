from pathlib import Path

import customtkinter as ctk
from customtkinter import CTkLabel

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
        self.preview_label = ctk.CTkTextbox(self, fg_color=Colors.surface1.hex_tuple, text_color=Colors.text.hex_tuple,
                                            state="disabled")
        self.preview_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.label_list: list[CTkLabel] = []
        self.name_list: list[Path] = []
        self.selected_index = 0

    def update_path(self, path: Path):
        self.path_label.configure(text=path)
        self.update_list(path)
        self.update_preview()

    def update_list(self, path: Path):
        self.list_frame.destroy()
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=Colors.surface1.hex_tuple, height=300)
        self.list_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.label_list.clear()
        self.selected_index = 0

        self.name_list = list(path.iterdir())
        # 将文件夹排在前面
        self.name_list.sort(key=lambda x: (x.is_file(), x.name.lower()))
        for index, item in enumerate(self.name_list):
            if item.is_dir():
                item_label = ctk.CTkLabel(self.list_frame, text=item.name, text_color=Colors.teal.hex_tuple,
                                          fg_color=Colors.surface2.hex_tuple if index != self.selected_index else Colors.surface0.hex_tuple,
                                          height=10, anchor="w")
            else:
                item_label = ctk.CTkLabel(self.list_frame, text=item.name, text_color=Colors.blue.hex_tuple,
                                          fg_color=Colors.surface2.hex_tuple if index != self.selected_index else Colors.surface0.hex_tuple,
                                          height=10, anchor="w")
            self.label_list.append(item_label)
            item_label.pack(padx=5, pady=2, fill="x")

    def select_previous(self, _event):
        if len(self.label_list) == 0:
            return
        self.label_list[self.selected_index].configure(fg_color=Colors.surface2.hex_tuple)
        if self.selected_index > 0:
            self.selected_index -= 1
        else:
            self.selected_index = len(self.label_list) - 1
        self.label_list[self.selected_index].configure(fg_color=Colors.surface0.hex_tuple)
        # 滚动到选中的标签
        self.list_frame._parent_canvas.yview_moveto(max(0, self.selected_index - 5) * 1.0 / len(self.label_list))
        self.update_preview()

    def select_next(self, _event):
        if len(self.label_list) == 0:
            return
        self.label_list[self.selected_index].configure(fg_color=Colors.surface2.hex_tuple)
        if self.selected_index < len(self.label_list) - 1:
            self.selected_index += 1
        else:
            self.selected_index = 0
        self.label_list[self.selected_index].configure(fg_color=Colors.surface0.hex_tuple)
        # 滚动到选中的标签
        self.list_frame._parent_canvas.yview_moveto(max(0, self.selected_index - 5) * 1.0 / len(self.label_list))
        self.update_preview()

    def can_preview(self) -> bool:
        selected_path = self.name_list[self.selected_index]
        # 不是文件夹
        if selected_path.is_dir():
            return False
        # 小于100KB
        if selected_path.stat().st_size >= 1024 * 100:
            return False
        # 是文本文件
        if b'\x00' in selected_path.read_bytes()[:1024]:
            return False
        return True

    def update_preview(self):
        selected_path = self.name_list[self.selected_index]
        if not self.can_preview():
            self.preview_label.configure(state="normal")
            self.preview_label.delete("0.0", ctk.END)
            self.preview_label.insert("0.0", "该文件无法预览")
            self.preview_label.configure(state="disabled")
            return
        try:
            with open(selected_path, "r", encoding="utf-8") as f:
                text = f.read()
            self.preview_label.configure(state="normal")
            self.preview_label.delete("0.0", ctk.END)
            self.preview_label.insert("0.0", text)
            self.preview_label.configure(state="disabled")
        except Exception as _e:
            self.preview_label.configure(state="normal")
            self.preview_label.delete("0.0", ctk.END)
            self.preview_label.insert("0.0", "该文件无法预览")
            self.preview_label.configure(state="disabled")
