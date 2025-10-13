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


def _split_lines_for_width(text: str, width: int) -> str:
	lines = []
	for line in text.splitlines():
		while len(line) > width:
			lines.append(line[:width])
			line = line[width:]
		lines.append(line)
	return "\n".join(lines)


def print_invoice_os(invoice_number: str) -> Path:
	path = save_invoice_text(invoice_number)
	if os.name == 'posix':
		os.system(f"lp '{path}' 2>/dev/null || open -P '{path}' 2>/dev/null || true")
	return path


def print_invoice_escpos(invoice_number: str, usb_vendor: Optional[int] = None, usb_product: Optional[int] = None, host: Optional[str] = None, port: Optional[int] = None) -> bool:
	if not _HAS_ESCPOS:
		return False
	text_path = save_invoice_text(invoice_number)
	text = Path(text_path).read_text(encoding='utf-8')
	text = _split_lines_for_width(text, CONFIG.paper_width_chars)
	try:
		printer = None
		v = usb_vendor or CONFIG.escpos_vendor_id
		p = usb_product or CONFIG.escpos_product_id
		h = host or CONFIG.escpos_host
		po = port or CONFIG.escpos_port
		if CONFIG.printer_type == 'escpos_usb' and v and p:
			printer = Usb(v, p, 0)
		elif CONFIG.printer_type == 'escpos_network' and h:
			printer = Network(h, port=po)
		if not printer:
			return False
		for line in text.splitlines():
			printer.text(line + "\n")
		printer.cut()
		return True
	except Exception:
		return False
