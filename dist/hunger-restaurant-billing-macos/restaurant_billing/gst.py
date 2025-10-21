from typing import Dict, Tuple

from .db import get_conn


def get_rates_for_slab(slab_percent: float) -> Tuple[float, float]:
	"""Fetch CGST and SGST for a slab from GSTSettings; fallback to 50/50 split."""
	with get_conn() as conn:
		cur = conn.execute(
			"SELECT cgst_rate, sgst_rate FROM GSTSettings WHERE slab_rate = ? ORDER BY date(applicable_from) DESC LIMIT 1",
			(slab_percent,),
		)
		row = cur.fetchone()
		if row:
			return float(row[0]), float(row[1])
	half = round(float(slab_percent) / 2.0, 4)
	return half, half


def round_indian(value: float) -> float:
	return round(value + 1e-9, 2)


def compute_gst_for_order_items(
	items: Dict[str, Dict[str, float]],
	intra_state: bool = True,
	service_charge_percent: float = 0.0,
) -> Dict[str, float]:
	"""
	items: {
		item_name: {
			"quantity": int,
			"rate": float,
			"gst_slab": float,
			"hsn_code": str
		}
	}
	"""
	subtotal = 0.0
	hsn_tax_map: Dict[str, Dict[str, float]] = {}

	for item, data in items.items():
		qty = int(data.get("quantity", 1))
		rate = float(data.get("rate", 0.0))
		slab = float(data.get("gst_slab", 0.0))
		line = qty * rate
		subtotal += line
		hsn = str(data.get("hsn_code", "996331"))
		hsn_entry = hsn_tax_map.setdefault(hsn, {"taxable": 0.0, "cgst": 0.0, "sgst": 0.0, "igst": 0.0})
		hsn_entry["taxable"] += line
		cgst_rate, sgst_rate = get_rates_for_slab(slab)
		if intra_state:
			hsn_entry["cgst"] += line * cgst_rate / 100.0
			hsn_entry["sgst"] += line * sgst_rate / 100.0
		else:
			hsn_entry["igst"] += line * slab / 100.0

	service_charge = subtotal * (service_charge_percent / 100.0)
	taxable_total = subtotal + service_charge

	total_cgst = sum(v["cgst"] for v in hsn_tax_map.values())
	total_sgst = sum(v["sgst"] for v in hsn_tax_map.values())
	total_igst = sum(v["igst"] for v in hsn_tax_map.values())

	total_amount = taxable_total + total_cgst + total_sgst + total_igst

	return {
		"subtotal": round_indian(subtotal),
		"service_charge": round_indian(service_charge),
		"cgst": round_indian(total_cgst),
		"sgst": round_indian(total_sgst),
		"igst": round_indian(total_igst),
		"total": round_indian(total_amount),
		"hsn_breakdown": hsn_tax_map,
	}
