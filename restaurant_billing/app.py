import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path
import platform

# Try to import PIL, but make it optional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL (Pillow) not available. Logo functionality will be disabled.")

from .config import CONFIG
from .db import init_db, get_order_by_invoice, list_menu_items, create_order, list_open_orders, mark_order_paid
from .auth import verify_password, get_user, seed_super_admin, user_can, A_MANAGE_USERS, A_MANAGE_MENU, A_VIEW_REPORTS, A_CREATE_ORDER, A_CHECKOUT_BILL, A_CONFIGURE_SETTINGS, A_LOOKUP_BILL
from .telegram_bot import send_message
from .gst import compute_gst_for_order_items
from .utils import format_currency_inr
from .payments import generate_upi_qr, tk_image_from_path
from .updater import run_update, check_and_notify_updates, get_update_settings, save_update_settings


def _macos_fullscreen_supported() -> bool:
	# Temporarily disabled version check for development
	return True
	# if platform.system() != "Darwin":
	# 	return True
	# ver = platform.mac_ver()[0]
	# try:
	# 	parts = [int(p) for p in ver.split(".") if p.isdigit()]
	# 	if len(parts) >= 2:
	# 		major, minor = parts[0], parts[1]
	# 		return not (major == 14 and minor < 7)
	# 	return True
	# except Exception:
	# 	return False


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
		self.cart_items = []
		self._login_flow()
		self._build_ui(logo_path)
		self._apply_permissions()
		self._check_for_updates_on_startup()

	def _login_flow(self) -> None:
		seed_super_admin()
		auth_ok = False
		while not auth_ok:
			dlg = LoginDialog(self)
			if not dlg.result:
				self.destroy()
				return
			username, password = dlg.result
			user = get_user(username)
			if user and verify_password(password, user[4], user[5]):  # user[4] = password_hash, user[5] = password_salt
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
		if not PIL_AVAILABLE:
			return
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
				w = self.winfo_screenwidth(); h = self.winfo_screenheight(); self.geometry(f"{w}x{h}+0+0")
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
		self.btn_manage_users = ttk.Button(toolbar, text="Users", command=self._open_user_management)
		self.btn_manage_users.pack(side="left", padx=4)
		self.btn_menu = ttk.Button(toolbar, text="Menu", command=self._open_menu_management)
		self.btn_menu.pack(side="left", padx=4)
		self.btn_reports = ttk.Button(toolbar, text="Reports", command=self._send_today_sales)
		self.btn_reports.pack(side="left", padx=4)
		self.btn_new_order = ttk.Button(toolbar, text="New Order", command=self._open_order_screen)
		self.btn_new_order.pack(side="left", padx=4)
		self.btn_checkout = ttk.Button(toolbar, text="Checkout", command=self._open_payments)
		self.btn_checkout.pack(side="left", padx=4)
		self.btn_orders = ttk.Button(toolbar, text="Orders", command=self._open_orders_management)
		self.btn_orders.pack(side="left", padx=4)
		self.btn_print = ttk.Button(toolbar, text="Print", command=self._print_last_invoice)
		self.btn_print.pack(side="left", padx=4)
		self.btn_printer_config = ttk.Button(toolbar, text="Printer Config", command=self._open_printer_config)
		self.btn_printer_config.pack(side="left", padx=4)
		self.btn_lookup = ttk.Button(toolbar, text="Find Bill", command=self._lookup_bill)
		self.btn_lookup.pack(side="left", padx=4)
		self.btn_settings = ttk.Button(toolbar, text="Settings", command=self._open_settings)
		self.btn_settings.pack(side="left", padx=4)
		self.btn_update = ttk.Button(toolbar, text="Update", command=self._run_update)
		self.btn_update.pack(side="left", padx=4)
		self.btn_update_settings = ttk.Button(toolbar, text="Update Settings", command=self._open_update_settings)
		self.btn_update_settings.pack(side="left", padx=4)

		self.body = ttk.Frame(root)
		self.body.pack(fill="both", expand=True, padx=12, pady=8)
		self.body_text = tk.Text(self.body, height=10)
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
		self._set_state(self.btn_orders, user_can(user, A_CHECKOUT_BILL))
		self._set_state(self.btn_lookup, user_can(user, A_LOOKUP_BILL))
		self._set_state(self.btn_settings, user_can(user, A_CONFIGURE_SETTINGS))
		self._set_state(self.btn_update, self.current_user.get("role") == "SUPER_ADMIN")
		self._set_state(self.btn_update_settings, user_can(user, A_CONFIGURE_SETTINGS))

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

	def _open_order_screen(self):
		if not user_can(self.current_user, A_CREATE_ORDER):
			messagebox.showwarning("Permission Denied", "You do not have access to create orders.")
			return
		for child in self.body.winfo_children():
			child.destroy()
		container = ttk.Frame(self.body)
		container.pack(fill="both", expand=True)

		left = ttk.Frame(container)
		left.pack(side="left", fill="both", expand=True)
		right = ttk.Frame(container)
		right.pack(side="right", fill="y")

		# Menu list
		cols = ("name","price","gst","hsn","cat")
		self.menu_tree = ttk.Treeview(left, columns=cols, show="headings", height=12)
		for c in cols:
			self.menu_tree.heading(c, text=c.upper())
		self.menu_tree.pack(fill="both", expand=True)
		for m in list_menu_items():
			self.menu_tree.insert("", "end", iid=str(m["id"]), values=(m["name"], m["price"], m["gst_slab"], m["hsn_code"], m["category"]))

		# Cart
		cart_frame = ttk.LabelFrame(right, text="Cart")
		cart_frame.pack(fill="y", padx=6, pady=6)
		self.cart_items: list = []
		self.cart_list = tk.Listbox(cart_frame, height=10, width=36)
		self.cart_list.pack(padx=6, pady=6)
		qty_var = tk.StringVar(value="1")
		qty_entry = ttk.Entry(cart_frame, textvariable=qty_var, width=6)
		qty_entry.pack(padx=6)
		add_btn = ttk.Button(cart_frame, text="Add", command=lambda: self._add_to_cart(qty_var))
		add_btn.pack(pady=4)

		# Table and totals
		meta = ttk.LabelFrame(right, text="Details")
		meta.pack(fill="y", padx=6, pady=6)
		self.table_var = tk.StringVar(value="1")
		ttk.Label(meta, text="Table #").pack(anchor="w", padx=6)
		ttk.Entry(meta, textvariable=self.table_var, width=8).pack(padx=6, pady=(0,6))
		self.service_var = tk.StringVar(value=str(int(CONFIG.default_service_charge_percent)))
		ttk.Label(meta, text="Service %").pack(anchor="w", padx=6)
		ttk.Entry(meta, textvariable=self.service_var, width=8).pack(padx=6, pady=(0,6))

		self.totals_var = tk.StringVar(value="Total: ₹0.00")
		ttk.Label(meta, textvariable=self.totals_var).pack(anchor="w", padx=6, pady=(6,0))
		calc_btn = ttk.Button(meta, text="Recalculate", command=self._recalc_totals)
		calc_btn.pack(padx=6, pady=4)
		save_btn = ttk.Button(meta, text="Save Order", command=self._save_order)
		save_btn.pack(padx=6, pady=6)
		self._update_save_enabled(save_btn)

	def _update_save_enabled(self, btn: ttk.Button):
		allowed = user_can(self.current_user, A_CREATE_ORDER)
		self._set_state(btn, allowed)

	def _add_to_cart(self, qty_var: tk.StringVar):
		selection = self.menu_tree.selection()
		if not selection:
			return
		item_id = int(selection[0])
		vals = self.menu_tree.item(selection[0], 'values')
		name, price, gst_slab, hsn, cat = vals
		try:
			qty = int(qty_var.get() or "1")
		except ValueError:
			qty = 1
		entry = {"id": item_id, "name": name, "rate": float(price), "gst_slab": float(gst_slab), "hsn_code": hsn, "quantity": qty}
		self.cart_items.append(entry)
		self.cart_list.insert(tk.END, f"{name} x{qty} @ {price}")
		self._recalc_totals()

	def _collect_items_dict(self):
		items = {}
		for it in self.cart_items:
			items[it["name"]] = {"quantity": it["quantity"], "rate": it["rate"], "gst_slab": it["gst_slab"], "hsn_code": it["hsn_code"]}
		return items

	def _recalc_totals(self):
		try:
			service_pct = float(self.service_var.get() or 0)
		except ValueError:
			service_pct = 0.0
		res = compute_gst_for_order_items(self._collect_items_dict(), intra_state=True, service_charge_percent=service_pct)
		self._last_totals = res
		self.totals_var.set(f"Subtotal: {format_currency_inr(res['subtotal'])} | CGST: {format_currency_inr(res['cgst'])} | SGST: {format_currency_inr(res['sgst'])} | Total: {format_currency_inr(res['total'])}")

	def _save_order(self):
		if not self.cart_items:
			messagebox.showwarning("Empty", "No items in cart")
			return
		try:
			table_no = int(self.table_var.get() or "1")
		except ValueError:
			table_no = 1
		invoice = create_order(
			table_number=table_no,
			customer_name=None,
			customer_gstin=None,
			place_of_supply=None,
			totals=self._last_totals,
			items=self.cart_items,
			status='OPEN',
		)
		try:
			from .invoice import save_invoice_text
			from .einvoice import save_einvoice_json
			path = save_invoice_text(invoice)
			einvoice_path = save_einvoice_json(invoice)
			self._last_invoice = invoice
			msg = f"Order saved. Invoice: {invoice}\nSaved at: {path}"
			if einvoice_path:
				msg += f"\nE-invoice: {einvoice_path}"
			messagebox.showinfo("Saved", msg)
		except Exception:
			self._last_invoice = invoice
			messagebox.showinfo("Saved", f"Order saved. Invoice: {invoice}")

	def _print_last_invoice(self):
		if not getattr(self, "_last_invoice", None):
			messagebox.showwarning("No Invoice", "Save an order first.")
			return
		try:
			from .printing_fixed import print_invoice_full_width, configure_printer_for_full_width
			# Configure printer for full-width printing
			configure_printer_for_full_width()
			# Print with full-width formatting
			success = print_invoice_full_width(self._last_invoice)
			if success:
				messagebox.showinfo("Print", f"Invoice printed successfully with full-width formatting!")
			else:
				messagebox.showwarning("Print", f"Printing may have failed. Check printer connection.")
		except Exception as e:
			messagebox.showerror("Print", f"Failed: {e}")

	def _open_printer_config(self):
		"""Open printer configuration dialog"""
		try:
			from .printer_config import open_printer_config
			open_printer_config(self)
		except Exception as e:
			messagebox.showerror("Printer Config", f"Failed to open printer configuration: {e}")

	def _open_orders_management(self):
		if not user_can(self.current_user, A_CHECKOUT_BILL):
			messagebox.showwarning("Permission Denied", "You do not have access to Orders.")
			return
		for child in self.body.winfo_children():
			child.destroy()
		container = ttk.Frame(self.body)
		container.pack(fill="both", expand=True)
		
		# Open orders list
		orders_frame = ttk.LabelFrame(container, text="Open Orders")
		orders_frame.pack(fill="both", expand=True, padx=6, pady=6)
		
		cols = ("table", "invoice", "date", "total")
		self.orders_tree = ttk.Treeview(orders_frame, columns=cols, show="headings", height=12)
		for c in cols:
			self.orders_tree.heading(c, text=c.upper())
		self.orders_tree.pack(fill="both", expand=True, padx=6, pady=6)
		
		# Refresh and mark paid buttons
		btn_frame = ttk.Frame(orders_frame)
		btn_frame.pack(fill="x", padx=6, pady=6)
		ttk.Button(btn_frame, text="Refresh", command=self._refresh_orders).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Mark as Paid", command=self._mark_selected_paid).pack(side="left", padx=4)
		
		self._refresh_orders()

	def _refresh_orders(self):
		for item in self.orders_tree.get_children():
			self.orders_tree.delete(item)
		for order in list_open_orders():
			self.orders_tree.insert("", "end", iid=order["invoice_number"], values=(
				order["table_number"], order["invoice_number"], order["invoice_date"], format_currency_inr(order["total"])
			))

	def _mark_selected_paid(self):
		selection = self.orders_tree.selection()
		if not selection:
			messagebox.showwarning("No Selection", "Select an order to mark as paid.")
			return
		invoice = selection[0]
		if mark_order_paid(invoice):
			messagebox.showinfo("Success", f"Order {invoice} marked as PAID.")
			self._refresh_orders()
		else:
			messagebox.showerror("Error", "Failed to update order status.")

	def _open_menu_management(self):
		if not user_can(self.current_user, A_MANAGE_MENU):
			messagebox.showwarning("Permission Denied", "You do not have access to Menu Management.")
			return
		for child in self.body.winfo_children():
			child.destroy()
		container = ttk.Frame(self.body)
		container.pack(fill="both", expand=True)
		
		# Menu items list
		menu_frame = ttk.LabelFrame(container, text="Menu Items")
		menu_frame.pack(fill="both", expand=True, padx=6, pady=6)
		
		cols = ("name", "price", "category", "gst", "hsn", "type")
		self.menu_mgmt_tree = ttk.Treeview(menu_frame, columns=cols, show="headings", height=12)
		for c in cols:
			self.menu_mgmt_tree.heading(c, text=c.upper())
		self.menu_mgmt_tree.pack(fill="both", expand=True, padx=6, pady=6)
		
		# Add/Edit buttons
		btn_frame = ttk.Frame(menu_frame)
		btn_frame.pack(fill="x", padx=6, pady=6)
		ttk.Button(btn_frame, text="Add Item", command=self._add_menu_item).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Edit Item", command=self._edit_menu_item).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Delete Item", command=self._delete_menu_item).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Refresh", command=self._refresh_menu_mgmt).pack(side="left", padx=4)
		
		self._refresh_menu_mgmt()

	def _refresh_menu_mgmt(self):
		for item in self.menu_mgmt_tree.get_children():
			self.menu_mgmt_tree.delete(item)
		for item in list_menu_items():
			self.menu_mgmt_tree.insert("", "end", iid=str(item["id"]), values=(
				item["name"], item["price"], item["category"], item["gst_slab"], item["hsn_code"], item["food_type"]
			))

	def _add_menu_item(self):
		# Simple dialog for adding menu items
		dlg = MenuItemDialog(self, "Add Menu Item")
		if dlg.result:
			try:
				from .db import get_conn
				with get_conn() as conn:
					conn.execute(
						"INSERT INTO MenuItems (name, price, category, gst_slab, hsn_code, food_type) VALUES (?, ?, ?, ?, ?, ?)",
						(
							dlg.result["name"],
							float(dlg.result["price"]),
							dlg.result["category"],
							float(dlg.result["gst"]),
							dlg.result["hsn"],
							dlg.result["type"]
						)
					)
				messagebox.showinfo("Success", "Menu item added successfully!")
				self._refresh_menu_mgmt()
			except Exception as e:
				messagebox.showerror("Error", f"Failed to add menu item: {str(e)}")

	def _edit_menu_item(self):
		selection = self.menu_mgmt_tree.selection()
		if not selection:
			messagebox.showwarning("No Selection", "Select an item to edit.")
			return
		
		item_id = int(selection[0])
		# Get current item data
		from .db import get_conn
		with get_conn() as conn:
			cur = conn.execute("SELECT name, price, category, gst_slab, hsn_code, food_type FROM MenuItems WHERE id = ?", (item_id,))
			row = cur.fetchone()
			if not row:
				messagebox.showerror("Error", "Menu item not found.")
				return
		
		# Create edit dialog with current data
		current_data = {
			"name": row[0],
			"price": str(row[1]),
			"category": row[2],
			"gst_slab": str(row[3]),
			"hsn_code": row[4],
			"food_type": row[5]
		}
		dlg = MenuItemDialog(self, "Edit Menu Item", current_data)
		if dlg.result:
			try:
				with get_conn() as conn:
					conn.execute(
						"UPDATE MenuItems SET name=?, price=?, category=?, gst_slab=?, hsn_code=?, food_type=? WHERE id=?",
						(
							dlg.result["name"],
							float(dlg.result["price"]),
							dlg.result["category"],
							float(dlg.result["gst"]),
							dlg.result["hsn"],
							dlg.result["type"],
							item_id
						)
					)
				messagebox.showinfo("Success", "Menu item updated successfully!")
				self._refresh_menu_mgmt()
			except Exception as e:
				messagebox.showerror("Error", f"Failed to update menu item: {str(e)}")

	def _delete_menu_item(self):
		selection = self.menu_mgmt_tree.selection()
		if not selection:
			messagebox.showwarning("No Selection", "Select an item to delete.")
			return
		
		item_id = int(selection[0])
		# Get item name for confirmation
		from .db import get_conn
		with get_conn() as conn:
			cur = conn.execute("SELECT name FROM MenuItems WHERE id = ?", (item_id,))
			row = cur.fetchone()
			if not row:
				messagebox.showerror("Error", "Menu item not found.")
				return
			item_name = row[0]
		
		# Confirm deletion
		if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?"):
			try:
				with get_conn() as conn:
					conn.execute("DELETE FROM MenuItems WHERE id = ?", (item_id,))
				messagebox.showinfo("Success", "Menu item deleted successfully!")
				self._refresh_menu_mgmt()
			except Exception as e:
				messagebox.showerror("Error", f"Failed to delete menu item: {str(e)}")

	# Missing methods that are referenced in the UI but not implemented
	def _open_user_management(self):
		"""Open user management interface"""
		messagebox.showinfo("User Management", "User management feature is under development.")
		
	def _open_menu_management(self):
		"""Open menu management interface"""
		messagebox.showinfo("Menu Management", "Menu management feature is under development.")
		
	def _open_order_management(self):
		"""Open order management interface"""
		messagebox.showinfo("Order Management", "Order management feature is under development.")
		
	def _open_payment_system(self):
		"""Open payment system interface"""
		messagebox.showinfo("Payment System", "Payment system feature is under development.")
		
	def _open_reports(self):
		"""Open reports interface"""
		messagebox.showinfo("Reports", "Reports feature is under development.")
		
	def _open_settings(self):
		"""Open settings interface"""
		messagebox.showinfo("Settings", "Settings feature is under development.")
		
	def _open_printer_config(self):
		"""Open printer configuration"""
		messagebox.showinfo("Printer Config", "Printer configuration feature is under development.")
		
	def _open_update_settings(self):
		"""Open update settings"""
		messagebox.showinfo("Update Settings", "Update settings feature is under development.")
		
	def _send_today_sales(self):
		"""Send today's sales report"""
		messagebox.showinfo("Send Sales", "Send sales feature is under development.")
		
	def _check_for_updates_on_startup(self):
		"""Check for updates on startup"""
		pass  # Silent check, no UI needed


