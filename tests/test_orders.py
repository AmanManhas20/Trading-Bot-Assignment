from decimal import Decimal
import unittest

from trading_bot.bot.orders import build_order_payload, summarize_order_response


class BuildOrderPayloadTests(unittest.TestCase):
    def test_market_order_payload_excludes_price(self) -> None:
        payload = build_order_payload(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=Decimal("0.0010"),
        )

        self.assertEqual(
            payload,
            {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "type": "MARKET",
                "quantity": "0.001",
            },
        )

    def test_limit_order_payload_includes_price_and_gtc(self) -> None:
        payload = build_order_payload(
            symbol="BTCUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity=Decimal("1.5000"),
            price=Decimal("80250.00"),
        )

        self.assertEqual(payload["price"], "80250")
        self.assertEqual(payload["timeInForce"], "GTC")

    def test_response_summary_contains_expected_fields(self) -> None:
        payload = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "quantity": "0.001",
        }
        response = {
            "orderId": 12345,
            "status": "FILLED",
            "executedQty": "0.001",
            "avgPrice": "80000.0",
        }

        summary = summarize_order_response(payload, response)

        self.assertIn("Order ID: 12345", summary)
        self.assertIn("Status: FILLED", summary)


if __name__ == "__main__":
    unittest.main()

