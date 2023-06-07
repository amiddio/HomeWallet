import calendar
import dataclasses
import tkinter as tk
import tkinter.messagebox as mb
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Entry

import helper as hlp

from datetime import datetime
from functools import partial
from tkinter import ttk
from typing import Callable
from sqlalchemy import desc
from lang_pack.lang import LANG_GENERAL, LANG_COLORS, LANG_MSG
from logger.logger import log
from models.scheme import TypeEnum
from models.tag_model import TagModel
from models.value_model import ValueModel
from widgets.widget_checkbutton_form_row import WidgetCheckbuttonFormRow
from widgets.widget_entry_form_row import WidgetEntryFormRow
from widgets.widget_filter_popup import WidgetFilterPopup
from widgets.widget_save_popup import WidgetSavePopup
from widgets.widget_selectbox_form_row import WidgetSelectboxFormRow
from widgets.widget_textarea_form_row import WidgetTextareaFormRow
from widgets.widget_total_section import WidgetTotalSection
from widgets.widget_treeview_table import WidgetTreeviewTable
from widgets.widget_view_popup import WidgetViewPopup

VALUES_TYPES = (LANG_GENERAL["income"], LANG_GENERAL["expense"])


class ValuesStore:
    type: tk.StringVar
    price_usd: Entry
    price_gel: Entry
    date: Entry
    message: ScrolledText
    tags: list


class FilterStore:
    from_year: tk.StringVar = None
    from_month: tk.StringVar = None
    to_year: tk.StringVar = None
    to_month: tk.StringVar = None
    tags: list = None
    submit: tk.Button = None


