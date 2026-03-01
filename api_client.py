# -*- coding: utf-8 -*-
"""
Robinhood API client — authentication, portfolio, orders, and quotes.
Wraps the unofficial Robinhood private API for programmatic access
to trading operations, account data, and market quotes.
"""
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from config import RobinhoodConfig, load_config, save_config

try:
    import requests
except ImportError:
    requests = None


CLIENT_ID = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"


@dataclass
class QuoteData:
    symbol: str
    last_trade_price: float
    bid_price: float
    ask_price: float
    previous_close: float
    updated_at: str = ""
    trading_halted: bool = False

    @property
    def change(self) -> float:
        return round(self.last_trade_price - self.previous_close, 4)

    @property
    def change_pct(self) -> float:
        if self.previous_close == 0:
            return 0.0
        return round((self.change / self.previous_close) * 100, 2)

    @property
    def spread(self) -> float:
        return round(self.ask_price - self.bid_price, 4)


@dataclass
class Position:
    instrument_url: str
    symbol: str
    quantity: float
    average_buy_price: float
    current_price: float = 0.0

    @property
    def market_value(self) -> float:
        return round(self.quantity * self.current_price, 4)

    @property
    def total_cost(self) -> float:
        return round(self.quantity * self.average_buy_price, 4)

    @property
    def pnl(self) -> float:
        return round(self.market_value - self.total_cost, 4)

    @property
    def pnl_pct(self) -> float:
        if self.total_cost == 0:
            return 0.0
        return round((self.pnl / self.total_cost) * 100, 2)


class RateLimiter:
    """Simple token-bucket rate limiter."""

    def __init__(self, rpm: int):
        self._interval = 60.0 / max(rpm, 1)
        self._last_call = 0.0

    def wait(self) -> None:
        elapsed = time.time() - self._last_call
        if elapsed < self._interval:
            time.sleep(self._interval - elapsed)
        self._last_call = time.time()


