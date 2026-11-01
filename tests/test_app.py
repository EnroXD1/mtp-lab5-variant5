"""Проверки настоящих виджетов Tkinter; требуется графическая среда."""

import tkinter as tk
import unittest

from lab5.app import ConverterApp


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.app = ConverterApp()
        self.app.withdraw()
        self.app.update_idletasks()

    def tearDown(self):
        try:
            self.app.destroy()
        except tk.TclError:
            pass

    def test_notebook_has_two_named_tabs(self):
        tabs = self.app.notebook.tabs()
        self.assertEqual(len(tabs), 2)
        self.assertEqual(
            [self.app.notebook.tab(tab, "text") for tab in tabs],
            ["Приветствие", "Конвертер"],
        )

    def test_tabs_can_be_selected(self):
        self.app.notebook.select(self.app.converter_tab)
        self.assertEqual(
            self.app.notebook.select(), str(self.app.converter_tab),
        )
        self.app.notebook.select(self.app.greeting_tab)
        self.assertEqual(
            self.app.notebook.select(), str(self.app.greeting_tab),
        )

    def test_file_menu_contains_exit(self):
        menu = self.app.nametowidget(self.app.cget("menu"))
        self.assertEqual(menu.entrycget(1, "label"), "File")
        self.assertEqual(self.app.file_menu.entrycget(0, "label"), "Exit")

    def test_exit_menu_destroys_main_window(self):
        self.app.file_menu.invoke(0)
        self.assertEqual(self.app.tk.call("info", "commands", "."), "")

    def test_greeting_button_updates_label(self):
        self.app.name_var.set("  Илья  ")
        self.app.greet_button.invoke()
        self.assertEqual(self.app.greeting_var.get(), "Привет, Илья!")

    def test_empty_name_gives_general_greeting(self):
        self.app.name_var.set("  ")
        self.app.greet_button.invoke()
        self.assertEqual(self.app.greeting_var.get(), "Привет!")

    def test_conversion_button_updates_result(self):
        self.app.convert_button.invoke()
        self.assertEqual(self.app.result_var.get(), "100 USD = 9000.00 RUB")
        self.assertEqual(self.app.error_var.get(), "")

    def test_currency_lists_are_readonly(self):
        for widget in (self.app.source_box, self.app.target_box):
            self.assertEqual(str(widget.cget("state")), "readonly")
            self.assertEqual(
                tuple(widget.cget("values")), ("RUB", "USD", "EUR"),
            )

    def test_error_clears_previous_result(self):
        self.app.convert_button.invoke()
        self.app.amount_var.set("-5")
        self.app.convert_button.invoke()
        self.assertEqual(self.app.result_var.get(), "")
        self.assertIn("Введите сумму", self.app.error_var.get())

    def test_valid_input_clears_error(self):
        self.app.amount_var.set("abc")
        self.app.convert_button.invoke()
        self.app.amount_var.set("1,50")
        self.app.convert_button.invoke()
        self.assertEqual(self.app.result_var.get(), "1,50 USD = 135.00 RUB")
        self.assertEqual(self.app.error_var.get(), "")

    def test_editing_each_input_clears_stale_result(self):
        for variable, value in (
            (self.app.amount_var, "200"),
            (self.app.source_var, "EUR"),
            (self.app.target_var, "USD"),
        ):
            with self.subTest(value=value):
                self.app.convert_button.invoke()
                self.assertTrue(self.app.result_var.get())
                variable.set(value)
                self.assertEqual(self.app.result_var.get(), "")

    def test_rates_button_opens_second_window(self):
        self.app.rates_button.invoke()
        window = self.app.rates_window
        self.assertIsInstance(window, tk.Toplevel)
        self.assertEqual(window.title(), "Учебные курсы")
        self.assertEqual(str(window.master), str(self.app))

    def test_repeated_open_reuses_rates_window(self):
        self.app.show_rates()
        first = self.app.rates_window
        self.app.show_rates()
        self.assertIs(self.app.rates_window, first)

    def test_rates_window_can_be_closed_and_reopened(self):
        self.app.show_rates()
        first = self.app.rates_window
        self.app.close_rates()
        self.assertFalse(first.winfo_exists())
        self.assertIsNone(self.app.rates_window)
        self.assertTrue(self.app.winfo_exists())
        self.app.show_rates()
        self.assertIsNot(self.app.rates_window, first)

    def test_window_manager_close_uses_same_handler(self):
        self.app.show_rates()
        window = self.app.rates_window
        command = window.protocol("WM_DELETE_WINDOW")
        window.tk.call(command)
        self.assertFalse(window.winfo_exists())
        self.assertIsNone(self.app.rates_window)

    def test_exit_also_closes_child_window(self):
        self.app.show_rates()
        window_path = str(self.app.rates_window)
        self.app.file_menu.invoke(0)
        self.assertEqual(
            self.app.tk.call("info", "commands", window_path), "",
        )


if __name__ == "__main__":
    unittest.main()