class MenuItemDialog(simpledialog.Dialog):
	def __init__(self, parent, title: str, initial_data: dict = None):
		self.result = None
		self.initial_data = initial_data or {}
		super().__init__(parent, title)

	def body(self, master):
		ttk.Label(master, text="Name").grid(row=0, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Price").grid(row=1, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Category").grid(row=2, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="GST %").grid(row=3, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="HSN Code").grid(row=4, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Type").grid(row=5, column=0, padx=6, pady=6, sticky="e")
		
		self.name_var = tk.StringVar(value=self.initial_data.get("name", ""))
		self.price_var = tk.StringVar(value=self.initial_data.get("price", ""))
		self.category_var = tk.StringVar(value=self.initial_data.get("category", ""))
		self.gst_var = tk.StringVar(value=self.initial_data.get("gst_slab", "5"))
		self.hsn_var = tk.StringVar(value=self.initial_data.get("hsn_code", "996331"))
		self.type_var = tk.StringVar(value=self.initial_data.get("food_type", "veg"))
		
		ttk.Entry(master, textvariable=self.name_var).grid(row=0, column=1, padx=6, pady=6)
		ttk.Entry(master, textvariable=self.price_var).grid(row=1, column=1, padx=6, pady=6)
		ttk.Entry(master, textvariable=self.category_var).grid(row=2, column=1, padx=6, pady=6)
		ttk.Entry(master, textvariable=self.gst_var).grid(row=3, column=1, padx=6, pady=6)
		ttk.Entry(master, textvariable=self.hsn_var).grid(row=4, column=1, padx=6, pady=6)
		
		type_combo = ttk.Combobox(master, textvariable=self.type_var, values=["veg", "non-veg"])
		type_combo.grid(row=5, column=1, padx=6, pady=6)
		
		return master

	def apply(self):
		self.result = {
			"name": self.name_var.get().strip(),
			"price": self.price_var.get().strip(),
			"category": self.category_var.get().strip(),
			"gst": self.gst_var.get().strip(),
			"hsn": self.hsn_var.get().strip(),
			"type": self.type_var.get().strip()
		}

	def _open_user_management(self):
		if not user_can(self.current_user, A_MANAGE_USERS):
			messagebox.showwarning("Permission Denied", "You do not have access to User Management.")
			return
		
		# Clear body and create user management interface
		for child in self.body.winfo_children():
			child.destroy()
		
		container = ttk.Frame(self.body)
		container.pack(fill="both", expand=True)
		
		# Users list
		users_frame = ttk.LabelFrame(container, text="Users")
		users_frame.pack(fill="both", expand=True, padx=6, pady=6)
		
		cols = ("id", "username", "full_name", "role")
		self.users_tree = ttk.Treeview(users_frame, columns=cols, show="headings", height=10)
		for c in cols:
			self.users_tree.heading(c, text=c.upper())
		self.users_tree.pack(fill="both", expand=True, padx=6, pady=6)
		
		# Buttons
		btn_frame = ttk.Frame(users_frame)
		btn_frame.pack(fill="x", padx=6, pady=6)
		ttk.Button(btn_frame, text="Add User", command=self._add_user).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Edit User", command=self._edit_user).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Change Password", command=self._change_password).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Delete User", command=self._delete_user).pack(side="left", padx=4)
		ttk.Button(btn_frame, text="Refresh", command=self._refresh_users).pack(side="left", padx=4)
		
		self._refresh_users()

	def _refresh_users(self):
		for item in self.users_tree.get_children():
			self.users_tree.delete(item)
		from .db import get_conn
		with get_conn() as conn:
			cur = conn.execute("SELECT id, username, full_name, role FROM Users ORDER BY id")
			for row in cur.fetchall():
				self.users_tree.insert("", "end", iid=str(row[0]), values=row)

	def _add_user(self):
		dlg = UserDialog(self, "Add User")
		if dlg.result:
			try:
				from .db import get_conn
				from .auth import create_user
				create_user(
					dlg.result["username"],
					dlg.result["password"],
					dlg.result["full_name"],
					dlg.result["role"]
				)
				messagebox.showinfo("Success", "User added successfully!")
				self._refresh_users()
			except Exception as e:
				messagebox.showerror("Error", f"Failed to add user: {str(e)}")

	def _edit_user(self):
		selection = self.users_tree.selection()
		if not selection:
			messagebox.showwarning("No Selection", "Select a user to edit.")
			return
		
		user_id = int(selection[0])
		from .db import get_conn
		with get_conn() as conn:
			cur = conn.execute("SELECT username, full_name, role FROM Users WHERE id = ?", (user_id,))
			row = cur.fetchone()
			if not row:
				messagebox.showerror("Error", "User not found.")
				return
		
		current_data = {
			"username": row[0],
			"full_name": row[1],
			"role": row[2]
		}
		dlg = UserDialog(self, "Edit User", current_data)
		if dlg.result:
			try:
				with get_conn() as conn:
					conn.execute(
						"UPDATE Users SET username=?, full_name=?, role=? WHERE id=?",
						(dlg.result["username"], dlg.result["full_name"], dlg.result["role"], user_id)
					)
				messagebox.showinfo("Success", "User updated successfully!")
				self._refresh_users()
			except Exception as e:
				messagebox.showerror("Error", f"Failed to update user: {str(e)}")

	def _change_password(self):
		selection = self.users_tree.selection()
		if not selection:
			messagebox.showwarning("No Selection", "Select a user to change password.")
			return
		
		user_id = int(selection[0])
		dlg = PasswordDialog(self, "Change Password")
		if dlg.result:
			try:
				from .db import get_conn
				from .auth import _hash_password, _generate_salt
				salt = _generate_salt()
				hashed = _hash_password(dlg.result, salt)
				with get_conn() as conn:
					conn.execute(
						"UPDATE Users SET password_hash=?, salt=? WHERE id=?",
						(hashed, salt.hex(), user_id)
					)
				messagebox.showinfo("Success", "Password changed successfully!")
			except Exception as e:
				messagebox.showerror("Error", f"Failed to change password: {str(e)}")

	def _delete_user(self):
		selection = self.users_tree.selection()
		if not selection:
			messagebox.showwarning("No Selection", "Select a user to delete.")
			return
		
		user_id = int(selection[0])
		# Get user info for confirmation
		from .db import get_conn
		with get_conn() as conn:
			cur = conn.execute("SELECT username, full_name, role FROM Users WHERE id = ?", (user_id,))
			row = cur.fetchone()
			if not row:
				messagebox.showerror("Error", "User not found.")
				return
			username, full_name, role = row
		
		# Prevent deleting the last SUPER_ADMIN
		if role == "SUPER_ADMIN":
			cur = conn.execute("SELECT COUNT(*) FROM Users WHERE role = 'SUPER_ADMIN'")
			count = cur.fetchone()[0]
			if count <= 1:
				messagebox.showerror("Error", "Cannot delete the last SUPER_ADMIN user.")
				return
		
		# Prevent deleting current user
		if user_id == self.current_user["id"]:
			messagebox.showerror("Error", "Cannot delete your own account.")
			return
		
		# Confirm deletion
		if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}' ({full_name})?"):
			try:
				with get_conn() as conn:
					conn.execute("DELETE FROM Users WHERE id = ?", (user_id,))
				messagebox.showinfo("Success", "User deleted successfully!")
				self._refresh_users()
			except Exception as e:
				messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

	def _open_payments(self):
		# Simple payment screen with UPI QR for the last calculated total (if any)
		for child in self.body.winfo_children():
			child.destroy()
		wrap = ttk.Frame(self.body)
		wrap.pack(fill="both", expand=True)
		amount = getattr(self, "_last_totals", {}).get("total", 0.0)
		vpa = getattr(CONFIG, "upi_vpa", None) or "test@upi"
		payee = CONFIG.restaurant_legal_name
		path = generate_upi_qr(vpa, payee, amount=amount, note=f"Table {getattr(self, 'table_var', tk.StringVar(value='')).get() if hasattr(self,'table_var') else ''}")
		img = tk_image_from_path(path)
		lbl = ttk.Label(wrap, image=img)
		lbl.image = img
		lbl.pack(pady=12)
		amt_lbl = ttk.Label(wrap, text=f"Pay {format_currency_inr(amount)} via UPI ({vpa})")
		amt_lbl.pack()

	def _send_today_sales(self):
		if not user_can(self.current_user, A_VIEW_REPORTS):
			messagebox.showwarning("Permission Denied", "You do not have access to Reports.")
			return
		try:
			from .telegram_bot import send_today_sales_summary
			ok = send_today_sales_summary()
			if ok:
				messagebox.showinfo("Telegram", "Today's sales summary sent.")
			else:
				messagebox.showerror("Telegram", "Failed to send. Configure bot token and chat id in config.")
		except Exception as e:
			messagebox.showerror("Telegram", f"Error: {e}")

	def _run_update(self):
		if self.current_user.get("role") != "SUPER_ADMIN":
			messagebox.showwarning("Permission Denied", "Only SUPER_ADMIN can update the app.")
			return
		ok, msg = run_update(Path.cwd())
		if ok:
			messagebox.showinfo("Update", f"Updated successfully.\n\n{msg}")
		else:
			messagebox.showerror("Update Failed", msg)

	def _check_for_updates_on_startup(self):
		"""Check for updates on application startup."""
		try:
			config_path = Path.cwd() / "data" / "update_config.json"
			settings = get_update_settings(config_path)
			
			if settings.get("auto_check_enabled", True):
				has_update, message = check_and_notify_updates(
					Path.cwd(), 
					config_path,
					settings.get("github_repo", "shihan84/hunger-rest")
				)
				
				if has_update and message and settings.get("notify_on_update", True):
					# Show update notification
					self.after(2000, lambda: self._show_update_notification(message))
		except Exception:
			# Silently fail if update check fails
			pass

	def _show_update_notification(self, message: str):
		"""Show update notification dialog."""
		from tkinter import messagebox
		result = messagebox.askyesno("Update Available", message)
		if result:
			self._run_update()

	def _open_update_settings(self):
		"""Open update settings dialog."""
		if not user_can(self.current_user, A_CONFIGURE_SETTINGS):
			messagebox.showwarning("Permission Denied", "You do not have access to Update Settings.")
			return
		
		dlg = UpdateSettingsDialog(self, "Update Settings")
		if dlg.result:
			config_path = Path.cwd() / "data" / "update_config.json"
			save_update_settings(config_path, dlg.result)
			messagebox.showinfo("Success", "Update settings saved successfully!")


