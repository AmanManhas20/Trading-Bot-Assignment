from __future__ import annotations

import argparse
import logging
import os
import sys
from decimal import Decimal

from trading_bot.bot.client import BinanceClientError, BinanceFuturesClient
from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import build_order_payload, submit_order, summarize_order_response
from trading_bot.bot.validators import (
    normalize_order_type,
    normalize_side,
    normalize_symbol,
    parse_positive_decimal,
    validate_price_requirement,
)

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place Binance Futures Testnet orders from the command line."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument(
        "--order-type",
        required=True,
        dest="order_type",
        help="MARKET or LIMIT",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Required for LIMIT orders")
    parser.add_argument(
        "--base-url",
        default=os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com"),
        help="Binance Futures API base URL",
    )
    return parser


def load_credentials() -> tuple[str, str]:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your environment"
        )
    return api_key, api_secret


def main() -> int:
    log_file = setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    try:
        symbol = normalize_symbol(args.symbol)
        side = normalize_side(args.side)
        order_type = normalize_order_type(args.order_type)
        quantity = parse_positive_decimal(args.quantity, "quantity")
        price = (
            parse_positive_decimal(args.price, "price")
            if args.price is not None
            else None
        )
        validate_price_requirement(order_type, price)

        api_key, api_secret = load_credentials()
        client = BinanceFuturesClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=args.base_url,
        )

        payload = build_order_payload(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
        response = submit_order(client, payload)
        print(summarize_order_response(payload, response))
        print(f"\nSuccess. Logs written to: {log_file}")
        return 0

    except ValueError as exc:
        LOGGER.exception("Validation error")
        print(f"Failure: {exc}")
        print(f"Logs written to: {log_file}")
        return 2
    except BinanceClientError as exc:
        LOGGER.exception("Binance client error")
        print(f"Failure: {exc}")
        print(f"Logs written to: {log_file}")
        return 1
    except Exception as exc:  # pragma: no cover
        LOGGER.exception("Unexpected error")
        print(f"Failure: unexpected error: {exc}")
        print(f"Logs written to: {log_file}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

