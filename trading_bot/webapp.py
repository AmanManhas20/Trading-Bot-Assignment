from __future__ import annotations

import json
import logging
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from trading_bot.bot.client import BinanceClientError, BinanceFuturesClient
from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import build_order_payload, submit_order
from trading_bot.bot.validators import (
    normalize_order_type,
    normalize_side,
    normalize_symbol,
    parse_positive_decimal,
    validate_price_requirement,
)

LOGGER = logging.getLogger(__name__)
STATIC_DIR = Path(__file__).resolve().parent / "web"


def load_credentials() -> tuple[str, str]:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your environment"
        )
    return api_key, api_secret


def create_order(payload: dict[str, str]) -> dict[str, object]:
    symbol = normalize_symbol(payload.get("symbol", ""))
    side = normalize_side(payload.get("side", ""))
    order_type = normalize_order_type(payload.get("orderType", ""))
    quantity = parse_positive_decimal(payload.get("quantity", ""), "quantity")
    price = (
        parse_positive_decimal(payload.get("price", ""), "price")
        if payload.get("price")
        else None
    )
    validate_price_requirement(order_type, price)

    api_key, api_secret = load_credentials()
    client = BinanceFuturesClient(
        api_key=api_key,
        api_secret=api_secret,
        base_url=os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com"),
    )
    order_payload = build_order_payload(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )
    response = submit_order(client, order_payload)
    return {"request": order_payload, "response": response}


class TradingBotHandler(BaseHTTPRequestHandler):
    server_version = "TradingBotUI/1.0"

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return

        if parsed.path == "/":
            self._serve_static("index.html", "text/html; charset=utf-8")
            return

        if parsed.path == "/styles.css":
            self._serve_static("styles.css", "text/css; charset=utf-8")
            return

        if parsed.path == "/app.js":
            self._serve_static("app.js", "application/javascript; charset=utf-8")
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/order":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")

        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "Request body must be valid JSON"},
            )
            return

        try:
            result = create_order(payload)
        except ValueError as exc:
            LOGGER.exception("Validation error while creating order")
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        except BinanceClientError as exc:
            LOGGER.exception("Binance client error while creating order")
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": str(exc)})
            return
        except Exception as exc:  # pragma: no cover
            LOGGER.exception("Unexpected error while creating order")
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": f"Unexpected server error: {exc}"},
            )
            return

        self._send_json(HTTPStatus.OK, result)

    def log_message(self, format: str, *args: object) -> None:
        LOGGER.info("%s - %s", self.address_string(), format % args)

    def _serve_static(self, filename: str, content_type: str) -> None:
        file_path = STATIC_DIR / filename
        if not file_path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        body = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    log_file = setup_logging()
    server = ThreadingHTTPServer((host, port), TradingBotHandler)
    LOGGER.info("Starting Trading Bot UI at http://%s:%s", host, port)
    LOGGER.info("Logs written to: %s", log_file)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("Stopping Trading Bot UI")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
