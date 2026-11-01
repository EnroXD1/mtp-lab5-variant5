"""Главное окно и обработчики событий учебного приложения."""

import tkinter as tk
from tkinter import ttk

from lab5.currency import CURRENCIES, RATES_RUB, convert_currency


class ConverterApp(tk.Tk):
    """Окно с двумя вкладками для заданий варианта 5."""

    def __init__(self) -> None:
        super().__init__()
        self.title("МТП - лабораторная №5")
        self.geometry("760x540")
        self.minsize(700, 500)
        self.rates_window: tk.Toplevel | None = None
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
        self._build_converter()

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

    def _build_converter(self) -> None:
        frame = self.converter_tab
        self.amount_var = tk.StringVar(value="100")
        self.source_var = tk.StringVar(value="USD")
        self.target_var = tk.StringVar(value="RUB")
        self.result_var = tk.StringVar()
        self.error_var = tk.StringVar()

        ttk.Label(
            frame, text="Конвертер валют", font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 18))
        for column, text in enumerate(("Сумма", "Из", "В")):
            frame.columnconfigure(column, weight=1)
            ttk.Label(frame, text=text).grid(
                row=1, column=column, sticky="w",
            )
        self.amount_entry = ttk.Entry(frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=2, column=0, sticky="ew", padx=(0, 16))
        self.amount_entry.bind("<Return>", self.calculate)
        self.source_box = ttk.Combobox(
            frame, textvariable=self.source_var, values=CURRENCIES,
            state="readonly", width=10,
        )
        self.source_box.grid(row=2, column=1, sticky="ew", padx=(0, 16))
        self.target_box = ttk.Combobox(
            frame, textvariable=self.target_var, values=CURRENCIES,
            state="readonly", width=10,
        )
        self.target_box.grid(row=2, column=2, sticky="ew")
        self.convert_button = ttk.Button(
            frame, text="Перевести", command=self.calculate,
        )
        self.convert_button.grid(row=3, column=0, sticky="w", pady=18)
        self.rates_button = ttk.Button(
            frame, text="Показать курсы", command=self.show_rates,
        )
        self.rates_button.grid(row=3, column=1, columnspan=2, sticky="w")
        ttk.Label(
            frame, textvariable=self.result_var,
            font=("Segoe UI", 14, "bold"), wraplength=560,
        ).grid(row=4, column=0, columnspan=3, sticky="w", pady=(8, 12))
        ttk.Label(
            frame, textvariable=self.error_var, foreground="#b3261e",
            wraplength=560,
        ).grid(row=5, column=0, columnspan=3, sticky="w")
        ttk.Label(
            frame,
            text=("Учебные фиксированные курсы: 1 USD = 90 RUB, "
                  "1 EUR = 100 RUB. Данные не загружаются из интернета."),
            wraplength=560,
        ).grid(row=6, column=0, columnspan=3, sticky="w", pady=20)
        for variable in (self.amount_var, self.source_var, self.target_var):
            variable.trace_add("write", self.clear_conversion)

    def clear_conversion(self, *_args) -> None:
        """Очистить устаревший результат при изменении входных данных."""
        self.result_var.set("")
        self.error_var.set("")

    def calculate(self, _event: tk.Event | None = None) -> None:
        """Выполнить пересчёт или показать ошибку рядом с полями."""
        self.clear_conversion()
        source, target = self.source_var.get(), self.target_var.get()
        try:
            result = convert_currency(self.amount_var.get(), source, target)
        except ValueError as error:
            self.error_var.set(str(error))
            return
        amount = self.amount_var.get().strip()
        self.result_var.set(f"{amount} {source} = {result:.2f} {target}")

    def show_rates(self) -> None:
        """Открыть дополнительное окно или поднять уже существующее."""
        if self.rates_window is not None and self.rates_window.winfo_exists():
            self.rates_window.lift()
            self.rates_window.focus_set()
            return

        window = tk.Toplevel(self)
        self.rates_window = window
        window.title("Учебные курсы")
        window.transient(self)
        window.resizable(False, False)
        window.geometry(
            f"+{self.winfo_rootx() + 100}+{self.winfo_rooty() + 100}",
        )
        window.protocol("WM_DELETE_WINDOW", self.close_rates)
        frame = ttk.Frame(window, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(
            frame, text="Фиксированные учебные курсы",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 12))
        for code, rate in RATES_RUB.items():
            ttk.Label(frame, text=f"1 {code} = {rate:f} RUB").pack(
                anchor="w", pady=3,
            )
        ttk.Label(
            frame, text="Это примеры для расчётов, а не текущие курсы.",
            wraplength=320,
        ).pack(anchor="w", pady=14)
        ttk.Button(frame, text="Закрыть", command=self.close_rates).pack(
            anchor="e",
        )

    def close_rates(self) -> None:
        """Закрыть только окно курсов, сохранив главное окно."""
        if self.rates_window is not None and self.rates_window.winfo_exists():
            self.rates_window.destroy()
        self.rates_window = None
