import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Optional, Tuple, List, Dict, Any

from .config import CONFIG


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Restaurant (
	name TEXT NOT NULL,
	address TEXT NOT NULL,
	gstin TEXT NOT NULL,
	state_code TEXT NOT NULL,
	fssai_license TEXT
);

CREATE TABLE IF NOT EXISTS GSTSettings (
	slab_rate REAL NOT NULL,
	cgst_rate REAL NOT NULL,
	sgst_rate REAL NOT NULL,
	applicable_from TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS MenuItems (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	price REAL NOT NULL,
	category TEXT NOT NULL,
	gst_slab REAL NOT NULL,
	hsn_code TEXT NOT NULL,
	food_type TEXT NOT NULL CHECK(food_type IN ('veg','non-veg'))
);

CREATE TABLE IF NOT EXISTS Orders (
	order_id INTEGER PRIMARY KEY AUTOINCREMENT,
	table_number INTEGER,
	customer_name TEXT,
	customer_gstin TEXT,
	place_of_supply TEXT,
	invoice_number TEXT,
	invoice_date TEXT,
	subtotal REAL NOT NULL DEFAULT 0,
	cgst REAL NOT NULL DEFAULT 0,
	sgst REAL NOT NULL DEFAULT 0,
	igst REAL NOT NULL DEFAULT 0,
	service_charge REAL NOT NULL DEFAULT 0,
	total REAL NOT NULL DEFAULT 0,
	status TEXT NOT NULL DEFAULT 'OPEN' -- OPEN, PAID, CANCELLED
);
CREATE INDEX IF NOT EXISTS idx_orders_invoice ON Orders(invoice_number);

CREATE TABLE IF NOT EXISTS OrderItems (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	order_id INTEGER NOT NULL REFERENCES Orders(order_id) ON DELETE CASCADE,
	item_id INTEGER NOT NULL REFERENCES MenuItems(id),
	item_name TEXT NOT NULL,
	hsn_code TEXT NOT NULL,
	quantity INTEGER NOT NULL,
	rate REAL NOT NULL,
	gst_slab REAL NOT NULL,
	line_amount REAL NOT NULL,
	UNIQUE(order_id, item_id)
);

-- Users for role-based access
CREATE TABLE IF NOT EXISTS Users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL UNIQUE,
	full_name TEXT,
	role TEXT NOT NULL CHECK(role IN ('SUPER_ADMIN','ADMIN','CAPTAIN')),
	password_hash TEXT NOT NULL,
	password_salt TEXT NOT NULL,
	is_active INTEGER NOT NULL DEFAULT 1,
	created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_users_username ON Users(username);
"""


SEED_SQL: Iterable[str] = (
	# Minimal restaurant details (edit via UI later)
	f"INSERT INTO Restaurant(name, address, gstin, state_code, fssai_license) VALUES (\n '{CONFIG.restaurant_legal_name}',\n '123, MG Road, Mumbai, Maharashtra 400001',\n '27ABCDE1234F1Z5',\n '27',\n '11518002000000'\n);",
	# GST slabs commonly used
	"INSERT INTO GSTSettings(slab_rate, cgst_rate, sgst_rate, applicable_from) VALUES (5, 2.5, 2.5, date('now'));",
	"INSERT INTO GSTSettings(slab_rate, cgst_rate, sgst_rate, applicable_from) VALUES (12, 6, 6, date('now'));",
	"INSERT INTO GSTSettings(slab_rate, cgst_rate, sgst_rate, applicable_from) VALUES (18, 9, 9, date('now'));",
	"INSERT INTO GSTSettings(slab_rate, cgst_rate, sgst_rate, applicable_from) VALUES (28, 14, 14, date('now'));",
	# Sample menu
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Paneer Tikka', 240, 'Starters & Appetizers', 5, '996331', 'veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Chicken Tikka', 280, 'Starters & Appetizers', 5, '996331', 'non-veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Dal Tadka', 220, 'Main Course (Veg)', 5, '996331', 'veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Butter Chicken', 360, 'Main Course (Non-Veg)', 5, '996331', 'non-veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Naan', 40, 'Breads & Rice', 5, '996331', 'veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Jeera Rice', 160, 'Breads & Rice', 5, '996331', 'veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Veg Fried Rice', 200, 'Chinese & Continental', 5, '996331', 'veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Masala Dosa', 120, 'South Indian', 5, '996331', 'veg');",
	"INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type) VALUES ('Lassi', 90, 'Beverages & Desserts', 12, '996331', 'veg');",
)


@contextmanager
def get_conn(db_path: Optional[Path] = None):
	db_file = str(db_path or CONFIG.db_path)
	conn = sqlite3.connect(db_file)
	try:
		yield conn
		conn.commit()
	finally:
		conn.close()


def init_db():
	with get_conn() as conn:
		conn.executescript(SCHEMA_SQL)
		# Seed idempotently: try inserts; ignore failures
		for stmt in SEED_SQL:
			try:
				conn.execute(stmt)
			except sqlite3.Error:
				pass


def get_today_sales_totals() -> Tuple[float, float]:
	"""Return (subtotal_without_tax_and_service, grand_total) for today's PAID orders."""
	with get_conn() as conn:
		cur = conn.execute(
			"""
			SELECT COALESCE(SUM(subtotal),0), COALESCE(SUM(total),0)
			FROM Orders
			WHERE date(invoice_date) = date('now') AND status = 'PAID'
			"""
		)
		row = cur.fetchone()
		return float(row[0]), float(row[1])


def get_order_by_invoice(invoice_number: str) -> Optional[Dict[str, Any]]:
	with get_conn() as conn:
		cur = conn.execute("SELECT * FROM Orders WHERE invoice_number = ?", (invoice_number,))
		order = cur.fetchone()
		if not order:
			return None
		columns = [d[0] for d in cur.description]
		order_dict = dict(zip(columns, order))
		cur_items = conn.execute(
			"SELECT item_name, hsn_code, quantity, rate, gst_slab, line_amount FROM OrderItems WHERE order_id = ?",
			(order_dict["order_id"],),
		)
		items = []
		for row in cur_items.fetchall():
			items.append({
				"item_name": row[0],
				"hsn_code": row[1],
				"quantity": row[2],
				"rate": row[3],
				"gst_slab": row[4],
				"line_amount": row[5],
			})
		order_dict["items"] = items
		return order_dict
