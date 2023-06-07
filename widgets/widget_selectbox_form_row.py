import tkinter as tk


class WidgetSelectboxFormRow:

    def __init__(self, root: tk, popup, label: str, data, fill: str = None) -> None:
        self.root = root
        self.popup = popup
        self.label = label
        self.data = data
        self.fill = fill

    def __call__(self):
        # Created container
        container = self.root.get_container_frame(self.popup, columns=[1, 10])

        # Created Label
        tk.Label(container, text=self.label, width=20).grid(row=0, column=0, sticky='w', padx=(5, 10), pady=10)

        values = tk.StringVar()
        if self.fill:
            values.set(self.fill.value)
        om = tk.OptionMenu(container, values, *self.data, command=None)
        om.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        return values
