from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any

from trading_bot.bot.client import BinanceFuturesClient

LOGGER = logging.getLogger(__name__)


def build_order_payload(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Decimal,
    price: Decimal | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": format_decimal(quantity),
    }

    if order_type == "LIMIT":
        payload["price"] = format_decimal(price)
        payload["timeInForce"] = "GTC"

    return payload


def submit_order(
    client: BinanceFuturesClient,
    payload: dict[str, Any],
) -> dict[str, Any]:
    LOGGER.info("Submitting order payload: %s", payload)
    response = client.place_order(payload)
    LOGGER.info("Binance order response: %s", response)
    return response


def summarize_order_response(
    payload: dict[str, Any],
    response: dict[str, Any],
) -> str:
    lines = [
        "Order request summary:",
        f"  Symbol: {payload['symbol']}",
        f"  Side: {payload['side']}",
        f"  Type: {payload['type']}",
        f"  Quantity: {payload['quantity']}",
    ]
    if payload["type"] == "LIMIT":
        lines.append(f"  Price: {payload['price']}")

    lines.extend(
        [
            "",
            "Order response details:",
            f"  Order ID: {response.get('orderId', 'N/A')}",
            f"  Status: {response.get('status', 'N/A')}",
            f"  Executed Quantity: {response.get('executedQty', 'N/A')}",
            f"  Average Price: {response.get('avgPrice', 'N/A')}",
        ]
    )
    return "\n".join(lines)


def format_decimal(value: Decimal | None) -> str:
    if value is None:
        raise ValueError("Decimal value is required")
    normalized = value.normalize()
    return format(normalized, "f")

