"""Главное окно и обработчики событий учебного приложения."""

import tkinter as tk
from tkinter import ttk


class ConverterApp(tk.Tk):
    """Окно с двумя вкладками для заданий варианта 5."""

    def __init__(self) -> None:
        super().__init__()
        self.title("МТП - лабораторная №5")
        self.geometry("720x480")
        self.minsize(640, 420)
        self._build_menu()

        ttk.Label(
            self, text="Практика Tkinter", font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w", padx=24, pady=(20, 4))
        ttk.Label(
            self, text="Вариант 5: вкладки, события и несколько окон",
        ).pack(anchor="w", padx=24, pady=(0, 16))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self.greeting_tab = ttk.Frame(self.notebook, padding=20)
        self.converter_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.greeting_tab, text="Приветствие")
        self.notebook.add(self.converter_tab, text="Конвертер")
        self.notebook.enable_traversal()
        self._build_greeting()

    def _build_menu(self) -> None:
        menu = tk.Menu(self)
        self.file_menu = tk.Menu(menu, tearoff=False)
        self.file_menu.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(label="File", menu=self.file_menu, underline=0)
        self.configure(menu=menu)

    def _build_greeting(self) -> None:
        self.name_var = tk.StringVar(value="Илья")
        self.greeting_var = tk.StringVar(value="Нажмите кнопку «Привет».")
        ttk.Label(self.greeting_tab, text="Ваше имя:").pack(anchor="w")
        self.name_entry = ttk.Entry(
            self.greeting_tab, textvariable=self.name_var, width=32,
        )
        self.name_entry.pack(anchor="w", pady=(6, 14))
        self.name_entry.bind("<Return>", self.greet)
        self.greet_button = ttk.Button(
            self.greeting_tab, text="Привет", command=self.greet,
        )
        self.greet_button.pack(anchor="w")
        ttk.Label(
            self.greeting_tab,
            textvariable=self.greeting_var,
            font=("Segoe UI", 14),
            wraplength=540,
        ).pack(anchor="w", pady=24)

    def greet(self, _event: tk.Event | None = None) -> None:
        """Обновить приветствие по нажатию кнопки или Enter."""
        name = self.name_var.get().strip()
        self.greeting_var.set(f"Привет, {name}!" if name else "Привет!")
