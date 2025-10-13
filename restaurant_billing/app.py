import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from pathlib import Path
import platform

from .config import CONFIG
from .db import init_db, get_order_by_invoice
from .auth import verify_password, get_user, seed_super_admin, user_can, A_MANAGE_USERS, A_MANAGE_MENU, A_VIEW_REPORTS, A_CREATE_ORDER, A_CHECKOUT_BILL, A_CONFIGURE_SETTINGS, A_LOOKUP_BILL
from .telegram_bot import send_message


def _macos_fullscreen_supported() -> bool:
	if platform.system() != "Darwin":
		return True
	ver = platform.mac_ver()[0]
	try:
		parts = [int(p) for p in ver.split(".") if p.isdigit()]
		if len(parts) >= 2:
			major, minor = parts[0], parts[1]
			return not (major == 14 and minor < 7)
		return True
	except Exception:
		return False


class PromptDialog(simpledialog.Dialog):
	def __init__(self, parent, title: str, label: str):
		self._label_text = label
		super().__init__(parent, title)

	def body(self, master):
		ttk.Label(master, text=self._label_text).grid(row=0, column=0, padx=6, pady=6, sticky="w")
		self.value_var = tk.StringVar()
		ttk.Entry(master, textvariable=self.value_var).grid(row=1, column=0, padx=6, pady=6)
		return master

	def apply(self):
		self.result = self.value_var.get().strip()


