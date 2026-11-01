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


if __name__ == "__main__":
    unittest.main()
