"""Проверки валидации и расчётов независимо от графического интерфейса."""

from decimal import Decimal, localcontext
import unittest

from lab5.currency import convert_currency, parse_amount


class AmountTests(unittest.TestCase):
    def test_integer_dot_comma_and_whitespace(self):
        for text in ("123.45", "123,45", " 123,45 "):
            with self.subTest(text=text):
                self.assertEqual(parse_amount(text), Decimal("123.45"))
        self.assertEqual(parse_amount("123"), Decimal("123"))

    def test_zero_and_maximum(self):
        self.assertEqual(parse_amount("0"), Decimal("0"))
        self.assertEqual(parse_amount("1000000000"), Decimal("1000000000"))

    def test_invalid_amounts(self):
        for text in (
            "", " ", "-1", "abc", "NaN", "Infinity", "1e3",
            "1.234", "1,2.3", "1 000", "0.", "1000000000.01",
        ):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_amount(text)

    def test_non_string_amount(self):
        for value in (True, False, 10, 1.5, None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    parse_amount(value)


class ConversionTests(unittest.TestCase):
    def test_usd_to_rub(self):
        self.assertEqual(
            convert_currency("100", "USD", "RUB"), Decimal("9000.00"),
        )

    def test_rub_to_usd(self):
        self.assertEqual(
            convert_currency("9000", "RUB", "USD"), Decimal("100.00"),
        )

    def test_cross_currency_conversion(self):
        self.assertEqual(
            convert_currency("100", "EUR", "USD"), Decimal("111.11"),
        )

    def test_same_currency(self):
        self.assertEqual(
            convert_currency("123,45", "EUR", "EUR"), Decimal("123.45"),
        )

    def test_zero(self):
        self.assertEqual(convert_currency("0", "USD", "EUR"), Decimal("0.00"))

    def test_half_cent_rounds_up(self):
        self.assertEqual(
            convert_currency("0.05", "USD", "EUR"), Decimal("0.05"),
        )

    def test_maximum_amount(self):
        self.assertEqual(
            convert_currency("1000000000", "EUR", "RUB"),
            Decimal("100000000000.00"),
        )

    def test_unknown_currency(self):
        for source, target in (("GBP", "RUB"), ("USD", "")):
            with self.subTest(source=source, target=target):
                with self.assertRaises(ValueError):
                    convert_currency("10", source, target)

    def test_non_string_currency(self):
        with self.assertRaises(TypeError):
            convert_currency("10", None, "RUB")

    def test_invalid_amount_is_rejected_by_conversion(self):
        with self.assertRaises(ValueError):
            convert_currency("-1", "USD", "RUB")

    def test_callers_decimal_precision_is_preserved(self):
        with localcontext() as context:
            context.prec = 5
            self.assertEqual(
                convert_currency("1000000", "EUR", "RUB"),
                Decimal("100000000.00"),
            )
            self.assertEqual(context.prec, 5)


if __name__ == "__main__":
    unittest.main()
