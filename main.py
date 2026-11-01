"""Запуск графического приложения лабораторной работы №5."""

from lab5.app import ConverterApp


def main() -> None:
    """Создать главное окно и запустить единственный цикл событий."""
    app = ConverterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
