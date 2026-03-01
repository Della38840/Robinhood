"""
Robinhood API Documentation CLI
Unofficial Documentation of Robinhood Trade's Private API
"""

import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich import box
from rich.markdown import Markdown
from rich.text import Text
from utils import ensure_env

console = Console()

ROBINHOOD_LOGO = r"""
 _______             __        __            __                                  __ 
/       \           /  |      /  |          /  |                                /  |
$$$$$$$  |  ______  $$ |____  $$/  _______  $$ |____    ______    ______    ____$$ |
$$ |__$$ | /      \ $$      \ /  |/       \ $$      \  /      \  /      \  /    $$ |
$$    $$< /$$$$$$  |$$$$$$$  |$$ |$$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |/$$$$$$$ |
$$$$$$$  |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |$$ \__$$ |$$ |__$$ |$$ |$$ |  $$ |$$ |  $$ |$$ \__$$ |$$ \__$$ |$$ \__$$ |
$$ |  $$ |$$    $$/ $$    $$/ $$ |$$ |  $$ |$$ |  $$ |$$    $$/ $$    $$/ $$    $$ |
$$/   $$/  $$$$$$/  $$$$$$$/  $$/ $$/   $$/ $$/   $$/  $$$$$$/   $$$$$$/   $$$$$$$/ 
"""


def clear_screen():
    """Clear terminal screen."""
    console.clear()


def show_logo():
    """Display Robinhood ASCII logo."""
    console.print(Panel(Text(ROBINHOOD_LOGO, style="bold green"), 
                       box=box.DOUBLE, border_style="green", padding=(0, 2)))
    console.print()


def install_dependencies():
    """Install project dependencies."""
    clear_screen()
    show_logo()
    console.print(Panel("[bold cyan]Install Dependencies[/bold cyan]", border_style="cyan"))
    console.print()
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            console.print("[bold green]✓ Dependencies installed successfully![/bold green]")
            console.print("[dim]Packages: rich, requests[/dim]")
        else:
            console.print("[bold red]✗ Installation failed:[/bold red]")
            console.print(result.stderr or result.stdout)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue[/dim]", default="")