class Values:
    price_usd = None
    price_gel = None
    date_ = None
    type_ = None
    message = None
    btn_add = None
    btn_filter = None
    btn_filter_submit = None
    treeview = None
    scrollbar = None
    tags = None
    total_section = None
    filter_section = None
    from_year = from_month = to_year = to_month = None

    # ------------------------------------------------------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, root: tk) -> None:
        super().__init__()

        self.root = root

        self.root.clear_window()
        FilterStore.submit = None

        # Add page header
        self.btn_add = self.root.get_page_header(
            self.root, title=LANG_GENERAL["wallet"], btn_text=LANG_GENERAL["add"],
            bg_color=LANG_COLORS["header_bg"]
        )
        self.btn_add.configure(command=WidgetSavePopup(self.root, self.btn_add, self.save_value))

        # Create treeview
        self.values_treevew()

    # ------------------------------------------------------------------------------------------------------------------
    # Treeview Methods
    # ------------------------------------------------------------------------------------------------------------------

    def values_treevew(self) -> None:
        # Prepare data to treeview
        columns = (LANG_GENERAL["tags"], LANG_GENERAL["price gel"], LANG_GENERAL["price usd"], LANG_GENERAL["date"])
        columns_width = (500, 20, 20, 50)

        data = []
        if not FilterStore.submit:
            values = ValueModel.get_latest()
        else:
            values = ValueModel.get_all_filtered(
                date_from=(FilterStore.from_year.get(), hlp.get_month_number(FilterStore.from_month.get())),
                date_to=(FilterStore.to_year.get(), hlp.get_month_number(FilterStore.to_month.get())),
                tags=[tag.id for tag in TagModel.get_checked_tags(FilterStore.tags)]
            )
        for val in values:
            tags = ', '.join([i.name for i in val.get().tags])
            gel = val.display_price(val.get().price_gel)
            usd = val.display_price(val.get().price_usd)
            data.append(
                (val.get().id, tags, gel, usd, ValueModel.date_formated(val.get().date))
            )
        callbacks = {
            LANG_GENERAL["view"]: self.treeview_submenu_view,
            LANG_GENERAL["edit"]: self.treeview_submenu_edit,
            LANG_GENERAL["delete"]: self.treeview_submenu_delete
        }

        # Create total section
        WidgetTotalSection.destroy(self.total_section)
        self.total_section, self.btn_filter = WidgetTotalSection(
            #root=self.root, values=values, callback=self.open_filter_popup
            root=self.root, values=values
        )()
        self.btn_filter.configure(command=WidgetFilterPopup(self.root, self.btn_filter, self.action_filter))

        # Create treeview
        WidgetTreeviewTable.destroy(self.treeview, self.scrollbar)
        trv = WidgetTreeviewTable(
            root=self.root, columns=columns, columns_width=columns_width, rows=data, callbacks=callbacks
        )
        self.treeview, self.scrollbar = trv()

    def treeview_submenu_view(self, tv: ttk.Treeview) -> None:
        for iid in tv.selection():
            WidgetViewPopup(master=self.root, iid=int(iid))()

    def treeview_submenu_edit(self, tv: ttk.Treeview) -> None:
        for iid in tv.selection():
            # self.open_add_edit_popup(iid=int(iid))
            WidgetSavePopup(self.root, self.btn_add, self.save_value, iid=int(iid))()

    def treeview_submenu_delete(self, tv: ttk.Treeview) -> None:
        try:
            if mb.askyesno(message=LANG_MSG["are you sure to delete this value"], title=LANG_GENERAL["yesno"]):
                for iid in tv.selection():
                    val = ValueModel.get_by_id(iid=int(iid))
                    if val:
                        tv.delete(iid)
                        val.delete()
                        msg = LANG_MSG["value deleted successfully"]
                        mb.showinfo(LANG_GENERAL["info"], msg)
                        log().info(msg)
        except Exception as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["internal error"], str(e))

    def action_filter(self, close_popup):
        close_popup()  # Close popup
        self.values_treevew()  # Refresh treeview

    # ------------------------------------------------------------------------------------------------------------------
    # Save Method
    # ------------------------------------------------------------------------------------------------------------------

    def save_value(self, close_popup: Callable, value: ValueModel = None) -> None:
        try:
            type_ = TypeEnum(ValuesStore.type.get())
            price_gel = float(ValuesStore.price_gel.get().strip())
            price_usd = float(ValuesStore.price_usd.get().strip())
            date_ = ValuesStore.date.get().strip()
            message = ValuesStore.message.get("1.0", tk.END).strip()
            tags = TagModel.get_checked_tags(ValuesStore.tags)

            # Validate type is required
            if not type_:
                raise TypeError(LANG_MSG["field type is required"])

            # Validate date is required
            if not date_:
                raise TypeError(LANG_MSG["field date is required"])

            # Add new value
            if not value:
                result = ValueModel(
                    type=type_,
                    price_gel=price_gel,
                    price_usd=price_usd,
                    date=datetime.strptime(date_, '%Y-%m-%d'),
                    message=message
                ).save().add_tags(tags)
            # Edit value
            else:
                value.set(
                    type=type_,
                    price_gel=price_gel,
                    price_usd=price_usd,
                    date=datetime.strptime(date_, '%Y-%m-%d'),
                    message=message
                )
                result = value.save().add_tags(tags)

            # If success
            if result:
                msg = LANG_MSG["value saved successfully"]
                log().info(msg)
                mb.showinfo(LANG_GENERAL["info"], msg)
                self.tags = None
                close_popup()  # Close popup
                self.values_treevew()  # Refresh treeview

        except TypeError as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["validation error"], str(e))
        except Exception as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["internal error"], str(e))

    # ------------------------------------------------------------------------------------------------------------------
    # Filter Methods
    # ------------------------------------------------------------------------------------------------------------------

    # def open_filter_popup(self):
    #
    #     # Create popup
    #     popup = self.root.popup(window_title='Filter', less_by_x=200, less_by_y=380)
    #     close_popup = self.root.close_popup_action(popup=popup, btn=self.btn_filter)
    #
    #     container1 = self.root.get_container_frame(popup, columns=[1, 1, 1, 1, 10])
    #     self.from_year = self.root.select_box_filter(
    #         container=container1, data=ValueModel.get_years_range(),
    #         label='From:', column=0,
    #         selected=datetime.today().year if not self.from_year else self.from_year.get()
    #     )
    #     self.from_month = self.root.select_box_filter(
    #         container=container1, data=list(calendar.month_name),
    #         label='', column=1,
    #         selected=datetime.today().strftime('%B') if not self.from_month else self.from_month.get()
    #     )
    #     self.to_year = self.root.select_box_filter(
    #         container=container1, data=ValueModel.get_years_range(),
    #         label='To:', column=2,
    #         selected=datetime.today().year if not self.to_year else self.to_year.get()
    #     )
    #     self.to_month = self.root.select_box_filter(
    #         container=container1, data=list(calendar.month_name),
    #         label='', column=3,
    #         selected=datetime.today().strftime('%B') if not self.to_month else self.to_month.get()
    #     )
    #
    #     # Add tags area
    #     self.tags = WidgetCheckbuttonFormRow(
    #         root=self.root, popup=popup,
    #         checked=TagModel.get_checked_tags(self.tags)
    #     )()
    #
    #     # self.root.get_filter_header(popup)
    #     container2 = self.root.get_container_frame(popup, columns=[10, 1])
    #     self.btn_filter_submit = ttk.Button(
    #         container2, style='Manage.TButton', text="Filter"
    #     )
    #     self.btn_filter_submit.configure(command=partial(self.action_filter, close_popup=close_popup))
    #     self.btn_filter_submit.grid(row=1, column=1, sticky="e", padx=10, pady=10)

    # ------------------------------------------------------------------------------------------------------------------
    # View Method
    # ------------------------------------------------------------------------------------------------------------------

    # def open_view_popup(self, iid: int) -> None:
    #
    #     value = ValueModel.get_by_id(iid=iid)
    #
    #     gel = f"{value.display_price(value.get().price_gel)} GEL"
    #     usd = f"{value.display_price(value.get().price_usd)} USD"
    #     date_ = ValueModel.date_formated(value.get().date)
    #     tags = LANG_GENERAL["tags"] + ': ' + ', '.join([tag.name for tag in value.get().tags])
    #
    #     if value.get().type == TypeEnum.VOUT:
    #         price_fg = LANG_COLORS["price_red"]
    #     else:
    #         price_fg = LANG_COLORS["price_green"]
    #
    #     # Create popup
    #     popup = self.root.popup(window_title=LANG_GENERAL["view value"], less_by_x=200, less_by_y=620)
    #
    #     # Add popup header
    #     self.root.get_page_header(
    #         popup, title=LANG_GENERAL["view value title"].format(type=value.get().type.value),
    #         bg_color=LANG_COLORS["header_bg"]
    #     )
    #
    #     container = self.root.get_container_frame(popup, columns=[1, 1, 1])
    #     tk.Label(container, text=gel, fg=price_fg, font=("Calibri", 16, 'bold'))\
    #         .grid(row=0, column=0, sticky="we", padx=10, pady=10)
    #     tk.Label(container, text=usd, fg=price_fg, font=("Calibri", 16, 'bold'))\
    #         .grid(row=0, column=1, sticky="we", padx=10, pady=10)
    #     tk.Label(container, text=date_, font=("Calibri", 14))\
    #         .grid(row=0, column=2, sticky="we", padx=10, pady=10)
    #     tk.Label(container, text=tags, font=("Calibri", 14))\
    #         .grid(row=1, column=0, sticky="w", padx=10, pady=20)
    #     if value.get().message:
    #         container2 = self.root.get_container_frame(popup, columns=[1])
    #         text_area = ScrolledText(container2, wrap=tk.WORD, height=7)
    #         text_area.insert(tk.INSERT, value.get().message)
    #         text_area.configure(state='disabled')
    #         text_area.grid(row=0, column=0, sticky="we", pady=10, padx=10)

    # ------------------------------------------------------------------------------------------------------------------
    # Save Methods
    # ------------------------------------------------------------------------------------------------------------------

    # def open_add_edit_popup(self, iid: int = None) -> None:
    #
    #     # Create popup
    #     popup = self.root.popup(window_title=LANG_GENERAL["add value"], less_by_x=200, less_by_y=380)
    #
    #     close_popup = self.root.close_popup_action(popup=popup, btn=self.btn_add)
    #
    #     value = None
    #     if iid:
    #         value = ValueModel.get_by_id(iid=iid)
    #
    #     # Add popup header
    #     self.root.get_page_header(
    #         popup, title=LANG_GENERAL["add value"], btn_text=LANG_GENERAL["save"],
    #         bg_color=LANG_COLORS["header_bg"],
    #         btn_callback=partial(self.save_value, close_popup=close_popup, value=value)
    #     )
    #     # Add type
    #     self.type_ = WidgetSelectboxFormRow(
    #         root=self.root, popup=popup, label=LANG_GENERAL["type"], data=Values.VALUES_TYPES,
    #         fill=value.get().type if value else None
    #     )()
    #     # Add price_gel entry
    #     self.price_gel = WidgetEntryFormRow(
    #         root=self.root, popup=popup, label=LANG_GENERAL["price gel"], is_focus=True,
    #         text=value.get().price_gel if value else ''
    #     )()
    #     # Add price_usd entry
    #     self.price_usd = WidgetEntryFormRow(
    #         root=self.root, popup=popup, label=LANG_GENERAL["price usd"],
    #         text=value.get().price_usd if value else ''
    #     )()
    #     # Add date entry
    #     date_ = datetime.now() if not value else value.get().date
    #     self.date_ = WidgetEntryFormRow(
    #         root=self.root, popup=popup, label=LANG_GENERAL["date"],
    #         text=date_.strftime('%Y-%m-%d')
    #     )()
    #     # Add message text area
    #     self.message = WidgetTextareaFormRow(
    #         root=self.root, popup=popup, text=value.get().message if value else None
    #     )()
    #     # Add tags area
    #     self.tags = WidgetCheckbuttonFormRow(
    #         root=self.root, popup=popup, checked=value.get().tags if value else None
    #     )()