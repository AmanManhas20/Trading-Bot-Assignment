from __future__ import annotations

from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def normalize_symbol(symbol: str) -> str:
    cleaned = (symbol or "").strip().upper()
    if not cleaned:
        raise ValueError("symbol is required")
    if not cleaned.endswith("USDT"):
        raise ValueError("symbol must be a USDT-M pair such as BTCUSDT")
    return cleaned


def normalize_side(side: str) -> str:
    cleaned = (side or "").strip().upper()
    if cleaned not in VALID_SIDES:
        raise ValueError("side must be BUY or SELL")
    return cleaned


def normalize_order_type(order_type: str) -> str:
    cleaned = (order_type or "").strip().upper()
    if cleaned not in VALID_ORDER_TYPES:
        raise ValueError("order_type must be MARKET or LIMIT")
    return cleaned


def parse_positive_decimal(raw_value: str, field_name: str) -> Decimal:
    try:
        value = Decimal(str(raw_value))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError(f"{field_name} must be a valid number") from exc

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")
    return value


def validate_price_requirement(order_type: str, price: Decimal | None) -> None:
    if order_type == "LIMIT" and price is None:
        raise ValueError("price is required for LIMIT orders")
    if order_type == "MARKET" and price is not None:
        raise ValueError("price must not be provided for MARKET orders")

