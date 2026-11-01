"""Пересчёт валют по фиксированным учебным курсам, без сетевых запросов."""

from decimal import Decimal, ROUND_HALF_UP, localcontext
import re


RATES_RUB = {
    "RUB": Decimal("1"),
    "USD": Decimal("90"),
    "EUR": Decimal("100"),
}
CURRENCIES = tuple(RATES_RUB)
MAX_AMOUNT = Decimal("1000000000")


def parse_amount(text: str) -> Decimal:
    """Принять неотрицательную сумму с точкой или запятой и до 2 знаков."""
    if not isinstance(text, str):
        raise TypeError("Сумма должна быть строкой.")
    text = text.strip()
    if not re.fullmatch(r"[0-9]+(?:[.,][0-9]{1,2})?", text):
        raise ValueError("Введите сумму от 0, до двух знаков: 123,45.")
    amount = Decimal(text.replace(",", "."))
    if amount > MAX_AMOUNT:
        raise ValueError("Сумма не должна превышать 1 000 000 000.")
    return amount


def convert_currency(text: str, source: str, target: str) -> Decimal:
    """Пересчитать сумму через RUB и округлить до копеек ROUND_HALF_UP."""
    if not isinstance(source, str) or not isinstance(target, str):
        raise TypeError("Коды валют должны быть строками.")
    if source not in RATES_RUB or target not in RATES_RUB:
        raise ValueError("Выберите валюту RUB, USD или EUR.")
    amount = parse_amount(text)
    with localcontext() as context:
        context.prec = 28
        result = amount * RATES_RUB[source] / RATES_RUB[target]
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
