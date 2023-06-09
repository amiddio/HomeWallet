import tkinter as tk

from functools import partial
from typing import Callable
from lang_pack.lang import LANG_GENERAL, LANG_COLORS
from models.tag_model import TagModel
from widgets.widget_entry_form_row import WidgetEntryFormRow


class WidgetSaveTagPopup:

    def __init__(self, master: tk, btn_add: tk.Button, save_tag: Callable, iid: int = None) -> None:
        self.master = master
        self.btn_add = btn_add
        self.save_tag = save_tag
        self.iid = iid

    def __call__(self) -> None:
        from widgets.tags import TagStore

        # Create popup
        popup = self.master.popup(window_title=LANG_GENERAL["add tag"], less_by_x=200, less_by_y=600)
        close_popup = self.master.close_popup_action(popup=popup, btn=self.btn_add)

        # Add popup header
        btn = self.master.get_page_header(
            popup, title=LANG_GENERAL["add tag"], btn_text=LANG_GENERAL["save"], bg_color=LANG_COLORS["header_bg"]
        )
        btn.configure(command=partial(self.save_tag, close_popup, self.iid))
        # Add name entry
        TagStore.name = WidgetEntryFormRow(
            root=self.master, popup=popup, label=LANG_GENERAL["tag name"], is_focus=True,
            text=TagModel.get_by_id(iid=self.iid).get().name if self.iid else ''
        )()
