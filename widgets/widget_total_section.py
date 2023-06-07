import tkinter as tk
import helper as hlp

from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import Callable

from lang_pack.lang import LANG_COLORS, LANG_GENERAL
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
        label_gel = LANG_GENERAL["gel"].format(price=hlp.display_price(price_gel))
        label_usd = LANG_GENERAL["usd"].format(price=hlp.display_price(price_usd))
        price_fg = LANG_COLORS["price_red"] if price_gel < 0 else LANG_COLORS["price_green"]

        tk.Label(container, text=label_total, font=("Calibri", 14))\
            .grid(row=0, column=0, sticky='e', padx=10, pady=10)
        tk.Label(container, text=label_gel, fg=price_fg, font=("Calibri", 14, 'bold'))\
            .grid(row=0, column=1, sticky='we', padx=10, pady=10)
        tk.Label(container, text=label_usd, fg=price_fg, font=("Calibri", 14, 'bold'))\
            .grid(row=0, column=2, sticky='we', padx=10, pady=10)
        text_area = ScrolledText(
            container, wrap=tk.WORD, height=2, background=LANG_COLORS["main_bg"], border=0
        )
        text_area.insert(tk.INSERT, self._get_tags())
        text_area.configure(state='disabled')
        text_area.grid(row=0, column=3, sticky="we", pady=10, padx=10)
        btn = ttk.Button(container, style='Manage.TButton', text='Filter')
        btn.grid(row=0, column=4, sticky="e", padx=15, pady=10)
        return container, btn

    def _get_price(self):
        gel = usd = 0.0
        for val in self.values:
            price_gel = val.get().price_gel if val.get().price_gel else 0
            price_usd = val.get().price_usd if val.get().price_usd else 0
            if val.get().type == TypeEnum.VOUT:
                gel -= price_gel
                usd -= price_usd
            elif val.get().type == TypeEnum.VIN:
                gel += price_gel
                usd += price_usd
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
