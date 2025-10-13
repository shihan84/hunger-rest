from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class AppConfig:
	app_name: str = "HUNGER Restaurant Billing"
	licensee: str = "Varchaswaa Medi Pvt Ltd"
	restaurant_legal_name: str = "HUNGER Restaurant"
	developed_by: str = "Varchaswaa Media Pvt Ltd"
	rights_owner: str = "Varchaswaa Media Pvt Ltd"
	db_path: Path = Path.cwd() / "data" / "restaurant.db"
	assets_path: Path = Path.cwd() / "assets"
	invoices_path: Path = Path.cwd() / "invoices"
	default_state_code: str = "27"  # Maharashtra by default
	currency_symbol: str = "₹"
	default_service_charge_percent: float = 0.0  # optional, can be set 5-10
	fullscreen: bool = False
	telegram_bot_token: Optional[str] = None
	telegram_chat_id: Optional[str] = None
	upi_vpa: Optional[str] = None
	upi_payee_name: Optional[str] = None


CONFIG = AppConfig()

# Ensure directories exist at import time for simplicity
CONFIG.db_path.parent.mkdir(parents=True, exist_ok=True)
CONFIG.assets_path.mkdir(parents=True, exist_ok=True)
CONFIG.invoices_path.mkdir(parents=True, exist_ok=True)
