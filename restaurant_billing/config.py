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
	fullscreen: bool = True  # Enable fullscreen for touch screens
	# Touch screen UI settings
	touch_mode: bool = True
	button_height: int = 60  # Larger buttons for touch
	button_width: int = 120
	font_size_large: int = 14
	font_size_medium: int = 12
	font_size_small: int = 10
	icon_size: int = 32  # Icon size for touch buttons
	telegram_bot_token: Optional[str] = "8391823641:AAHuRZlop8M_0zNSMnk1iiGkGTCORCc7qks"
	telegram_chat_id: Optional[str] = "-4816754138"
	upi_vpa: Optional[str] = None
	upi_payee_name: Optional[str] = None
	# Printing configuration for POSIFLOW KP206B-UB
	printer_type: str = "os"  # os | escpos_usb | escpos_network
	escpos_vendor_id: Optional[int] = None  # Will be auto-detected for POSIFLOW
	escpos_product_id: Optional[int] = None  # Will be auto-detected for POSIFLOW
	escpos_host: Optional[str] = None  # for network printers
	escpos_port: int = 9100
	paper_width_chars: int = 30  # 58mm paper width for POSIFLOW KP206B-UB (30 chars per line, Font Size 8, precise margins)
	printer_encoding: str = "utf-8"  # Better Unicode support
	printer_name: str = "POSIFLOW KP206B-UB"  # Friendly printer name
	# POSIFLOW KP206B-UB specific settings
	paper_width_mm: int = 58  # 58mm paper width
	print_speed_mm_per_sec: int = 90  # 90mm/s print speed
	thermal_printer: bool = True  # Thermal receipt printer
	# GST Configuration
	gst_enabled: bool = False  # Enable/disable GST calculation (disabled by default)
	restaurant_gst_number: Optional[str] = None  # Restaurant GST number
	gst_registration_type: str = "REGULAR"  # REGULAR | COMPOSITION | UNREGISTERED


CONFIG = AppConfig()

# Ensure directories exist at import time for simplicity
CONFIG.db_path.parent.mkdir(parents=True, exist_ok=True)
CONFIG.assets_path.mkdir(parents=True, exist_ok=True)
CONFIG.invoices_path.mkdir(parents=True, exist_ok=True)
