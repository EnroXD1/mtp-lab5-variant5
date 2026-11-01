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
