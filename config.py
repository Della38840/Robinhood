# -*- coding: utf-8 -*-
"""
Robinhood API Documentation CLI — configuration management.
Handles API base URLs, authentication tokens, rate limiting, and client preferences.
"""
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


_BASE_DIR = Path(__file__).resolve().parent
_CONFIG_FILE = _BASE_DIR / "rh_config.json"

API_BASE_URL = "https://api.robinhood.com"
NUMMUS_URL = "https://nummus.robinhood.com"
OAUTH_TOKEN_URL = f"{API_BASE_URL}/oauth2/token/"

DEFAULT_TIMEOUT = 30
DEFAULT_RATE_LIMIT_RPM = 60
DEFAULT_PAGE_SIZE = 25


@dataclass
class RobinhoodConfig:
    api_base: str = API_BASE_URL
    nummus_base: str = NUMMUS_URL
    timeout_seconds: int = DEFAULT_TIMEOUT
    rate_limit_rpm: int = DEFAULT_RATE_LIMIT_RPM
    page_size: int = DEFAULT_PAGE_SIZE
    auth_token: Optional[str] = None
    device_token: Optional[str] = None
    account_url: Optional[str] = None
    output_format: str = "table"
    color_theme: str = "green"
    ssl_verify: bool = True
    log_level: str = "INFO"
    cache_quotes: bool = True
    cache_ttl_seconds: int = 15

    @property
    def is_authenticated(self) -> bool:
        return self.auth_token is not None and len(self.auth_token) == 40

    @property
    def auth_header(self) -> dict:
        if self.auth_token:
            return {"Authorization": f"Token {self.auth_token}"}
        return {}

    def validate(self) -> list[str]:
        errors = []
        if self.timeout_seconds < 1:
            errors.append("Timeout must be >= 1 second")
        if self.rate_limit_rpm < 1:
            errors.append("Rate limit must be >= 1 RPM")
        if self.page_size < 1 or self.page_size > 100:
            errors.append("Page size must be 1-100")
        if self.auth_token and len(self.auth_token) != 40:
            errors.append("Auth token must be exactly 40 characters")
        return errors


def load_config() -> RobinhoodConfig:
    """Load configuration from disk or return defaults."""
    if not _CONFIG_FILE.exists():
        cfg = RobinhoodConfig()
        save_config(cfg)
        return cfg

    with open(_CONFIG_FILE, "r", encoding="utf-8") as fp:
        raw = json.load(fp)

    cfg = RobinhoodConfig()
    for k, v in raw.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)
    return cfg


def save_config(cfg: RobinhoodConfig) -> None:
    """Persist configuration to disk."""
    with open(_CONFIG_FILE, "w", encoding="utf-8") as fp:
        json.dump(asdict(cfg), fp, indent=2, ensure_ascii=False)


def reset_config() -> RobinhoodConfig:
    """Reset to defaults (clears auth token)."""
    cfg = RobinhoodConfig()
    save_config(cfg)
    return cfg


def set_auth_token(token: str) -> Optional[str]:
    """Set authentication token. Returns error or None."""
    if len(token) != 40:
        return "Token must be exactly 40 characters"
    cfg = load_config()
    cfg.auth_token = token
    save_config(cfg)
    return None
