from datetime import datetime
from num2words import num2words


def format_currency_inr(amount: float) -> str:
	return f"₹{amount:,.2f}".replace(",", ",")  # Keep grouping; OS locale-independent


def amount_in_words_inr(amount: float) -> str:
	integer = int(round(amount))
	return num2words(integer, lang="en_IN").replace(" and ", " ").title() + " Only"


def format_date_indian(dt: datetime) -> str:
	return dt.strftime("%d/%m/%Y")
