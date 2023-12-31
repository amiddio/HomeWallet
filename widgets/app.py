import tkinter as tk

from tkinter import ttk
from tkinter.ttk import Frame
from typing import Callable

from config_data.config import load_config, Config
from widgets.menu import Menu
from widgets.values import Values, ViewMonth


class App(tk.Tk):

    # ------------------------------------------------------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self.config_: Config = load_config()

        # Configuration app main window
        self._window_resizable(self)
        self._window_geometry(self)
        self._window_minsize(self)
        App._window_title(self, self.config_.window_app_title)
        App._window_ico(self)
        App._window_styling()

        # Created menu
        Menu(self)
        # Opened values widget
        Values(self, view_month=ViewMonth.CURRENT)

    # ------------------------------------------------------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------------------------------------------------------

    def clear_window(self) -> None:
        for widget in self.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()

    def get_container_frame(self, master: tk, columns: list[int], background: str = None) -> tk.Frame:
        container = tk.Frame(master)
        if background:
            container.configure(background=background)
        container.pack(side="top", fill="both")
        for index, weight in enumerate(columns):
            container.grid_columnconfigure(index, weight=weight)
        return container

    def get_page_header(self, master: tk, title: str,
                        btn_text: str = None, bg_color: str = None) -> ttk.Button | None:
        container = self.get_container_frame(master, columns=[10, 1], background=bg_color)
        tk.Label(container, text=title, font=("Calibri", 16, 'bold'), background=bg_color) \
            .grid(row=0, column=0, sticky="w", padx=15, pady=10)
        if btn_text:
            btn = ttk.Button(container, style='Manage.TButton', text=btn_text)
            btn.grid(row=0, column=1, sticky="e", padx=15, pady=10)
            return btn
        return

    def close_popup_action(self, popup: tk.Toplevel, btn: ttk.Button) -> Callable:

        # Set button to normal after popup closed
        def close_popup():
            btn.configure(state=tk.NORMAL)
            popup.destroy()

        # Disabled button after clicked
        btn.configure(state=tk.DISABLED)
        popup.protocol('WM_DELETE_WINDOW', close_popup)

        return close_popup

    def popup(self, window_title: str, less_by_x: int, less_by_y: int) -> tk.Toplevel:
        popup = tk.Toplevel()
        self._window_resizable(popup, is_not_resizable=True)
        self._window_geometry(popup, less_by_x, less_by_y)
        self._window_minsize(popup)
        App._window_title(popup, window_title)
        App._window_ico(popup)
        App._window_styling()
        return popup

    @staticmethod
    def select_box_filter(
            container: Frame, data: list[str | int], label: str, column: int, selected: str | int
    ) -> tk.StringVar:
        values = tk.StringVar()
        if selected is not None:
            values.set(selected)
        if data:
            ttk.Label(container, text=label, style='dropdown-label.TLabel')\
                .grid(row=0, column=column, sticky='w', padx=10, pady=(10, 5))
            om = tk.OptionMenu(container, values, *data, command=None)
            om.grid(row=1, column=column, sticky='w', padx=10, pady=(5, 10))
        return values

    # ------------------------------------------------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------------------------------------------------

    def _window_geometry(self, window: tk, less_by_x: int = 0, less_by_y: int = 0) -> None:

        # set window width/heignt
        window_width = int(self.config_.window_width) - less_by_x
        window_height = int(self.config_.window_height) - less_by_y

        # get the screen size computer
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # gets both half the screen width/height and window width/height
        position_right = int(screen_width / 2 - window_width / 2)
        position_top = int(screen_height / 2 - window_height / 2)

        # window configure
        window.geometry('{}x{}+{}+{}'.format(window_width, window_height, position_right, position_top))

    def _window_resizable(self, window: tk, is_not_resizable: bool = False) -> None:
        if is_not_resizable:
            window.resizable(False, False)
        else:
            window.resizable(self.config_.window_resizable, self.config_.window_resizable)

    def _window_minsize(self, window: tk):
        window.minsize(self.config_.window_width_min, self.config_.window_height_min)

    @staticmethod
    def _window_title(window: tk, title: str) -> None:
        window.title(title)

    @staticmethod
    def _window_ico(window: tk) -> None:
        window.iconbitmap(r'./app.ico')

    @staticmethod
    def _window_styling() -> None:
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=('Calibri', 12, 'bold'))
        style.configure("Treeview", font=('Calibri', 12), rowheight=40)
        style.configure("dropdown-label.TLabel", font=('Calibri', 12), background='#f0f0f0')
