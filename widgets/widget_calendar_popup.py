import tkinter as tk
import helper as hlp

from tkinter import ttk
from tkcalendar import Calendar
from lang_pack.lang import LANG_GENERAL
from logger.logger import log


class WidgetCalendarPopup:

    POPUP_WIDTH = 251
    POPUP_HEIGHT = 236

    def __init__(self, master: tk, date) -> None:
        self.master = master
        self.date = date

    def __call__(self, *args, **kwargs) -> None:

        def on_closing() -> None:
            try:
                popup.destroy()
                self.date.configure(textvariable=tk.StringVar(value=str(cal.selection_get())))
            except Exception as e:
                log().error(e)

        # Created popup
        popup = tk.Toplevel()
        self._window_geometry(popup)
        popup.protocol("WM_DELETE_WINDOW", on_closing)

        y, m, d = hlp.get_year_month_day(self.date.get())
        # Created calendar and selected year, month, day
        cal = Calendar(popup, selectmode='day', year=y, month=m, day=d)
        cal.grid(row=0, column=0, padx=0, pady=0)
        # Created select button
        btn = ttk.Button(popup, style='Manage.TButton', text=LANG_GENERAL["select"], width=10)
        btn.configure(command=on_closing)
        btn.grid(row=1, column=0, padx=0, pady=10)

    def _window_geometry(self, window: tk) -> None:
        # get the screen size computer
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # gets both half the screen width/height and window width/height
        position_right = int(screen_width / 2 - WidgetCalendarPopup.POPUP_WIDTH / 2)
        position_top = int(screen_height / 2 - WidgetCalendarPopup.POPUP_HEIGHT / 2)

        # window configure
        window.geometry('{}x{}+{}+{}'.format(
                WidgetCalendarPopup.POPUP_WIDTH, WidgetCalendarPopup.POPUP_HEIGHT, position_right, position_top
            )
        )
        window.resizable(False, False)
