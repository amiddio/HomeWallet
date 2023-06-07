import tkinter as tk

from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import Callable

from lang_pack.lang import LANG_COLORS
from models.scheme import TypeEnum

from functools import partial


class WidgetTotalSection:

    filter_btn = None

    def __init__(self, root: tk, values: list):
        self.root = root
        self.values = values
        #self.callback = callback

    def __call__(self):
        # Created container
        container = self.root.get_container_frame(self.root, columns=[1, 1, 1, 10, 1])

        label_total = "Total: "
        price_gel, price_usd = self._get_price()
        label_gel = f"{round(price_gel, 2)} GEL"
        label_usd = f"{round(price_usd, 2)} USD"
        label_tags = "Tags: "

        tk.Label(container, text=label_total).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        tk.Label(container, text=label_gel).grid(row=0, column=1, sticky='we', padx=10, pady=10)
        tk.Label(container, text=label_usd).grid(row=0, column=2, sticky='we', padx=10, pady=10)
        text_area = ScrolledText(
            container, wrap=tk.WORD, height=2, background=LANG_COLORS["main_bg"], border=0
        )
        text_area.insert(tk.INSERT, label_tags + self._get_tags())
        text_area.configure(state='disabled')
        text_area.grid(row=0, column=3, sticky="we", pady=10, padx=10)
        btn = ttk.Button(container, style='Manage.TButton', text='Filter')
        btn.grid(row=0, column=4, sticky="e", padx=15, pady=10)
        return container, btn

    def _get_price(self):
        gel = usd = 0.0
        for val in self.values:
            if val.get().type == TypeEnum.VOUT:
                gel -= val.get().price_gel
                usd -= val.get().price_usd
            elif val.get().type == TypeEnum.VIN:
                gel += val.get().price_gel
                usd += val.get().price_usd
        return gel, usd

    def _get_tags(self):
        tags = set()
        for val in self.values:
            for tag in val.get().tags:
                tags.add(tag.name)
        return ', '.join(sorted(tags))

    @staticmethod
    def destroy(total_section) -> None:
        if total_section:
            total_section.destroy()
