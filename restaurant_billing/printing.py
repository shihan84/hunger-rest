from pathlib import Path
from typing import Optional
import os

from .config import CONFIG
from .invoice import save_invoice_text

try:
	from escpos.printer import Usb, Network
	_HAS_ESCPOS = True
except Exception:
	_HAS_ESCPOS = False


def print_invoice_os(invoice_number: str) -> Path:
	"""Save invoice text and send to OS default print handler where available."""
	path = save_invoice_text(invoice_number)
	# macOS: open -P (may require GUI); Windows: not supported via CLI in all cases; users can open and print
	if os.name == 'posix':
		os.system(f"lp '{path}' 2>/dev/null || open -P '{path}' 2>/dev/null || true")
	return path


def print_invoice_escpos(invoice_number: str, usb_vendor: Optional[int] = None, usb_product: Optional[int] = None, host: Optional[str] = None, port: int = 9100) -> bool:
	"""Print using ESC/POS via USB or Network. Returns True if attempted."""
	if not _HAS_ESCPOS:
		return False
	text_path = save_invoice_text(invoice_number)
	text = Path(text_path).read_text(encoding='utf-8')
	try:
		printer = None
		if usb_vendor and usb_product:
			printer = Usb(usb_vendor, usb_product, 0)
		elif host:
			printer = Network(host, port=port)
		if not printer:
			return False
		for line in text.splitlines():
			printer.text(line + "\n")
		printer.cut()
		return True
	except Exception:
		return False
