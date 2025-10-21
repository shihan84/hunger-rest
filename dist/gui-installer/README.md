# HUNGER Restaurant Billing (India GST)

Python Tkinter billing system with SQLite, India GST compliance, role-based login, Telegram notifications, and invoice lookup.

## 1) Installation

### Windows (recommended)
1. Install Python 3.11 (64-bit) and check "Add Python to PATH".
2. Option A: One-click batch
   ```bat
   install_windows.bat
   ```
3. Option B: GUI installer (PowerShell)
   - Right-click `install_windows_gui.ps1` > Run with PowerShell
   - Click Install, then Run App
4. Or manual:
   ```bash
   python -m pip install -r requirements.txt
   python main.py
   ```

### macOS
- Prefer Python 3.11 from the official website (bundles Tk). On macOS 14.6, system Tk may abort; using the official installer avoids this.
```bash
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pip install -r requirements.txt
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 main.py
```

## Notes
- Configure Telegram in `restaurant_billing/config.py`.
- Data stored in `data/restaurant.db`.
- Licensee: Varchaswaa Media Pvt Ltd. Restaurant: HUNGER Restaurant.

## 2) First Login
- Default SUPER_ADMIN account:
  - Username: `owner`
  - Password: `1234`

## 3) User Roles & Permissions
- SUPER_ADMIN: Users, Menu, Reports, New Order, Checkout, Settings, Find Bill
- ADMIN: Menu, Reports, New Order, Checkout
- CAPTAIN: New Order, Checkout

## 4) Features Overview
- India GST: CGST/SGST slabs, HSN code storage per item, per-order tax totals
- Menu management (schema ready), veg/non-veg flags
- Orders with `invoice_number`, service charge, totals, and HSN-wise item storage
- Invoice lookup by `invoice_number` (SUPER_ADMIN only)
- Telegram test notification (Settings) – configure token and chat ID
- Role-based access control

## 5) Configuration
Edit `restaurant_billing/config.py`:
- `licensee`, `restaurant_legal_name`
- `developed_by`, `rights_owner` (displayed in footer)
- `default_state_code`, `currency_symbol`, `default_service_charge_percent`
- `fullscreen` (set True on Windows if you prefer)
- `telegram_bot_token`, `telegram_chat_id`

## 6) Telegram Setup (Optional)
1. Create a bot with BotFather and get the token.
2. Obtain your chat ID (add the bot to the chat and use a finder bot or API).
3. Set values in `restaurant_billing/config.py`.
4. In the app, open Settings and send a test message.

## 7) Database
- SQLite file: `data/restaurant.db` (auto-created)
- Tables: `Restaurant`, `GSTSettings`, `MenuItems`, `Orders`, `OrderItems`, `Users`
- Seed: basic GST slabs, sample menu, and default SUPER_ADMIN user

## 8) Troubleshooting
- macOS 14.6 abort: use Python from the official website.
- `_tkinter` missing (on some Python builds): use the official installer or a Tk-enabled build.
- No sales totals: mark orders as `PAID` with valid `invoice_date` for reporting.

## 9) License
- Developed by: Varchaswaa Media Pvt Ltd
- © All rights reserved to Varchaswaa Media Pvt Ltd
- License granted to operate this software for HUNGER Restaurant. Redistribution or sublicensing requires prior written consent from Varchaswaa Media Pvt Ltd.

## 10) Support
- For customization (GST formats, printers, multi-language, e-invoicing), contact Varchaswaa Media Pvt Ltd.
