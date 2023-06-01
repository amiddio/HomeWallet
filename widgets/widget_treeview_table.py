import tkinter as tk

from functools import partial
from tkinter import ttk


class WidgetTreeviewTable:

    scrollbar: tk.Scrollbar = None
    treeview: ttk.Treeview = None

    def __init__(self, root: tk, columns: tuple, rows: list, callbacks: dict = None) -> None:
        self.root = root
        self.columns = columns
        self.rows = rows
        self.callbacks = callbacks

    def __call__(self) -> tuple[ttk.Treeview, tk.Scrollbar]:
        """
        Widget table with data and scrollbar
        :return: tuple[ttk.Treeview, tk.Scrollbar]
        """

        def display_menu(event):
            iid = self.treeview.identify_row(event.y)
            if iid:
                self.treeview.selection_set(iid)
                self.treeview.menu.post(event.x_root, event.y_root)

        # Create widgets
        self.scrollbar = tk.Scrollbar(self.root)
        self.treeview = ttk.Treeview(self.root)

        # Configure widgets
        self.treeview.config(columns=self.columns, show='headings')
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.treeview.yview)

        # Create menu if needed
        if self.callbacks is not None:
            self.treeview.bind("<Button-3>", display_menu)  # Bind
            self.treeview.menu = tk.Menu(self.root, tearoff=0)
            for k, v in self.callbacks.items():
                self.treeview.menu.add_command(label=k.capitalize(), command=partial(v, self.treeview))

        # Define headings and columns
        for i, item in enumerate(self.columns, 1):
            self.treeview.column(f"# {i}", width=30 if i > 1 else 150)
            self.treeview.heading(item, text=item.capitalize(), anchor='w')

        # Display widget
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=(10, 0))
        self.treeview.pack(expand=True, fill='both', side='top', padx=0, pady=(10, 0))

        # Filling treeview widget
        for row in self.rows:
            row_id, *d = row
            self.treeview.insert(parent='', index='end', iid=row_id, values=d)

        return self.treeview, self.scrollbar

    @staticmethod
    def destroy(treeview: ttk.Treeview, scrollbar: tk.Scrollbar) -> None:
        """
        Destroy treeview and scrollbar if exist
        :param treeview: ttk.Treeview
        :param scrollbar: tk.Scrollbar
        :return: None
        """
        if treeview and scrollbar:
            treeview.destroy()
            scrollbar.destroy()
