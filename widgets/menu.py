import tkinter as tk

from lang_pack.lang import LANG_MENU
from widgets.tags import Tags
from widgets.values import Values, ViewMonth


class Menu(tk.Menu):

    # ------------------------------------------------------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, root):
        super().__init__()
        self.root = root

        menu = tk.Menu(self.root)

        view = tk.Menu(menu, tearoff=0)
        view.add_cascade(
            label=LANG_MENU["current month"], command=lambda: Values(self.root, view_month=ViewMonth.CURRENT)
        )
        view.add_cascade(
            label=LANG_MENU["last month"], command=lambda: Values(self.root, view_month=ViewMonth.LAST)
        )
        view.add_separator()
        view.add_command(label=LANG_MENU["exit"], command=self.master.destroy)
        menu.add_cascade(label=LANG_MENU["view"], menu=view)

        tags = tk.Menu(menu, tearoff=0)
        tags.add_cascade(label=LANG_MENU["manage"], command=lambda: Tags(self.root))
        menu.add_cascade(label=LANG_MENU["tags"], menu=tags)

        self.root.config(menu=menu)

