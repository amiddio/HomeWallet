import tkinter as tk

from tkinter.scrolledtext import ScrolledText


class WidgetTextareaFormRow:

    def __init__(self, root: tk, popup, text: str = None) -> None:
        self.root = root
        self.popup = popup
        self.text = text

    def __call__(self):
        # Created container
        container = self.root.get_container_frame(self.popup, columns=[1])

        text_area = ScrolledText(container, wrap=tk.WORD, height=5)
        if self.text:
            text_area.insert(tk.INSERT, self.text)
        text_area.grid(row=1, column=0, sticky="we", pady=10, padx=10)
        return text_area
