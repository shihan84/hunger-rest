from typing import Optional
from telegram import Bot
from telegram.error import TelegramError

from .config import CONFIG


def send_message(text: str, bot_token: Optional[str] = None, chat_id: Optional[str] = None) -> bool:
	"""Send a message to Telegram chat. Returns True if sent."""
	if bot_token is None:
		bot_token = CONFIG.telegram_bot_token
	if chat_id is None:
		chat_id = CONFIG.telegram_chat_id
	if not bot_token or not chat_id:
		return False
	try:
		bot = Bot(token=bot_token)
		bot.send_message(chat_id=chat_id, text=text)
		return True
	except TelegramError:
		return False
