# Robinhood
Robinhood API Docs — CLI reference browser for Robinhood Trade unofficial private REST API documentation with endpoint exploration, authentication flow reference, order management, market data retrieval, portfolio queries, and Rich terminal interface for trading API research
<div align="center">

```
 _______             __        __            __                                  __
/       \           /  |      /  |          /  |                                /  |
$$$$$$$  |  ______  $$ |____  $$/  _______  $$ |____    ______    ______    ____$$ |
$$ |__$$ | /      \ $$      \ /  |/       \ $$      \  /      \  /      \  /    $$ |
$$    $$< /$$$$$$  |$$$$$$$  |$$ |$$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |/$$$$$$$ |
$$$$$$$  |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |$$ \__$$ |$$ |__$$ |$$ |$$ |  $$ |$$ |  $$ |$$ \__$$ |$$ \__$$ |$$ \__$$ |
$$ |  $$ |$$    $$/ $$    $$/ $$ |$$ |  $$ |$$ |  $$ |$$    $$/ $$    $$/ $$    $$ |
$$/   $$/  $$$$$$/  $$$$$$$/  $$/ $$/   $$/ $$/   $$/  $$$$$$/   $$$$$$/   $$$$$$$/
```

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Robinhood](https://img.shields.io/badge/Robinhood-API_Docs-00C805?style=for-the-badge)
![REST](https://img.shields.io/badge/REST-API-FF6600?style=for-the-badge&logo=fastapi&logoColor=white)
![Unofficial](https://img.shields.io/badge/Unofficial-Documentation-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-Unlicense-blue?style=for-the-badge)

**CLI reference browser for Robinhood Trade's unofficial private API documentation**

[Features](#-features) · [Getting Started](#-getting-started) · [Configuration](#-configuration) · [Usage](#-usage) · [FAQ](#-faq)

</div>

---

## Registration & Official Links

| # | Resource | Link |
|---|----------|------|
| 1 | Robinhood Official Platform | [robinhood.com](https://robinhood.com/) |
| 2 | Robinhood Crypto Docs | [docs.robinhood.com/crypto/trading](https://docs.robinhood.com/crypto/trading/) |
| 3 | Original API Documentation (sanko) | [github.com/sanko/Robinhood](https://github.com/sanko/Robinhood) |
| 4 | pyrh — Python Robinhood Library | [pyrh.readthedocs.io](https://pyrh.readthedocs.io/en/latest) |
| 5 | GitHub Discussions | [github.com/sanko/Robinhood/discussions](https://github.com/sanko/Robinhood/discussions) |

---

## Features

<table>
<tr><td colspan="2"><strong>API Documentation Sections</strong></td></tr>
<tr><td width="50%">

- [x] Introduction & API Overview
- [x] Authentication (OAuth, tokens, MFA)
- [x] Banking (ACH, deposits, withdrawals)
- [x] Order (buy/sell, cancel, history)
- [x] Options (chains, orders, positions)
- [x] Quote (real-time stock prices)
- [x] Fundamentals (company data)
- [x] Instrument (symbol lookup)

</td><td width="50%">

- [x] Watchlist (create, manage, symbols)
- [x] Account (portfolio, user info)
- [x] Settings (notifications, 2FA, privacy)
- [x] Markets (exchange info, hours)
- [x] Referrals (referral program)
- [x] Statistics (social endpoints)
- [x] Tags (categorization)
- [x] Unsorted (miscellaneous endpoints)

</td></tr>
<tr><td colspan="2"><strong>Interface & UX</strong></td></tr>
<tr><td>

- [x] Rich terminal UI with panels & tables
- [x] ASCII art header with green theme
- [x] 18 navigable menu options

</td><td>

- [x] Markdown rendering in terminal
- [x] Endpoint reference tables
- [x] Cross-platform (Windows / Linux / macOS)

</td></tr>
</table>

---

## Getting Started

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.8+ | Runtime |
| pip | latest | Package manager |

### Installation

<details>
<summary><strong>Windows (One-Click)</strong></summary>

Double-click `run.bat` to launch:

```bat
@echo off
chcp 65001 > nul
cd /d "%~dp0"
python main.py
pause
```

</details>

<details>
<summary><strong>Manual Setup (All Platforms)</strong></summary>

```bash
git clone <repository-url>
cd Robinhood
pip install -r requirements.txt
python main.py
```

</details>

### Dependency Table

| Package | Version | Purpose |
|---------|---------|---------|
| `rich` | >=13.0.0 | Terminal UI — panels, tables, markdown rendering |
| `requests` | >=2.28.0 | HTTP requests (optional for live API calls) |

---

## Configuration

This application is a documentation browser and requires no configuration files. All API endpoint information is embedded in the source code.

### Authentication Context

The documented API uses token-based authentication:

```
Authorization: Token <your_40_character_token>
```

| Auth Level | Description | Example Endpoints |
|------------|-------------|-------------------|
| **None** | No auth required | Quotes, instrument lookup |
| **Token** | Requires auth header | Orders, account, banking |

### API Base URL

```
https://api.robinhood.com/
```

---

## Usage

Run the application:

```bash
python main.py
```

### CLI Menu

```
┌────┬──────────────────────┬─────────────────────────────────┐
│  # │ Option               │ Description                     │
├────┼──────────────────────┼─────────────────────────────────┤
│  1 │ Install Dependencies │ Install rich, requests          │
│  2 │ Settings             │ Notifications and account       │
│  3 │ About                │ Project info and hashtags       │
│  4 │ Introduction         │ API overview and security       │
│  5 │ Authentication       │ Login, tokens, password recovery│
│  6 │ Banking              │ Bank accounts & ACH transfers   │
│  7 │ Order                │ Placing, cancelling, listing    │
│  8 │ Options              │ Options related endpoints       │
│  9 │ Quote                │ Stock quotes                    │
│ 10 │ Fundamentals         │ Basic fundamental data          │
│ 11 │ Instrument           │ Financial instruments reference │
│ 12 │ Watchlist            │ Watchlists management           │
│ 13 │ Account              │ User and account information    │
│ 14 │ Markets              │ Exchange info                   │
│ 15 │ Referrals            │ Account referrals               │
│ 16 │ Statistics           │ Social/statistical endpoints    │
│ 17 │ Tags                 │ Categorizing endpoints          │
│ 18 │ Unsorted             │ Unorganized endpoints           │
│  0 │ Exit                 │ Quit application                │
└────┴──────────────────────┴─────────────────────────────────┘
```

### API Sections Quick Reference

| Section | Key Endpoints | Auth Required |
|---------|---------------|---------------|
| Authentication | `/api-token-auth/`, `/api-token-logout/` | No (login) / Token (logout) |
| Banking | `/ach/transfers/`, `/ach/relationships/` | Token |
| Order | `/orders/`, `/orders/{id}/cancel/` | Token |
| Options | `/options/chains/`, `/options/orders/` | Token |
| Quote | `/quotes/{symbol}/` | None |
| Fundamentals | `/fundamentals/{symbol}/` | None |
| Instrument | `/instruments/`, `/instruments/{id}/` | None |
| Watchlist | `/watchlists/` | Token |
| Account | `/accounts/`, `/portfolios/` | Token |
| Markets | `/markets/{mic}/` | None |

---

## Project Structure

```
Robinhood/
├── main.py              # Entry point — Rich CLI, API section browsers, menu loop
├── run.bat              # Windows one-click launcher
├── requirements.txt     # Python dependencies (rich, requests)
└── about/
    ├── about.md         # Project description, hashtags, API overview table
    └── hashtags.txt     # Tag collection for discovery
```

---

## FAQ

<details>
<summary><strong>What is this project?</strong></summary>

This is a CLI documentation browser for Robinhood's unofficial private API. It is based on the [sanko/Robinhood](https://github.com/sanko/Robinhood) repository (1.7k+ stars) which reverse-engineered Robinhood Trade's internal REST API endpoints. The tool presents this documentation in an interactive terminal interface.

</details>

<details>
<summary><strong>Does this tool execute real trades?</strong></summary>

No. This is a **read-only documentation browser**. It does not connect to Robinhood's API, does not store credentials, and does not execute any trades. It simply displays API endpoint documentation in a Rich terminal UI.

</details>

<details>
<summary><strong>What is the Robinhood private API?</strong></summary>

Robinhood uses an internal REST API over HTTPS for all client-server communication. This API is not officially documented for third-party use. The `sanko/Robinhood` project reverse-engineered these endpoints including authentication flows (OAuth2, MFA), order placement, banking, and market data retrieval.

</details>

<details>
<summary><strong>Is using the Robinhood API legal?</strong></summary>

Accessing the API programmatically may violate Robinhood's Terms of Service. This tool is for educational and research purposes only. Always review Robinhood's current ToS before interacting with their API directly.

</details>

<details>
<summary><strong>How do I get a Robinhood API token?</strong></summary>

According to the documented API, you POST credentials to `/api-token-auth/` to receive a 40-character token. This token is then included as `Authorization: Token <token>` in subsequent requests. MFA-enabled accounts require additional steps documented in the Authentication section.

</details>

<details>
<summary><strong>Can I use pyrh instead?</strong></summary>

Yes. [pyrh](https://pyrh.readthedocs.io/) is a Python framework built on the same unofficial API that provides a higher-level interface for authentication, quote retrieval, and trading. It can be installed via `pip install pyrh`.

</details>

---

## Disclaimer

> This software is provided for **educational and research purposes only**. It documents an unofficial, reverse-engineered API. Use of the Robinhood API outside of official channels may violate Robinhood's Terms of Service. The developers are not affiliated with Robinhood Markets, Inc. and assume no liability for any consequences of API usage.

---

<div align="center">

**If this tool helped you, consider giving it a** ⭐

Based on [sanko/Robinhood](https://github.com/sanko/Robinhood) — Unofficial Documentation of Robinhood Trade's Private API

[Back to Top](#)

</div>
