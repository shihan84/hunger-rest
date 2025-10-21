from pathlib import Path
from typing import Dict, Any

from .config import CONFIG
from .db import get_conn, get_order_by_invoice
from .utils import amount_in_words_inr, format_date_indian, format_currency_inr


def _get_restaurant() -> Dict[str, Any]:
	with get_conn() as conn:
		cur = conn.execute("SELECT name, address, gstin, state_code, fssai_license FROM Restaurant LIMIT 1")
		row = cur.fetchone()
		if not row:
			return {"name": CONFIG.restaurant_legal_name, "address": "", "gstin": "", "state_code": CONFIG.default_state_code, "fssai_license": ""}
		return {"name": row[0], "address": row[1], "gstin": row[2], "state_code": row[3], "fssai_license": row[4]}


def _hsn_breakdown(items: list[dict]) -> Dict[str, Dict[str, float]]:
	by_hsn: Dict[str, Dict[str, float]] = {}
	for it in items:
		hsn = str(it["hsn_code"]) if it.get("hsn_code") else ""
		entry = by_hsn.setdefault(hsn, {"taxable": 0.0, "cgst": 0.0, "sgst": 0.0, "igst": 0.0})
		entry["taxable"] += float(it["line_amount"])
		# Item-level taxes are not stored per line; rely on order totals for summary
	return by_hsn


def build_invoice_text(order: Dict[str, Any]) -> str:
	rest = _get_restaurant()
	lines: list[str] = []
	lines.append(f"{rest['name']}")
	lines.append(rest["address"]) if rest.get("address") else None
	lines.append(f"GSTIN: {rest['gstin']}   FSSAI: {rest['fssai_license']}")
	lines.append("")
	lines.append(f"TAX INVOICE")
	lines.append(f"Invoice No: {order['invoice_number']}    Date: {order['invoice_date']}")
	if order.get("customer_name"):
		lines.append(f"Customer: {order['customer_name']}")
	if order.get("customer_gstin"):
		lines.append(f"Customer GSTIN: {order['customer_gstin']}")
	lines.append("")
	lines.append("Items:")
	for it in order["items"]:
		lines.append(f" - {it['item_name']} x{it['quantity']} @ {format_currency_inr(it['rate'])} = {format_currency_inr(it['line_amount'])}")
	lines.append("")
	lines.append(f"Subtotal: {format_currency_inr(order['subtotal'])}")
	if float(order.get('service_charge',0)):
		lines.append(f"Service Charge: {format_currency_inr(order['service_charge'])}")
	if float(order.get('cgst',0)):
		lines.append(f"CGST: {format_currency_inr(order['cgst'])}")
	if float(order.get('sgst',0)):
		lines.append(f"SGST: {format_currency_inr(order['sgst'])}")
	if float(order.get('igst',0)):
		lines.append(f"IGST: {format_currency_inr(order['igst'])}")
	lines.append(f"Grand Total: {format_currency_inr(order['total'])}")
	lines.append(f"Amount in words: {amount_in_words_inr(order['total'])}")
	lines.append("")
	lines.append("HSN-wise Summary:")
	for hsn, entry in _hsn_breakdown(order["items"]).items():
		lines.append(f" HSN {hsn}: Taxable {format_currency_inr(entry['taxable'])}")
	lines.append("")
	lines.append("Declaration: We declare that this invoice shows the actual price and that all particulars are true and correct.")
	lines.append("This is a computer generated invoice.")
	return "\n".join(lines)


def save_invoice_text(invoice_number: str) -> Path:
	order = get_order_by_invoice(invoice_number)
	if not order:
		raise ValueError("Invoice not found")
	text = build_invoice_text(order)
	CONFIG.invoices_path.mkdir(parents=True, exist_ok=True)
	out = CONFIG.invoices_path / f"{invoice_number}.txt"
	out.write_text(text, encoding="utf-8")
	return out