class LoginDialog(simpledialog.Dialog):
	def body(self, master):
		self.title("Login")
		ttk.Label(master, text="Username").grid(row=0, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Password").grid(row=1, column=0, padx=6, pady=6, sticky="e")
		self.username_var = tk.StringVar()
		self.password_var = tk.StringVar()
		ttk.Entry(master, textvariable=self.username_var).grid(row=0, column=1, padx=6, pady=6)
		ttk.Entry(master, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=6, pady=6)
		return master

	def apply(self):
		self.result = (self.username_var.get().strip(), self.password_var.get())


class RestaurantApp(tk.Tk):
	def __init__(self, logo_path: Path):
		super().__init__()
		self.title(CONFIG.app_name)
		self._set_window_icon(logo_path)
		self._enter_fullscreen(CONFIG.fullscreen)
		self.current_user = None
		self._login_flow()
		self._build_ui(logo_path)
		self._apply_permissions()

	def _login_flow(self) -> None:
		seed_super_admin()
		auth_ok = False
		while not auth_ok:
			dlg = LoginDialog(self)
			if not dlg.result:
				self.destroy()
				return
			username, password = dlg.result
			if verify_password(username, password):
				user = get_user(username)
				self.current_user = {
					"id": user[0],
					"username": user[1],
					"full_name": user[2],
					"role": user[3],
				}
				auth_ok = True
			else:
				messagebox.showerror("Login Failed", "Invalid credentials.")

	def _set_window_icon(self, logo_path: Path) -> None:
		try:
			img = Image.open(logo_path)
			icon = ImageTk.PhotoImage(img)
			self.iconphoto(True, icon)
			self._icon_ref = icon
		except Exception:
			pass

	def _enter_fullscreen(self, enable: bool) -> None:
		if enable:
			if _macos_fullscreen_supported():
				self.attributes("-fullscreen", True)
				self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
			else:
				w = self.winfo_screenwidth()
				h = self.winfo_screenheight()
				self.geometry(f"{w}x{h}+0+0")
				self.bind("<Escape>", lambda e: self.geometry("1200x800"))
		else:
			self.geometry("1200x800")

	def _build_ui(self, logo_path: Path) -> None:
		root = ttk.Frame(self)
		root.pack(fill="both", expand=True)

		header = ttk.Frame(root)
		header.pack(fill="x", padx=12, pady=8)
		try:
			logo_img = Image.open(logo_path).resize((48, 48))
			self._logo_photo = ImageTk.PhotoImage(logo_img)
			logo_lbl = ttk.Label(header, image=self._logo_photo)
			logo_lbl.pack(side="left", padx=(0, 8))
		except Exception:
			pass
		title_lbl = ttk.Label(header, text=CONFIG.restaurant_legal_name, font=("Segoe UI", 18, "bold"))
		title_lbl.pack(side="left")
		user_lbl = ttk.Label(header, text=f"User: {self.current_user['full_name']} ({self.current_user['role']})")
		user_lbl.pack(side="right")

		toolbar = ttk.Frame(root)
		toolbar.pack(fill="x", padx=12, pady=(0,8))
		self.btn_manage_users = ttk.Button(toolbar, text="Users", command=lambda: messagebox.showinfo("Users", "Manage Users"))
		self.btn_manage_users.pack(side="left", padx=4)
		self.btn_menu = ttk.Button(toolbar, text="Menu", command=lambda: messagebox.showinfo("Menu", "Manage Menu"))
		self.btn_menu.pack(side="left", padx=4)
		self.btn_reports = ttk.Button(toolbar, text="Reports", command=lambda: messagebox.showinfo("Reports", "View Reports"))
		self.btn_reports.pack(side="left", padx=4)
		self.btn_new_order = ttk.Button(toolbar, text="New Order", command=lambda: messagebox.showinfo("Order", "Create Order"))
		self.btn_new_order.pack(side="left", padx=4)
		self.btn_checkout = ttk.Button(toolbar, text="Checkout", command=lambda: messagebox.showinfo("Checkout", "Checkout Bill"))
		self.btn_checkout.pack(side="left", padx=4)
		self.btn_lookup = ttk.Button(toolbar, text="Find Bill", command=self._lookup_bill)
		self.btn_lookup.pack(side="left", padx=4)
		self.btn_settings = ttk.Button(toolbar, text="Settings", command=self._open_settings)
		self.btn_settings.pack(side="left", padx=4)

		body = ttk.Frame(root)
		body.pack(fill="both", expand=True, padx=12, pady=8)
		self.body_text = tk.Text(body, height=10)
		self.body_text.pack(fill="both", expand=True)
		self.body_text.insert("1.0", "Welcome. UI under construction.\n")

		footer = ttk.Frame(root)
		footer.pack(fill="x", padx=12, pady=8)
		license_lbl = ttk.Label(footer, text=f"Licensed to: {CONFIG.licensee}")
		license_lbl.pack(side="right")
		dev_lbl = ttk.Label(footer, text=f"Developed by: {CONFIG.developed_by} | © All rights reserved to {CONFIG.rights_owner}")
		dev_lbl.pack(side="left")

	def _set_state(self, widget: ttk.Button, allowed: bool) -> None:
		widget.state(["!disabled"]) if allowed else widget.state(["disabled"])

	def _apply_permissions(self) -> None:
		user = self.current_user
		self._set_state(self.btn_manage_users, user_can(user, A_MANAGE_USERS))
		self._set_state(self.btn_menu, user_can(user, A_MANAGE_MENU))
		self._set_state(self.btn_reports, user_can(user, A_VIEW_REPORTS))
		self._set_state(self.btn_new_order, user_can(user, A_CREATE_ORDER))
		self._set_state(self.btn_checkout, user_can(user, A_CHECKOUT_BILL))
		self._set_state(self.btn_lookup, user_can(user, A_LOOKUP_BILL))
		self._set_state(self.btn_settings, user_can(user, A_CONFIGURE_SETTINGS))

	def _open_settings(self):
		if not user_can(self.current_user, A_CONFIGURE_SETTINGS):
			messagebox.showwarning("Permission Denied", "You do not have access to Settings.")
			return
		sent = send_message("Test message from HUNGER Restaurant Billing")
		if sent:
			messagebox.showinfo("Telegram", "Test message sent.")
		else:
			messagebox.showerror("Telegram", "Failed to send. Configure bot token and chat id in config.")

	def _lookup_bill(self):
		if not user_can(self.current_user, A_LOOKUP_BILL):
			messagebox.showwarning("Permission Denied", "You do not have access to Bill Lookup.")
			return
		dlg = PromptDialog(self, "Find Bill", "Enter Invoice Number:")
		invoice_no = dlg.result
		if not invoice_no:
			return
		order = get_order_by_invoice(invoice_no)
		self.body_text.delete("1.0", tk.END)
		if not order:
			self.body_text.insert("1.0", f"Invoice {invoice_no} not found.\n")
			return
		lines = [
			f"Invoice: {order['invoice_number']}",
			f"Date: {order['invoice_date']}",
			f"Status: {order['status']}",
			f"Subtotal: {order['subtotal']}",
			f"CGST: {order['cgst']} SGST: {order['sgst']} IGST: {order['igst']}",
			f"Service Charge: {order['service_charge']}",
			f"Total: {order['total']}",
			"Items:",
		]
		for item in order["items"]:
			lines.append(f" - {item['item_name']} x{item['quantity']} @ {item['rate']} = {item['line_amount']}")
		self.body_text.insert("1.0", "\n".join(lines) + "\n")


def bootstrap() -> None:
	init_db()
	logo = Path.cwd() / "logo.png"
	app = RestaurantApp(logo)
	app.mainloop()
