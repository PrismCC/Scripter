import customtkinter as ctk

from colors import Colors


class TitleBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=Colors.surface0.hex_tuple, corner_radius=0)
        self.parent = parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=9)
        self.grid_columnconfigure(1, weight=1)

        # title label
        self.title_label = ctk.CTkLabel(self, text="Scripter", text_color=Colors.text.hex_tuple, height=18)
        self.title_label.grid(row=0, column=0, padx=(20, 20), pady=1, sticky="w")

        # close button
        self.close_button = ctk.CTkButton(self, text="X", command=self.parent.destroy, width=20, height=20,
                                          fg_color=Colors.base.hex_tuple, text_color=Colors.text.hex_tuple,
                                          hover_color=Colors.red.hex_tuple, border_width=0, corner_radius=0)
        self.close_button.grid(row=0, column=1, padx=0, pady=0, sticky="e")
