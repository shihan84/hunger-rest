import hashlib
import os
from typing import Optional, Tuple, Dict, Set

from .db import get_conn

# Actions in the system
A_MANAGE_USERS = "manage_users"
A_MANAGE_MENU = "manage_menu"
A_VIEW_REPORTS = "view_reports"
A_CREATE_ORDER = "create_order"
A_CHECKOUT_BILL = "checkout_bill"
A_CONFIGURE_SETTINGS = "configure_settings"
A_LOOKUP_BILL = "lookup_bill"

# Permissions by role
ROLE_PERMISSIONS: Dict[str, Set[str]] = {
	"SUPER_ADMIN": {
		A_MANAGE_USERS,
		A_MANAGE_MENU,
		A_VIEW_REPORTS,
		A_CREATE_ORDER,
		A_CHECKOUT_BILL,
		A_CONFIGURE_SETTINGS,
		A_LOOKUP_BILL,
	},
	"ADMIN": {
		A_MANAGE_MENU,
		A_VIEW_REPORTS,
		A_CREATE_ORDER,
		A_CHECKOUT_BILL,
	},
	"CAPTAIN": {
		A_CREATE_ORDER,
		A_CHECKOUT_BILL,
	},
}


def user_can(user: Optional[dict], action: str) -> bool:
	if not user:
		return False
	role = user.get("role")
	perms = ROLE_PERMISSIONS.get(role, set())
	return action in perms


def _hash_password(password: str, salt: bytes) -> str:
	return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200000).hex()


def create_user(username: str, full_name: str, role: str, password: str) -> int:
	salt = os.urandom(16)
	hash_hex = _hash_password(password, salt)
	with get_conn() as conn:
		cur = conn.execute(
			"INSERT INTO Users(username, full_name, role, password_hash, password_salt) VALUES (?, ?, ?, ?, ?)",
			(username, full_name, role, hash_hex, salt.hex()),
		)
		return cur.lastrowid


def get_user(username: str) -> Optional[Tuple[int, str, str, str, str, int]]:
	with get_conn() as conn:
		cur = conn.execute("SELECT id, username, full_name, role, password_hash, is_active FROM Users WHERE username = ?", (username,))
		row = cur.fetchone()
		return row if row else None


def verify_password(username: str, password: str) -> bool:
	with get_conn() as conn:
		cur = conn.execute("SELECT password_hash, password_salt, is_active FROM Users WHERE username = ?", (username,))
		row = cur.fetchone()
		if not row:
			return False
		existing_hash, salt_hex, is_active = row
		if not is_active:
			return False
		salt = bytes.fromhex(salt_hex)
		return existing_hash == _hash_password(password, salt)


def seed_super_admin() -> None:
	"""Create a default super admin if none exists."""
	with get_conn() as conn:
		cur = conn.execute("SELECT COUNT(*) FROM Users WHERE role = 'SUPER_ADMIN'")
		count = cur.fetchone()[0]
		if count == 0:
			create_user("owner", "Super Admin", "SUPER_ADMIN", "1234")
