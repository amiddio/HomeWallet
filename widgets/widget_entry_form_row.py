import tkinter as tk


class WidgetEntryFormRow:

    def __init__(self, root: tk, popup,  label: str, text: str = None, is_focus: bool = False) -> None:
        self.root = root
        self.popup = popup
        self.label = label
        self.text = text
        self.is_focus = is_focus

    def __call__(self) -> tk.Entry:
        """
        Widget creating Label and Entry row for form
        :return: None
        """

        # Created conteiner
        container = self.root.get_container_frame(self.popup, columns=[1, 4])

        # Created Label
        tk.Label(container, text=self.label).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # Created Entry
        entry = tk.Entry(
            container, textvariable='' if self.text is None else tk.StringVar(value=self.text),
        )
        entry.grid(row=0, column=1, sticky="we", padx=10, pady=10)

        # Set focus if needed
        if self.is_focus:
            entry.focus_set()

        return entry

