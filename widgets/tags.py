import tkinter as tk
import tkinter.messagebox as mb

from functools import partial
from tkinter import ttk
from typing import Callable
from sqlalchemy import asc

from lang_pack.lang import LANG_GENERAL, LANG_COLORS, LANG_MSG
from logger.logger import log
from models.tag_model import TagModel
from widgets.widget_entry_form_row import WidgetEntryFormRow
from widgets.widget_treeview_table import WidgetTreeviewTable


class Tags:
    entry_name = None
    btn_add = None
    treeview = None
    scrollbar = None

    # ------------------------------------------------------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, root: tk) -> None:
        super().__init__()

        self.root = root

        self.root.clear_window()

        # Add page header
        self.btn_add = self.root.get_page_header(
            self.root, title=LANG_GENERAL["tags"], btn_text=LANG_GENERAL["add"],
            bg_color=LANG_COLORS["header_bg"], btn_callback=self.open_popup
        )

        # Create treeview
        self.tags_treevew()

    # ------------------------------------------------------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------------------------------------------------------

    def open_popup(self, iid: int = None) -> None:
        """
        Open popup after button add clicked
        :param iid: int
        :return: None
        """

        # Disabled button after clicked
        self.btn_add.configure(state=tk.DISABLED)

        # Create popup
        popup = self.root.popup(window_title=LANG_GENERAL["add tag"], less_by_x=200, less_by_y=600)

        # Set button to normal after popup closed
        def close_popup():
            self.btn_add.configure(state=tk.NORMAL)
            popup.destroy()
        popup.protocol('WM_DELETE_WINDOW', close_popup)

        # Add popup header
        self.root.get_page_header(
            popup, title=LANG_GENERAL["add tag"], btn_text=LANG_GENERAL["save"],
            bg_color=LANG_COLORS["header_bg"], btn_callback=partial(self.save_tag, close_popup, iid)
        )
        # Add name entry
        self.entry_name = WidgetEntryFormRow(
            root=self.root, popup=popup, label=LANG_GENERAL["tag name"], is_focus=True,
            text=TagModel.get_by_id(iid=iid).get().name if iid else ''
        )()

    def save_tag(self, close_popup: Callable, iid: int = None) -> None:
        """
        Save tag
        :param close_popup: Callable
        :param iid: int
        :return: None
        """

        try:
            name = self.entry_name.get().strip()

            # Validate name is required
            if not name:
                raise TypeError("Field Name is required")

            tag = TagModel.get_by_id(iid=iid)

            # Validate if tag already exist
            is_exist = TagModel.is_exist(name=name)
            if is_exist and is_exist.get().id != tag.get().id:
                raise TypeError(f"Tag '{name}' already exist")

            # Save tag
            if tag:
                tag.set(name=name)
                result = tag.save()
            else:
                result = TagModel(name=name).save()

            # If success
            if result:
                msg = LANG_MSG["tag '{name}' saved successfully"].format(name=name)
                log().info(msg)
                mb.showinfo(LANG_GENERAL["info"], msg)
                self.tags_treevew()  # Refresh treeview
                close_popup()  # Close popup
        except TypeError as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["validation error"], str(e))
        except Exception as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["internal error"], str(e))

    def tags_treevew(self) -> None:
        """
        Dispay list of tags
        :return: None
        """

        # Prepare data to treeview
        columns = (LANG_GENERAL["tag name"],)
        data = []
        for tag in TagModel.get_all(order_={'name': asc}):
            data.append((tag.get().id, tag.get().name))
        callbacks = {
            LANG_GENERAL["edit"]: self.treeview_submenu_edit,
            LANG_GENERAL["delete"]: self.treeview_submenu_delete
        }

        # Create treeview
        WidgetTreeviewTable.destroy(self.treeview, self.scrollbar)
        trv = WidgetTreeviewTable(root=self.root, columns=columns, rows=data, callbacks=callbacks)
        self.treeview, self.scrollbar = trv()

    def treeview_submenu_edit(self, tv: ttk.Treeview) -> None:
        """
        Edit tag action after submenu clicked
        :param tv: ttk.Treeview
        :return: None
        """

        for iid in tv.selection():
            self.open_popup(iid=int(iid))

    def treeview_submenu_delete(self, tv: ttk.Treeview) -> None:
        """
        Delete tag action after submenu clicked
        :param tv: ttk.Treeview
        :return: None
        """

        try:
            if mb.askyesno(message=LANG_MSG["are you sure to delete this tag"], title=LANG_GENERAL["yesno"]):
                for iid in tv.selection():
                    tag = TagModel.get_by_id(iid=int(iid))
                    if tag:
                        tv.delete(iid)
                        tag.delete()
                        msg = LANG_MSG["tag '{tag}' deleted successfully"].format(tag=tag.get().name)
                        mb.showinfo(LANG_GENERAL["info"], msg)
                        log().info(msg)
        except Exception as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["internal error"], str(e))


