from pathlib import Path
from typing import Optional
import os
import subprocess
import platform

from .config import CONFIG
from .invoice import save_invoice_text

try:
	from escpos.printer import Usb, Network
	_HAS_ESCPOS = True
except Exception:
	_HAS_ESCPOS = False


def _split_lines_for_width(text: str, width: int) -> str:
	"""Split text lines to fit within specified width"""
	lines = []
	for line in text.splitlines():
		while len(line) > width:
			lines.append(line[:width])
			line = line[width:]
		lines.append(line)
	return "\n".join(lines)


def _format_for_full_width(text: str, width: int = 80) -> str:
	"""Format text for full-width printing with proper alignment"""
	lines = []
	for line in text.splitlines():
		# Center restaurant name
		if line.startswith(CONFIG.restaurant_legal_name) or line.startswith("HUNGER"):
			lines.append(line.center(width))
		# Center headers like "TAX INVOICE"
		elif line.startswith("TAX INVOICE") or line.startswith("RECEIPT"):
			lines.append(line.center(width))
		# Left-align other content
		else:
			lines.append(line.ljust(width))
	return "\n".join(lines)


def _get_printer_width() -> int:
	"""Get appropriate printer width based on system and printer type"""
	if CONFIG.printer_type == "escpos_usb" or CONFIG.printer_type == "escpos_network":
		# ESC/POS printers typically support 32-48 characters
		return 48
	else:
		# For OS printing, use full page width
		return 80


def print_invoice_os(invoice_number: str) -> Path:
	"""Print invoice using OS printing with full-width support"""
	path = save_invoice_text(invoice_number)
	
	# Read the invoice text
	with open(path, 'r', encoding='utf-8') as f:
		text = f.read()
	
	# Format for full-width printing
	width = _get_printer_width()
	formatted_text = _format_for_full_width(text, width)
	
	# Write formatted text to a temporary file
	temp_path = path.parent / f"formatted_{invoice_number}.txt"
	with open(temp_path, 'w', encoding='utf-8') as f:
		f.write(formatted_text)
	
	# Print using OS commands
	if os.name == 'posix':  # Unix/Linux/macOS
		# Try different printing methods
		commands = [
			f"lp '{temp_path}'",
			f"lpr '{temp_path}'",
			f"cat '{temp_path}' | lp",
			f"cat '{temp_path}' | lpr"
		]
		
		for cmd in commands:
			try:
				result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
				if result.returncode == 0:
					print(f"[INFO] Printed using: {cmd}")
					break
			except Exception as e:
				print(f"[WARNING] Print command failed: {cmd} - {e}")
				continue
	else:  # Windows
		# Try different Windows printing methods
		commands = [
			f'notepad /p "{temp_path}"',
			f'type "{temp_path}" | more',
			f'powershell -Command "Get-Content \'{temp_path}\' | Out-Printer"'
		]
		
		for cmd in commands:
			try:
				result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
				if result.returncode == 0:
					print(f"[INFO] Printed using: {cmd}")
					break
			except Exception as e:
				print(f"[WARNING] Print command failed: {cmd} - {e}")
				continue
	
	# Clean up temporary file
	try:
		temp_path.unlink()
	except:
		pass
	
	return path


def print_invoice_escpos(invoice_number: str, usb_vendor: Optional[int] = None, usb_product: Optional[int] = None, host: Optional[str] = None, port: Optional[int] = None) -> bool:
	"""Print invoice using ESC/POS with full-width support"""
	if not _HAS_ESCPOS:
		return False
	
	text_path = save_invoice_text(invoice_number)
	text = Path(text_path).read_text(encoding='utf-8')
	
	# Format for full-width printing
	width = _get_printer_width()
	formatted_text = _format_for_full_width(text, width)
	
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
		
		# Set printer to use full width
		printer.set(align='center', width=2, height=2)  # Center alignment for headers
		
		for line in formatted_text.splitlines():
			if line.strip().startswith(CONFIG.restaurant_legal_name) or line.strip().startswith("HUNGER"):
				# Center restaurant name
				printer.set(align='center', width=2, height=2)
				printer.text(line.strip() + "\n")
			elif line.strip().startswith("TAX INVOICE") or line.strip().startswith("RECEIPT"):
				# Center headers
				printer.set(align='center', width=2, height=2)
				printer.text(line.strip() + "\n")
			else:
				# Left-align other content
				printer.set(align='left', width=1, height=1)
				printer.text(line + "\n")
		
		printer.cut()
		return True
	except Exception as e:
		print(f"[ERROR] ESC/POS printing failed: {e}")
		return False


def print_invoice_full_width(invoice_number: str) -> bool:
	"""Print invoice with full-width formatting"""
	try:
		if CONFIG.printer_type == "os":
			print_invoice_os(invoice_number)
			return True
		elif CONFIG.printer_type in ["escpos_usb", "escpos_network"]:
			return print_invoice_escpos(invoice_number)
		else:
			print(f"[ERROR] Unknown printer type: {CONFIG.printer_type}")
			return False
	except Exception as e:
		print(f"[ERROR] Printing failed: {e}")
		return False


def configure_printer_for_full_width():
	"""Configure printer settings for full-width printing"""
	# Update config for full-width printing
	global CONFIG
	CONFIG.paper_width_chars = 80  # Use full page width
	CONFIG.printer_encoding = "utf-8"  # Use UTF-8 encoding
	
	print("[INFO] Printer configured for full-width printing")
	print(f"[INFO] Paper width: {CONFIG.paper_width_chars} characters")
	print(f"[INFO] Printer type: {CONFIG.printer_type}")


def test_printer_width():
	"""Test printer width with sample text"""
	test_text = """
HUNGER Restaurant
123 Main Street, City
GSTIN: 27ABCDE1234F1Z5   FSSAI: 12345678901234

TAX INVOICE
Invoice No: TEST001    Date: 2024-01-01

Items:
 - Test Item 1 x1 @ ₹100.00 = ₹100.00
 - Test Item 2 x2 @ ₹50.00 = ₹100.00

Subtotal: ₹200.00
CGST: ₹18.00
SGST: ₹18.00
Total: ₹236.00

Thank you for your business!
"""
	
	width = _get_printer_width()
	formatted_text = _format_for_full_width(test_text, width)
	
	print("=" * 80)
	print("PRINTER WIDTH TEST")
	print("=" * 80)
	print(formatted_text)
	print("=" * 80)
	print(f"Width: {width} characters")
	print("=" * 80)
