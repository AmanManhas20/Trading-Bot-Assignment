from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class BinanceClientError(Exception):
    """Raised when the Binance client cannot complete a request."""


@dataclass
class BinanceFuturesClient:
    api_key: str
    api_secret: str
    base_url: str = "https://testnet.binancefuture.com"
    timeout: int = 15

    def __post_init__(self) -> None:
        self.headers = {"X-MBX-APIKEY": self.api_key}

    def place_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._signed_request("POST", "/fapi/v1/order", payload)

    def _signed_request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        request_params = dict(params or {})
        request_params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(request_params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        url = f"{self.base_url.rstrip('/')}{path}"
        final_params = dict(request_params)
        final_params["signature"] = signature
        request_url = f"{url}?{urlencode(final_params, doseq=True)}"

        try:
            request = Request(
                url=request_url,
                method=method,
                headers=self.headers,
            )
            with urlopen(request, timeout=self.timeout) as response:
                raw_body = response.read().decode("utf-8")
                status_code = response.status
        except HTTPError as exc:
            raw_body = exc.read().decode("utf-8", errors="replace")
            message = self._format_error(exc.code, raw_body)
            raise BinanceClientError(message) from exc
        except URLError as exc:
            raise BinanceClientError(f"Network error while calling Binance: {exc}") from exc

        data = json.loads(raw_body)
        if isinstance(data, dict) and data.get("code", 0) not in (0, None):
            raise BinanceClientError(self._format_error(status_code, raw_body))
        return data

    @staticmethod
    def _format_error(status_code: int, raw_body: str) -> str:
        try:
            payload = json.loads(raw_body)
        except ValueError:
            return f"Binance API error: HTTP {status_code} - {raw_body}"

        code = payload.get("code")
        message = payload.get("msg", raw_body)
        if code is None:
            return f"Binance API error: HTTP {status_code} - {message}"
        return f"Binance API error {code}: {message}"
