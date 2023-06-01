import tkinter as tk

from lang_pack.lang import LANG_MENU
from widgets.tags import Tags


class Menu(tk.Menu):

    # ------------------------------------------------------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, root):
        super().__init__()
        self.root = root

        menu = tk.Menu(self.root)

        new = tk.Menu(menu, tearoff=0)
        new.add_separator()
        new.add_command(label=LANG_MENU["exit"], command=self.master.destroy)
        menu.add_cascade(label=LANG_MENU["new"], menu=new)

        tags = tk.Menu(menu, tearoff=0)
        tags.add_cascade(label=LANG_MENU["manage"], command=lambda: Tags(self.root))
        menu.add_cascade(label=LANG_MENU["tags"], menu=tags)

        self.root.config(menu=menu)

