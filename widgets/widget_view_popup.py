import tkinter as tk
import tkinter.messagebox as mb
import helper as hlp

from tkinter.scrolledtext import ScrolledText
from lang_pack.lang import LANG_GENERAL, LANG_COLORS, LANG_MSG
from logger.logger import log
from models.scheme import TypeEnum
from models.value_model import ValueModel
from tkinter import ttk


class WidgetViewPopup:
    """
    Widget popup for display value details
    """

    value: ValueModel = None

    def __init__(self, master: tk, iid: int) -> None:
        self.master = master
        self.iid = iid

    def __call__(self) -> None:
        try:
            self.value = ValueModel.get_by_id(iid=self.iid)
            if not self.value:
                raise TypeError(LANG_MSG["this value not found"])

            # Create popup
            popup = self.master.popup(window_title=LANG_GENERAL["view value"], less_by_x=200, less_by_y=650)
            # Add popup header
            self.master.get_page_header(
                popup, title=LANG_GENERAL["view value title"].format(type=self.value.get().type.value),
                bg_color=LANG_COLORS["header_bg"]
            )
            self._get_price_section(popup=popup)  # Add price section
            self._get_message_section(popup=popup)  # Add message section
        except TypeError as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["validation error"], str(e))
        except Exception as e:
            log().error(e)
            mb.showerror(LANG_GENERAL["internal error"], str(e))

    def _get_price_section(self, popup: tk.Toplevel) -> None:
        """
        Display labels with prices, date and tags string
        :param popup: tk.Toplevel
        :return: None
        """

        gel = LANG_GENERAL["gel"].format(price=hlp.display_price(self.value.get().price_gel, self.value.get().type))
        usd = LANG_GENERAL["usd"].format(price=hlp.display_price(self.value.get().price_usd, self.value.get().type))
        dt = hlp.date_formated(self.value.get().date)
        tags = LANG_GENERAL["tags"] + ': ' + ', '.join([tag.name for tag in self.value.get().tags])
        price_fg = LANG_COLORS["price_red"] if self.value.get().type == TypeEnum.VOUT else LANG_COLORS["price_green"]

        container = self.master.get_container_frame(popup, columns=[1, 1, 1])
        tk.Label(container, text=gel, fg=price_fg, font=("Calibri", 16, 'bold')) \
            .grid(row=0, column=0, sticky="we", padx=10, pady=10)
        tk.Label(container, text=usd, fg=price_fg, font=("Calibri", 16, 'bold')) \
            .grid(row=0, column=1, sticky="we", padx=10, pady=10)
        tk.Label(container, text=dt, font=("Calibri", 14)) \
            .grid(row=0, column=2, sticky="we", padx=10, pady=10)
        ttk.Separator(container, orient='horizontal')\
            .grid(row=1, column=0, columnspan=3, sticky="we", padx=10, pady=(10, 0))
        tk.Label(container, text=tags, font=("Calibri", 14)) \
            .grid(row=2, column=0, columnspan=3, sticky="w", padx=10, pady=10)

    def _get_message_section(self, popup: tk.Toplevel) -> None:
        """
        Display message of value
        :param popup: tk.Toplevel
        :return: None
        """

        #if self.value.get().message:
        container = self.master.get_container_frame(popup, columns=[1])
        text_area = ScrolledText(container, wrap=tk.WORD, height=7)
        text_area.insert(tk.INSERT, self.value.get().message)
        text_area.configure(state='disabled')
        text_area.grid(row=0, column=0, sticky="we", pady=10, padx=10)
