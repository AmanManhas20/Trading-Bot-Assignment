import unittest
from decimal import Decimal

from trading_bot.bot.validators import (
    normalize_order_type,
    normalize_side,
    normalize_symbol,
    parse_positive_decimal,
    validate_price_requirement,
)


class ValidatorTests(unittest.TestCase):
    def test_symbol_is_normalized_to_uppercase(self) -> None:
        self.assertEqual(normalize_symbol(" btcusdt "), "BTCUSDT")

    def test_symbol_must_be_usdt_pair(self) -> None:
        with self.assertRaisesRegex(ValueError, "USDT-M pair"):
            normalize_symbol("BTCUSD")

    def test_side_must_be_buy_or_sell(self) -> None:
        with self.assertRaisesRegex(ValueError, "BUY or SELL"):
            normalize_side("hold")

    def test_order_type_must_be_market_or_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "MARKET or LIMIT"):
            normalize_order_type("stop")

    def test_decimal_must_be_positive(self) -> None:
        self.assertEqual(parse_positive_decimal("0.25", "quantity"), Decimal("0.25"))
        with self.assertRaisesRegex(ValueError, "greater than 0"):
            parse_positive_decimal("0", "quantity")

    def test_limit_price_is_required(self) -> None:
        with self.assertRaisesRegex(ValueError, "required for LIMIT"):
            validate_price_requirement("LIMIT", None)

    def test_market_price_must_not_be_provided(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be provided"):
            validate_price_requirement("MARKET", Decimal("1"))


if __name__ == "__main__":
    unittest.main()
