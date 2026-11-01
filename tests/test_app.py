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


if __name__ == "__main__":
    unittest.main()