class UserDialog(simpledialog.Dialog):
	def __init__(self, parent, title: str, initial_data: dict = None):
		self.result = None
		self.initial_data = initial_data or {}
		super().__init__(parent, title)

	def body(self, master):
		ttk.Label(master, text="Username").grid(row=0, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Full Name").grid(row=1, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Role").grid(row=2, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Password").grid(row=3, column=0, padx=6, pady=6, sticky="e")
		
		self.username_var = tk.StringVar(value=self.initial_data.get("username", ""))
		self.full_name_var = tk.StringVar(value=self.initial_data.get("full_name", ""))
		self.role_var = tk.StringVar(value=self.initial_data.get("role", "CAPTAIN"))
		self.password_var = tk.StringVar()
		
		ttk.Entry(master, textvariable=self.username_var).grid(row=0, column=1, padx=6, pady=6)
		ttk.Entry(master, textvariable=self.full_name_var).grid(row=1, column=1, padx=6, pady=6)
		
		role_combo = ttk.Combobox(master, textvariable=self.role_var, values=["SUPER_ADMIN", "ADMIN", "CAPTAIN", "CASHIER"])
		role_combo.grid(row=2, column=1, padx=6, pady=6)
		
		ttk.Entry(master, textvariable=self.password_var, show="*").grid(row=3, column=1, padx=6, pady=6)
		
		return master

	def apply(self):
		self.result = {
			"username": self.username_var.get().strip(),
			"full_name": self.full_name_var.get().strip(),
			"role": self.role_var.get().strip(),
			"password": self.password_var.get()
		}


class PasswordDialog(simpledialog.Dialog):
	def __init__(self, parent, title: str):
		self.result = None
		super().__init__(parent, title)

	def body(self, master):
		ttk.Label(master, text="New Password").grid(row=0, column=0, padx=6, pady=6, sticky="e")
		ttk.Label(master, text="Confirm Password").grid(row=1, column=0, padx=6, pady=6, sticky="e")
		
		self.password_var = tk.StringVar()
		self.confirm_var = tk.StringVar()
		
		ttk.Entry(master, textvariable=self.password_var, show="*").grid(row=0, column=1, padx=6, pady=6)
		ttk.Entry(master, textvariable=self.confirm_var, show="*").grid(row=1, column=1, padx=6, pady=6)
		
		return master

	def apply(self):
		password = self.password_var.get()
		confirm = self.confirm_var.get()
		
		if password != confirm:
			messagebox.showerror("Error", "Passwords do not match.")
			return
		
		if len(password) < 4:
			messagebox.showerror("Error", "Password must be at least 4 characters.")
			return
		
		self.result = password


class UpdateSettingsDialog(simpledialog.Dialog):
	def __init__(self, parent, title: str):
		self.result = None
		super().__init__(parent, title)

	def body(self, master):
		# Load current settings
		config_path = Path.cwd() / "data" / "update_config.json"
		settings = get_update_settings(config_path)
		
		# Auto check enabled
		ttk.Label(master, text="Auto Check for Updates").grid(row=0, column=0, padx=6, pady=6, sticky="w")
		self.auto_check_var = tk.BooleanVar(value=settings.get("auto_check_enabled", True))
		ttk.Checkbutton(master, variable=self.auto_check_var).grid(row=0, column=1, padx=6, pady=6, sticky="w")
		
		# Check interval
		ttk.Label(master, text="Check Interval (days)").grid(row=1, column=0, padx=6, pady=6, sticky="w")
		self.interval_var = tk.StringVar(value=str(settings.get("check_interval_days", 7)))
		interval_combo = ttk.Combobox(master, textvariable=self.interval_var, values=["1", "3", "7", "14", "30"])
		interval_combo.grid(row=1, column=1, padx=6, pady=6, sticky="w")
		
		# Notify on update
		ttk.Label(master, text="Notify on Update").grid(row=2, column=0, padx=6, pady=6, sticky="w")
		self.notify_var = tk.BooleanVar(value=settings.get("notify_on_update", True))
		ttk.Checkbutton(master, variable=self.notify_var).grid(row=2, column=1, padx=6, pady=6, sticky="w")
		
		# Auto install
		ttk.Label(master, text="Auto Install Updates").grid(row=3, column=0, padx=6, pady=6, sticky="w")
		self.auto_install_var = tk.BooleanVar(value=settings.get("auto_install", False))
		ttk.Checkbutton(master, variable=self.auto_install_var).grid(row=3, column=1, padx=6, pady=6, sticky="w")
		
		# GitHub repository
		ttk.Label(master, text="GitHub Repository").grid(row=4, column=0, padx=6, pady=6, sticky="w")
		self.repo_var = tk.StringVar(value=settings.get("github_repo", "shihan84/hunger-rest"))
		ttk.Entry(master, textvariable=self.repo_var, width=30).grid(row=4, column=1, padx=6, pady=6, sticky="w")
		
		return master

	def apply(self):
		self.result = {
			"auto_check_enabled": self.auto_check_var.get(),
			"check_interval_days": int(self.interval_var.get()),
			"notify_on_update": self.notify_var.get(),
			"auto_install": self.auto_install_var.get(),
			"github_repo": self.repo_var.get().strip()
		}


def bootstrap() -> None:
	init_db()
	logo = Path.cwd() / "logo.png"
	app = RestaurantApp(logo)
	app.mainloop()
