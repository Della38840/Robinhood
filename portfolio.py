# -*- coding: utf-8 -*-
"""
Robinhood — portfolio analysis and display.
Aggregates position data, calculates sector allocation,
and provides PnL breakdowns for the trading account.
"""
import time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class AssetClass(Enum):
    STOCK = "stock"
    ETF = "etf"
    CRYPTO = "crypto"
    OPTION = "option"
    UNKNOWN = "unknown"


@dataclass
class HoldingEntry:
    symbol: str
    quantity: float
    average_cost: float
    current_price: float
    asset_class: AssetClass = AssetClass.STOCK
    sector: str = "Unknown"
    instrument_id: Optional[str] = None

    @property
    def market_value(self) -> float:
        return round(self.quantity * self.current_price, 4)

    @property
    def cost_basis(self) -> float:
        return round(self.quantity * self.average_cost, 4)

    @property
    def unrealized_pnl(self) -> float:
        return round(self.market_value - self.cost_basis, 4)

    @property
    def unrealized_pnl_pct(self) -> float:
        if self.cost_basis == 0:
            return 0.0
        return round((self.unrealized_pnl / self.cost_basis) * 100, 2)

    @property
    def weight_factor(self) -> float:
        return self.market_value


@dataclass
class PortfolioSnapshot:
    timestamp: float
    total_equity: float
    total_market_value: float
    cash_balance: float
    unrealized_pnl: float
    day_change: float
    day_change_pct: float


class PortfolioAnalyzer:
    """Aggregate and analyze portfolio holdings."""

    def __init__(self):
        self._holdings: dict[str, HoldingEntry] = {}
        self._cash: float = 0.0
        self._snapshots: list[PortfolioSnapshot] = []

    def set_cash(self, amount: float) -> None:
        self._cash = amount

    def add_holding(self, entry: HoldingEntry) -> None:
        self._holdings[entry.symbol.upper()] = entry

    def remove_holding(self, symbol: str) -> bool:
        key = symbol.upper()
        if key in self._holdings:
            del self._holdings[key]
            return True
        return False

    def get_holding(self, symbol: str) -> Optional[HoldingEntry]:
        return self._holdings.get(symbol.upper())

    def all_holdings(self) -> list[HoldingEntry]:
        return list(self._holdings.values())

    def total_market_value(self) -> float:
        return round(sum(h.market_value for h in self._holdings.values()), 4)

    def total_cost_basis(self) -> float:
        return round(sum(h.cost_basis for h in self._holdings.values()), 4)

    def total_equity(self) -> float:
        return round(self.total_market_value() + self._cash, 4)

    def total_unrealized_pnl(self) -> float:
        return round(self.total_market_value() - self.total_cost_basis(), 4)

    def total_unrealized_pnl_pct(self) -> Optional[float]:
        basis = self.total_cost_basis()
        if basis == 0:
            return None
        return round((self.total_unrealized_pnl() / basis) * 100, 2)

    def top_gainers(self, limit: int = 5) -> list[HoldingEntry]:
        sorted_h = sorted(
            self._holdings.values(),
            key=lambda h: h.unrealized_pnl,
            reverse=True,
        )
        return sorted_h[:limit]

    def top_losers(self, limit: int = 5) -> list[HoldingEntry]:
        sorted_h = sorted(
            self._holdings.values(),
            key=lambda h: h.unrealized_pnl,
        )
        return sorted_h[:limit]

    def by_asset_class(self) -> dict[str, list[HoldingEntry]]:
        result: dict[str, list[HoldingEntry]] = {}
        for h in self._holdings.values():
            key = h.asset_class.value
            result.setdefault(key, []).append(h)
        return result

    def sector_allocation(self) -> dict[str, float]:
        """Calculate portfolio weight per sector as percentages."""
        total = self.total_market_value()
        if total == 0:
            return {}
        allocation: dict[str, float] = {}
        for h in self._holdings.values():
            allocation[h.sector] = allocation.get(h.sector, 0.0) + h.market_value
        return {
            sector: round((value / total) * 100, 2)
            for sector, value in sorted(allocation.items(), key=lambda x: -x[1])
        }

    def weight_allocation(self) -> dict[str, float]:
        """Calculate portfolio weight per symbol as percentages."""
        total = self.total_market_value()
        if total == 0:
            return {}
        return {
            h.symbol: round((h.market_value / total) * 100, 2)
            for h in sorted(self._holdings.values(), key=lambda h: -h.market_value)
        }

    def concentration_risk(self, threshold_pct: float = 25.0) -> list[str]:
        """Identify positions exceeding the concentration threshold."""
        weights = self.weight_allocation()
        return [sym for sym, w in weights.items() if w >= threshold_pct]

    def take_snapshot(self, day_change: float = 0.0,
                      day_change_pct: float = 0.0) -> PortfolioSnapshot:
        snap = PortfolioSnapshot(
            timestamp=time.time(),
            total_equity=self.total_equity(),
            total_market_value=self.total_market_value(),
            cash_balance=self._cash,
            unrealized_pnl=self.total_unrealized_pnl(),
            day_change=day_change,
            day_change_pct=day_change_pct,
        )
        self._snapshots.append(snap)
        return snap

    @property
    def snapshots(self) -> list[PortfolioSnapshot]:
        return list(self._snapshots)

    def summary(self) -> dict:
        return {
            "total_equity": self.total_equity(),
            "market_value": self.total_market_value(),
            "cash": self._cash,
            "cost_basis": self.total_cost_basis(),
            "unrealized_pnl": self.total_unrealized_pnl(),
            "unrealized_pnl_pct": self.total_unrealized_pnl_pct(),
            "positions_count": len(self._holdings),
            "top_sector": next(iter(self.sector_allocation()), "N/A"),
            "concentration_warnings": self.concentration_risk(),
            "snapshots_recorded": len(self._snapshots),
        }
