import tkinter as tk

from datetime import datetime
from functools import partial
from typing import Callable
from lang_pack.lang import LANG_GENERAL, LANG_COLORS
from models.scheme import TypeEnum
from models.value_model import ValueModel
from widgets.widget_checkbutton_form_row import WidgetCheckbuttonFormRow
from widgets.widget_entry_form_row import WidgetEntryFormRow
from widgets.widget_selectbox_form_row import WidgetSelectboxFormRow
from widgets.widget_textarea_form_row import WidgetTextareaFormRow


class WidgetSavePopup:
    """
    Widget popup to add/edit value
    """

    value = None

    def __init__(self, master: tk, btn_add: tk.Button, save_value: Callable, iid: int = None) -> None:
        self.master = master
        self.btn_add = btn_add
        self.save_value = save_value
        self.iid = iid

    def __call__(self) -> None:
        if self.iid:
            self.value = ValueModel.get_by_id(iid=self.iid)

        # Create popup
        popup = self.master.popup(
            window_title=LANG_GENERAL["add value"] if not self.value else LANG_GENERAL["edit value"],
            less_by_x=200, less_by_y=380
        )
        close_popup = self.master.close_popup_action(popup=popup, btn=self.btn_add)

        # Add popup header
        btn = self.master.get_page_header(
            popup, title=LANG_GENERAL["add value"] if not self.value else LANG_GENERAL["edit value"],
            btn_text=LANG_GENERAL["save"], bg_color=LANG_COLORS["header_bg"]
        )
        btn.configure(command=partial(self.save_value, close_popup=close_popup, value=self.value))
        self._get_fields_section(popup)  # Add fields section

    def _get_fields_section(self, popup: tk.Toplevel):
        from widgets.values import ValuesStore
        from widgets.values import VALUES_TYPES

        # Add type
        ValuesStore.type = WidgetSelectboxFormRow(
            root=self.master, popup=popup, label=LANG_GENERAL["type"], data=VALUES_TYPES,
            fill=self.value.get().type if self.value else TypeEnum.VOUT
        )()
        # Add price_gel entry
        ValuesStore.price_gel = WidgetEntryFormRow(
            root=self.master, popup=popup, label=LANG_GENERAL["price gel"], is_focus=True,
            text=self.value.get().price_gel if self.value else ''
        )()
        # Add price_usd entry
        ValuesStore.price_usd = WidgetEntryFormRow(
            root=self.master, popup=popup, label=LANG_GENERAL["price usd"],
            text=self.value.get().price_usd if self.value else ''
        )()
        # Add date entry
        date_ = datetime.now() if not self.value else self.value.get().date
        ValuesStore.date = WidgetEntryFormRow(
            root=self.master, popup=popup, label=LANG_GENERAL["date"],
            text=date_.strftime('%Y-%m-%d')
        )()
        # Add message text area
        ValuesStore.message = WidgetTextareaFormRow(
            root=self.master, popup=popup, text=self.value.get().message if self.value else None
        )()
        # Add tags area
        ValuesStore.tags = WidgetCheckbuttonFormRow(
            root=self.master, popup=popup, checked=self.value.get().tags if self.value else None
        )()