def show_settings():
    """Display and manage Settings (notifications and other settings)."""
    clear_screen()
    show_logo()
    console.print(Panel("[bold cyan]Settings[/bold cyan] - Notifications and other settings", border_style="cyan"))
    console.print()
    
    settings_info = """
Settings.md covers:
• [bold]Notifications[/bold] - Push and email notification preferences
• [bold]API Token[/bold] - Manage authorization tokens
• [bold]Preferences[/bold] - User interface and trading preferences
• [bold]Privacy[/bold] - Account visibility and data sharing options

Authorized calls require: [bold]Authorization: Token <your_40_char_token>[/bold]
"""
    console.print(Markdown(settings_info))
    
    table = Table(title="Quick Settings Reference")
    table.add_column("Setting", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Endpoint", style="dim")
    table.add_row("Push Notifications", "Enable/disable mobile push", "api.robinhood.com/settings/")
    table.add_row("Email Alerts", "Trading and account alerts", "api.robinhood.com/notifications/")
    table.add_row("2FA", "Two-factor authentication", "api.robinhood.com/user/mfa/")
    console.print(table)
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue[/dim]", default="")


def show_about():
    """Display About information with hashtags."""
    clear_screen()
    show_logo()
    console.print(Panel("[bold cyan]About[/bold cyan]", border_style="cyan"))
    console.print()
    
    about_path = Path(__file__).parent / "about" / "about.md"
    if about_path.exists():
        content = about_path.read_text(encoding="utf-8")
        console.print(Markdown(content))
    else:
        console.print("[yellow]About file not found. Loading default info...[/yellow]")
        default_about = """
# Robinhood API Documentation

**Unofficial Documentation of Robinhood Trade's Private API**

Robinhood is a commission-free, online securities brokerage.
Official docs: https://docs.robinhood.com/crypto/trading/

#Robinhood #API #UnofficialDocs #Crypto #Trading
"""
        console.print(Markdown(default_about))
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue[/dim]", default="")


def show_api_section(title: str, description: str, content: str):
    """Display an API documentation section."""
    clear_screen()
    show_logo()
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", border_style="cyan"))
    console.print()
    console.print(description)
    console.print()
    console.print(Markdown(content))
    console.print()
    Prompt.ask("[dim]Press Enter to continue[/dim]", default="")


def show_authentication():
    """Authentication API section."""
    content = """
## Authentication
- User login and logout
- Password recovery
- Token generation and refresh
- OAuth flows

**Auth Header:** `Authorization: Token <40_char_token>`
"""
    show_api_section("Authentication", "Methods for user authentication, password recovery, etc.", content)


def show_banking():
    """Banking API section."""
    content = """
## Banking
- Bank accounts management
- ACH transfers
- Withdrawals and deposits
- Linked accounts
"""
    show_api_section("Banking", "Bank accounts & ACH transfers methods", content)


def show_order():
    """Order API section."""
    content = """
## Order
- Placing buy/sell orders
- Cancelling orders
- Listing previous orders
- Order status and history
"""
    show_api_section("Order", "Order-related functions (placing, cancelling, listing)", content)


def show_options():
    """Options API section."""
    content = """
## Options
- Options chains
- Options orders
- Options positions
- Greeks and pricing
"""
    show_api_section("Options", "Options related endpoints", content)


def show_quote():
    """Quote API section."""
    content = """
## Quote
- Real-time stock quotes
- Bid/Ask prices
- Volume and price data
"""
    show_api_section("Quote", "Stock quotes", content)


def show_fundamentals():
    """Fundamentals API section."""
    content = """
## Fundamentals
- Basic fundamental data
- Company information
- Financial metrics
"""
    show_api_section("Fundamentals", "Basic, fundamental data", content)


def show_instrument():
    """Instrument API section."""
    content = """
## Instrument
- Internal reference to financial instruments
- Symbol lookup
- Instrument metadata
"""
    show_api_section("Instrument", "Internal reference to financial instruments", content)


def show_watchlist():
    """Watchlist API section."""
    content = """
## Watchlist
- Create and manage watchlists
- Add/remove symbols
- Watchlist customization
"""
    show_api_section("Watchlist", "Watchlists management", content)


def show_account():
    """Account API section."""
    content = """
## Account
- User and account information
- Portfolio data
- Account modifications
"""
    show_api_section("Account", "Gathering and modifying user and account information", content)


def show_markets():
    """Markets API section."""
    content = """
## Markets
- Exchange information
- Market hours
- Trading sessions
"""
    show_api_section("Markets", "API for getting basic info about specific exchanges", content)


def show_referrals():
    """Referrals API section."""
    content = """
## Referrals
- Account referral program
- Referral links
- Bonus tracking
"""
    show_api_section("Referrals", "Account referrals", content)


def show_statistics():
    """Statistics API section."""
    content = """
## Statistics
- Social/statistical endpoints
- Popular stocks
- Community data
"""
    show_api_section("Statistics", "Social/statistical endpoints", content)


def show_tags():
    """Tags API section."""
    content = """
## Tags
- Categorizing endpoints
- Stock categories
- Custom tags
"""
    show_api_section("Tags", "Categorizing endpoints", content)


def show_unsorted():
    """Unsorted API section."""
    content = """
## Unsorted
- Endpoints yet to be organized
- Miscellaneous API methods
- Work in progress documentation
"""
    show_api_section("Unsorted", "Things yet to be organized", content)


def show_introduction():
    """Introduction section from README."""
    clear_screen()
    show_logo()
    console.print(Panel("[bold cyan]Introduction[/bold cyan]", border_style="cyan"))
    console.print()
    
    intro = """
Robinhood is a commission-free, online securities brokerage. Being an online service means 
everything is handled through a request made to a specific URL.

**API Security:** HTTPS protocol. SSL Pinning recommended for production.

**Authentication Levels:**
- *None* - No auth. Informational queries (quotes, lookup).
- *Token* - Requires `Authorization: Token <40_char_token>` header.
"""
    console.print(Markdown(intro))
    console.print()
    Prompt.ask("[dim]Press Enter to continue[/dim]", default="")


def show_menu():
    """Display main menu."""
    table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
    table.add_column(" # ", style="bold yellow", width=4)
    table.add_column("Option", style="white")
    table.add_column("Description", style="dim")
    
    menu_items = [
        (1, "Install Dependencies", "Install rich, requests and other packages"),
        (2, "Settings", "Notifications and account settings"),
        (3, "About", "Project info and hashtags"),
        (4, "Introduction", "API overview and security"),
        (5, "Authentication", "Login, tokens, password recovery"),
        (6, "Banking", "Bank accounts & ACH transfers"),
        (7, "Order", "Placing, cancelling, listing orders"),
        (8, "Options", "Options related endpoints"),
        (9, "Quote", "Stock quotes"),
        (10, "Fundamentals", "Basic fundamental data"),
        (11, "Instrument", "Financial instruments reference"),
        (12, "Watchlist", "Watchlists management"),
        (13, "Account", "User and account information"),
        (14, "Markets", "Exchange info"),
        (15, "Referrals", "Account referrals"),
        (16, "Statistics", "Social/statistical endpoints"),
        (17, "Tags", "Categorizing endpoints"),
        (18, "Unsorted", "Unorganized endpoints"),
        (0, "Exit", "Quit application"),
    ]
    
    for num, option, desc in menu_items:
        table.add_row(f" {num} ", option, desc)
    
    console.print(table)
    console.print()


@ensure_env
def main():
    """Main application loop."""
    actions = {
        1: install_dependencies,
        2: show_settings,
        3: show_about,
        4: show_introduction,
        5: show_authentication,
        6: show_banking,
        7: show_order,
        8: show_options,
        9: show_quote,
        10: show_fundamentals,
        11: show_instrument,
        12: show_watchlist,
        13: show_account,
        14: show_markets,
        15: show_referrals,
        16: show_statistics,
        17: show_tags,
        18: show_unsorted,
    }
    
    while True:
        clear_screen()
        show_logo()
        console.print(Panel("[bold]Unofficial Documentation of Robinhood Trade's Private API[/bold]", 
                           border_style="blue", padding=(0, 2)))
        console.print()
        show_menu()
        
        try:
            choice = IntPrompt.ask("[bold cyan]Select option[/bold cyan]", default=0)
        except (ValueError, KeyboardInterrupt):
            choice = 0
        
        if choice == 0:
            clear_screen()
            console.print("[bold green]Goodbye![/bold green]")
            break
        
        if choice in actions:
            actions[choice]()
        else:
            console.print("[red]Invalid option. Please try again.[/red]")
            Prompt.ask("[dim]Press Enter to continue[/dim]", default="")


if __name__ == "__main__":
    main()
