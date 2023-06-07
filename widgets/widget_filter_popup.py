import calendar
import tkinter as tk

from datetime import datetime
from functools import partial
from tkinter import ttk
from typing import Callable
from lang_pack.lang import LANG_GENERAL, LANG_COLORS
from models.tag_model import TagModel
from models.value_model import ValueModel
from widgets.widget_checkbutton_form_row import WidgetCheckbuttonFormRow


class WidgetFilterPopup:
    """
    Widget popup for display filter
    """

    def __init__(self, master: tk, btn_filter: tk.Button, submit_filter: Callable) -> None:
        self.master = master
        self.btn_filter = btn_filter
        self.submit_filter = submit_filter

    def __call__(self) -> None:
        from widgets.values import FilterStore
        # Create popup
        popup = self.master.popup(window_title=LANG_GENERAL["filter"], less_by_x=200, less_by_y=550)
        # Add popup header
        FilterStore.submit = self.master.get_page_header(
            popup, title=LANG_GENERAL["filter"], btn_text=LANG_GENERAL["submit"], bg_color=LANG_COLORS["header_bg"]
        )
        FilterStore.submit.configure(
            command=partial(
                self.submit_filter,
                close_popup=self.master.close_popup_action(popup=popup, btn=self.btn_filter)
            )
        )
        self._get_date_section(popup=popup)  # Add date select boxes
        self._get_tags_section(
            popup=popup, close_popup=self.master.close_popup_action(popup=popup, btn=self.btn_filter)
        )  # Add tags section

    def _get_date_section(self, popup: tk.Toplevel) -> None:
        from widgets.values import FilterStore

        container = self.master.get_container_frame(popup, columns=[1, 1, 1, 1, 10])
        FilterStore.from_year = self.master.select_box_filter(
            container=container, data=ValueModel.get_years_range(), label=LANG_GENERAL["from"], column=0,
            selected=datetime.today().year if not FilterStore.from_year else FilterStore.from_year.get()
        )
        FilterStore.from_month = self.master.select_box_filter(
            container=container, data=list(calendar.month_name)[1:], label='', column=1,
            selected=datetime.today().strftime('%B') if not FilterStore.from_month else FilterStore.from_month.get()
        )
        FilterStore.to_year = self.master.select_box_filter(
            container=container, data=ValueModel.get_years_range(), label=LANG_GENERAL["to"], column=2,
            selected=datetime.today().year if not FilterStore.to_year else FilterStore.to_year.get()
        )
        FilterStore.to_month = self.master.select_box_filter(
            container=container, data=list(calendar.month_name)[1:], label='', column=3,
            selected=datetime.today().strftime('%B') if not FilterStore.to_month else FilterStore.to_month.get()
        )
        ttk.Separator(popup, orient='horizontal').pack(fill='x', padx=10, pady=(10, 5))

    def _get_tags_section(self, popup: tk.Toplevel, close_popup: Callable) -> None:
        from widgets.values import FilterStore

        # Add tags area
        FilterStore.tags = WidgetCheckbuttonFormRow(
            root=self.master, popup=popup,
            checked=TagModel.get_checked_tags(FilterStore.tags)
        )()
