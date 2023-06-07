import enum
import tkinter as tk
import helper as hlp
import tkinter.messagebox as mb

from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Entry
from datetime import datetime
from tkinter import ttk
from typing import Callable
from lang_pack.lang import LANG_GENERAL, LANG_COLORS, LANG_MSG
from logger.logger import log
from models.scheme import TypeEnum
from models.tag_model import TagModel
from models.value_model import ValueModel
from widgets.widget_filter_popup import WidgetFilterPopup
from widgets.widget_save_popup import WidgetSavePopup
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


class ViewMonth(enum.Enum):
    CURRENT = 'current'
    LAST = 'last'


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
    view_month = None

    # ------------------------------------------------------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, root: tk, view_month: ViewMonth) -> None:
        super().__init__()

        self.root = root
        self.view_month = view_month

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

        values = self._get_treeview_data()

        callbacks = {
            LANG_GENERAL["view"]: self.treeview_submenu_view,
            LANG_GENERAL["edit"]: self.treeview_submenu_edit,
            LANG_GENERAL["delete"]: self.treeview_submenu_delete
        }

        # Create total section
        WidgetTotalSection.destroy(self.total_section)
        self.total_section, self.btn_filter = WidgetTotalSection(
            root=self.root, values=values
        )()
        self.btn_filter.configure(command=WidgetFilterPopup(self.root, self.btn_filter, self.action_filter))

        # Create treeview
        WidgetTreeviewTable.destroy(self.treeview, self.scrollbar)
        trv = WidgetTreeviewTable(
            root=self.root, columns=columns, columns_width=columns_width,
            rows=self._get_treeview_rows(values), callbacks=callbacks
        )
        self.treeview, self.scrollbar = trv()

    def treeview_submenu_view(self, tv: ttk.Treeview) -> None:
        for iid in tv.selection():
            WidgetViewPopup(master=self.root, iid=int(iid))()

    def treeview_submenu_edit(self, tv: ttk.Treeview) -> None:
        for iid in tv.selection():
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

    def _get_treeview_data(self):
        if not FilterStore.submit:
            if self.view_month.value == ViewMonth.LAST.value:
                values = ValueModel.get_last_month()
            else:
                values = ValueModel.get_current_month()
        else:
            values = ValueModel.get_all_filtered(
                date_from=(FilterStore.from_year.get(), hlp.get_month_number(FilterStore.from_month.get())),
                date_to=(FilterStore.to_year.get(), hlp.get_month_number(FilterStore.to_month.get())),
                tags=[tag.id for tag in TagModel.get_checked_tags(FilterStore.tags)]
            )
        return values

    def _get_treeview_rows(self, values):
        rows = []
        for val in values:
            tags = ', '.join([i.name for i in val.get().tags])
            gel = hlp.display_price(val.get().price_gel, val.get().type)
            usd = hlp.display_price(val.get().price_usd, val.get().type)
            rows.append(
                (val.get().id, tags, gel, usd, hlp.date_formated(val.get().date))
            )
        return rows

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
