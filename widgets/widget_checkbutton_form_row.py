import tkinter as tk

from tkinter.scrolledtext import ScrolledText
from sqlalchemy import asc
from lang_pack.lang import LANG_COLORS
from models.tag_model import TagModel


class WidgetCheckbuttonFormRow:
    checked = None

    def __init__(self, root: tk, popup, checked: list = None) -> None:
        self.root = root
        self.popup = popup
        if checked:
            self.checked = [i.id for i in checked]

    def __call__(self):
        # Created container
        container = self.root.get_container_frame(self.popup, columns=[1])

        scrolled = ScrolledText(container, height=14, background=LANG_COLORS["main_bg"], state='disabled', border=0)
        scrolled.grid(row=1, column=0, sticky="we", pady=10, padx=10)

        checked = []
        tags = TagModel.get_all(order_={'name': asc})
        for i, tag in enumerate(tags):
            checked.append(tk.IntVar())
            checkbox = tk.Checkbutton(
                scrolled, text=tag.get().name, variable=checked[i], anchor='w', cursor='hand2', padx=10, pady=5
            )
            if self.checked and tag.get().id in self.checked:
                checkbox.select()
            scrolled.window_create('end', window=checkbox)
            scrolled.insert('end', '  ')
        return checked
