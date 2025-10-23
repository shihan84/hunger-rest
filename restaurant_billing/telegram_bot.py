from typing import Optional
import asyncio
import requests

from .config import CONFIG
from .db import get_today_sales_totals


def send_message(text: str, bot_token: Optional[str] = None, chat_id: Optional[str] = None) -> bool:
	"""Send a message to Telegram chat. Returns True if sent."""
	if bot_token is None:
		bot_token = CONFIG.telegram_bot_token
	if chat_id is None:
		chat_id = CONFIG.telegram_chat_id
	if not bot_token or not chat_id:
		return False
	
	try:
		# Use requests instead of async telegram library to avoid async issues
		url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
		data = {
			"chat_id": chat_id,
			"text": text,
			"parse_mode": "HTML"
		}
		
		response = requests.post(url, data=data, timeout=10)
		return response.status_code == 200
		
	except Exception as e:
		print(f"Telegram send error: {e}")
		return False


def send_today_sales_summary() -> bool:
	subtotal, grand = get_today_sales_totals()
	text = (
		f"HUNGER Restaurant Sales Today\n"
		f"Subtotal (Taxable): ₹{subtotal:.2f}\n"
		f"Grand Total: ₹{grand:.2f}"
	)
	return send_message(text)
