from typing import Dict, Any, Optional
from datetime import datetime

from .db import get_conn, get_order_by_invoice


def is_einvoice_required(order: Dict[str, Any], threshold: float = 50000.0) -> bool:
	"""Check if e-invoice is required based on order total and threshold."""
	return float(order.get("total", 0.0)) >= threshold


def generate_einvoice_json(invoice_number: str) -> Optional[Dict[str, Any]]:
	"""Generate e-invoice JSON structure (IRN-ready format). Returns None if not required."""
	order = get_order_by_invoice(invoice_number)
	if not order:
		return None
	
	if not is_einvoice_required(order):
		return None
	
	# Basic e-invoice structure (IRN format)
	einvoice = {
		"Version": "1.1",
		"TranDtls": {
			"TaxSch": "GST",
			"SupTyp": "B2B" if order.get("customer_gstin") else "B2C",
			"IgstOnIntra": "N" if order.get("place_of_supply") == "27" else "Y"
		},
		"DocDtls": {
			"Typ": "INV",
			"No": order["invoice_number"],
			"Dt": order["invoice_date"][:10]  # YYYY-MM-DD
		},
		"SellerDtls": _get_seller_details(),
		"BuyerDtls": _get_buyer_details(order),
		"ItemList": _build_item_list(order["items"]),
		"ValDtls": {
			"AssVal": float(order["subtotal"]),
			"TotInvVal": float(order["total"]),
			"TotInvValFc": float(order["total"])
		}
	}
	
	# Add GST details
	if float(order.get("cgst", 0)) > 0 or float(order.get("sgst", 0)) > 0:
		einvoice["ValDtls"]["CgstVal"] = float(order["cgst"])
		einvoice["ValDtls"]["SgstVal"] = float(order["sgst"])
	if float(order.get("igst", 0)) > 0:
		einvoice["ValDtls"]["IgstVal"] = float(order["igst"])
	
	return einvoice


def _get_seller_details() -> Dict[str, Any]:
	"""Get seller (restaurant) details for e-invoice."""
	with get_conn() as conn:
		cur = conn.execute("SELECT name, address, gstin, state_code FROM Restaurant LIMIT 1")
		row = cur.fetchone()
		if not row:
			return {}
		return {
			"Gstin": row[2],
			"LglNm": row[0],
			"Addr1": row[1],
			"Loc": "Mumbai",
			"Pin": 400001,
			"Stcd": row[3]
		}


def _get_buyer_details(order: Dict[str, Any]) -> Dict[str, Any]:
	"""Get buyer details for e-invoice."""
	if order.get("customer_gstin"):
		return {
			"Gstin": order["customer_gstin"],
			"LglNm": order.get("customer_name", "Walk-in Customer"),
			"Pos": order.get("place_of_supply", "27")
		}
	else:
		return {
			"LglNm": order.get("customer_name", "Walk-in Customer"),
			"Pos": order.get("place_of_supply", "27")
		}


def _build_item_list(items: list) -> list:
	"""Build item list for e-invoice."""
	item_list = []
	for item in items:
		item_list.append({
			"SlNo": len(item_list) + 1,
			"PrdDesc": item["item_name"],
			"IsServc": "Y",  # Restaurant services
			"HsnCd": item["hsn_code"],
			"Qty": float(item["quantity"]),
			"Unit": "NOS",
			"UnitPrice": float(item["rate"]),
			"TotAmt": float(item["line_amount"]),
			"AssAmt": float(item["line_amount"]),
			"GstRt": float(item["gst_slab"]),
			"IgstAmt": 0.0,  # Will be calculated based on place of supply
			"CgstAmt": 0.0,
			"SgstAmt": 0.0
		})
	return item_list


def save_einvoice_json(invoice_number: str) -> Optional[str]:
	"""Save e-invoice JSON to file. Returns file path if saved, None if not required."""
	einvoice = generate_einvoice_json(invoice_number)
	if not einvoice:
		return None
	
	import json
	from .config import CONFIG
	
	CONFIG.invoices_path.mkdir(parents=True, exist_ok=True)
	file_path = CONFIG.invoices_path / f"{invoice_number}_einvoice.json"
	file_path.write_text(json.dumps(einvoice, indent=2), encoding="utf-8")
	return str(file_path)