class RobinhoodClient:
    """Client for the Robinhood private REST API."""

    def __init__(self, cfg: Optional[RobinhoodConfig] = None):
        if requests is None:
            raise RuntimeError("requests library is required — run: pip install requests")
        self._cfg = cfg or load_config()
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "RobinhoodCLI/1.0",
            "X-Robinhood-API-Version": "1.431.4",
        })
        if self._cfg.auth_token:
            self._session.headers["Authorization"] = f"Token {self._cfg.auth_token}"
        self._session.verify = self._cfg.ssl_verify
        self._limiter = RateLimiter(self._cfg.rate_limit_rpm)
        self._quote_cache: dict[str, tuple[float, QuoteData]] = {}

    def _url(self, path: str) -> str:
        base = self._cfg.api_base.rstrip("/")
        return f"{base}/{path.lstrip('/')}"

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        self._limiter.wait()
        resp = self._session.get(
            self._url(path),
            params=params,
            timeout=self._cfg.timeout_seconds,
        )
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    def _post(self, path: str, data: Optional[dict] = None) -> dict:
        self._limiter.wait()
        resp = self._session.post(
            self._url(path),
            json=data,
            timeout=self._cfg.timeout_seconds,
        )
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    def login(self, username: str, password: str,
              mfa_code: Optional[str] = None) -> dict:
        """Authenticate with username/password and optional MFA code."""
        payload = {
            "client_id": CLIENT_ID,
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "internal",
            "device_token": self._cfg.device_token or uuid.uuid4().hex,
        }
        if mfa_code:
            payload["mfa_code"] = mfa_code

        result = self._post("/oauth2/token/", payload)
        if "access_token" in result:
            self._cfg.auth_token = result["access_token"]
            self._session.headers["Authorization"] = f"Token {result['access_token']}"
            save_config(self._cfg)
        return result

    def logout(self) -> dict:
        """Revoke the current authentication token."""
        result = self._post("/oauth2/revoke_token/", {
            "client_id": CLIENT_ID,
            "token": self._cfg.auth_token,
        })
        self._cfg.auth_token = None
        self._session.headers.pop("Authorization", None)
        save_config(self._cfg)
        return result

    def get_account(self) -> dict:
        """Retrieve primary account information."""
        data = self._get("/accounts/")
        results = data.get("results", [])
        if results:
            self._cfg.account_url = results[0].get("url")
            save_config(self._cfg)
        return results[0] if results else {}

    def get_portfolio(self) -> dict:
        """Retrieve portfolio summary with equity and market value."""
        if not self._cfg.account_url:
            self.get_account()
        if not self._cfg.account_url:
            return {}
        acct_id = self._cfg.account_url.rstrip("/").split("/")[-1]
        return self._get(f"/portfolios/{acct_id}/")

    def get_positions(self, nonzero: bool = True) -> list[dict]:
        """List stock positions, optionally filtering for non-zero quantity."""
        params = {"nonzero": "true"} if nonzero else {}
        data = self._get("/positions/", params)
        return data.get("results", [])

    def get_quote(self, symbol: str) -> QuoteData:
        """Fetch real-time quote for a stock symbol (cached briefly)."""
        symbol = symbol.upper()
        now = time.time()

        if self._cfg.cache_quotes and symbol in self._quote_cache:
            ts, cached = self._quote_cache[symbol]
            if now - ts < self._cfg.cache_ttl_seconds:
                return cached

        data = self._get(f"/quotes/{symbol}/")
        quote = QuoteData(
            symbol=data.get("symbol", symbol),
            last_trade_price=float(data.get("last_trade_price", 0)),
            bid_price=float(data.get("bid_price", 0)),
            ask_price=float(data.get("ask_price", 0)),
            previous_close=float(data.get("previous_close", 0)),
            updated_at=data.get("updated_at", ""),
            trading_halted=data.get("trading_halted", False),
        )
        self._quote_cache[symbol] = (now, quote)
        return quote

    def get_quotes_batch(self, symbols: list[str]) -> list[QuoteData]:
        """Fetch quotes for multiple symbols in a single request."""
        joined = ",".join(s.upper() for s in symbols)
        data = self._get("/quotes/", params={"symbols": joined})
        results = data.get("results", [])
        quotes = []
        for item in results:
            if item is None:
                continue
            quotes.append(QuoteData(
                symbol=item.get("symbol", ""),
                last_trade_price=float(item.get("last_trade_price", 0)),
                bid_price=float(item.get("bid_price", 0)),
                ask_price=float(item.get("ask_price", 0)),
                previous_close=float(item.get("previous_close", 0)),
                updated_at=item.get("updated_at", ""),
                trading_halted=item.get("trading_halted", False),
            ))
        return quotes

    def place_order(self, symbol: str, side: str, quantity: float,
                    order_type: str = "market", price: Optional[float] = None,
                    time_in_force: str = "gfd") -> dict:
        """Place a buy or sell order."""
        instrument = self._get(f"/instruments/", params={"symbol": symbol.upper()})
        results = instrument.get("results", [])
        if not results:
            raise ValueError(f"Instrument not found for symbol: {symbol}")

        instrument_url = results[0]["url"]

        if not self._cfg.account_url:
            self.get_account()

        payload = {
            "account": self._cfg.account_url,
            "instrument": instrument_url,
            "symbol": symbol.upper(),
            "side": side.lower(),
            "type": order_type,
            "quantity": quantity,
            "time_in_force": time_in_force,
            "trigger": "immediate",
        }
        if price is not None:
            payload["price"] = f"{price:.2f}"

        return self._post("/orders/", payload)

    def cancel_order(self, order_id: str) -> dict:
        """Cancel a pending order by its ID."""
        return self._post(f"/orders/{order_id}/cancel/")

    def get_orders(self, updated_at: Optional[str] = None) -> list[dict]:
        """List recent orders, optionally filtered by update time."""
        params = {}
        if updated_at:
            params["updated_at[gte]"] = updated_at
        data = self._get("/orders/", params)
        return data.get("results", [])

    def get_fundamentals(self, symbol: str) -> dict:
        """Get fundamental data for a stock."""
        return self._get(f"/fundamentals/{symbol.upper()}/")

    def get_watchlists(self) -> list[dict]:
        """List all watchlists."""
        data = self._get("/watchlists/")
        return data.get("results", [])

    def get_markets(self) -> list[dict]:
        """Get information about exchanges."""
        data = self._get("/markets/")
        return data.get("results", [])


def create_client(cfg: Optional[RobinhoodConfig] = None) -> RobinhoodClient:
    """Factory: create a RobinhoodClient with current or provided config."""
    return RobinhoodClient(cfg or load_config())
