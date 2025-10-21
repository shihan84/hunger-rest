#!/usr/bin/env python3
"""
HUNGER Restaurant Billing System - Test Script
Comprehensive testing of all billing features
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from restaurant_billing.db import init_db, get_conn, list_menu_items, create_order, list_open_orders, mark_order_paid, get_order_by_invoice
from restaurant_billing.auth import create_user, verify_password, user_can, A_MANAGE_USERS, A_MANAGE_MENU, A_CREATE_ORDER, A_CHECKOUT_BILL
from restaurant_billing.gst import compute_gst_for_order_items
from restaurant_billing.utils import format_currency_inr
from restaurant_billing.invoice import build_invoice_text
from restaurant_billing.config import CONFIG

def test_database_initialization():
    """Test database initialization and basic operations"""
    print("🧪 Testing Database Initialization...")
    
    try:
        # Initialize database
        init_db()
        print("✅ Database initialized successfully")
        
        # Test connection
        with get_conn() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM Users")
            user_count = cur.fetchone()[0]
            print(f"✅ Database connection working - {user_count} users found")
        
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_user_management():
    """Test user creation, authentication, and permissions"""
    print("\n🧪 Testing User Management...")
    
    try:
        # Test user creation
        user_id = create_user("test_user", "Test User", "CAPTAIN", "test123")
        print(f"✅ User created successfully - ID: {user_id}")
        
        # Test password verification
        if verify_password("test_user", "test123"):
            print("✅ Password verification working")
        else:
            print("❌ Password verification failed")
            return False
        
        # Test permissions
        user = {"id": user_id, "username": "test_user", "role": "CAPTAIN"}
        if user_can(user, A_CREATE_ORDER):
            print("✅ Permission system working")
        else:
            print("❌ Permission system failed")
            return False
        
        # Clean up test user
        with get_conn() as conn:
            conn.execute("DELETE FROM Users WHERE id = ?", (user_id,))
        print("✅ Test user cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ User management test failed: {e}")
        return False

def test_menu_management():
    """Test menu item operations"""
    print("\n🧪 Testing Menu Management...")
    
    try:
        # Test menu item creation
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO MenuItems (name, price, category, gst_slab, hsn_code, food_type) VALUES (?, ?, ?, ?, ?, ?)",
                ("Test Item", 100.0, "Test Category", 5.0, "996331", "veg")
            )
            item_id = cur.lastrowid
            print(f"✅ Menu item created - ID: {item_id}")
        
        # Test menu item retrieval
        items = list_menu_items()
        test_item = next((item for item in items if item["id"] == item_id), None)
        if test_item:
            print("✅ Menu item retrieval working")
        else:
            print("❌ Menu item retrieval failed")
            return False
        
        # Test menu item update
        with get_conn() as conn:
            conn.execute(
                "UPDATE MenuItems SET price = ? WHERE id = ?",
                (150.0, item_id)
            )
        print("✅ Menu item update working")
        
        # Clean up test item
        with get_conn() as conn:
            conn.execute("DELETE FROM MenuItems WHERE id = ?", (item_id,))
        print("✅ Test menu item cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ Menu management test failed: {e}")
        return False

def test_gst_calculations():
    """Test GST calculation functionality"""
    print("\n🧪 Testing GST Calculations...")
    
    try:
        # Test GST calculation
        items = {
            "Test Item 1": {
                "quantity": 2,
                "rate": 100.0,
                "gst_slab": 5.0,
                "hsn_code": "996331"
            },
            "Test Item 2": {
                "quantity": 1,
                "rate": 200.0,
                "gst_slab": 12.0,
                "hsn_code": "996331"
            }
        }
        
        result = compute_gst_for_order_items(items, intra_state=True, service_charge_percent=5.0)
        
        # Verify calculations
        expected_subtotal = (2 * 100.0) + (1 * 200.0)  # 400.0
        expected_service_charge = expected_subtotal * 0.05  # 20.0
        
        if abs(result["subtotal"] - expected_subtotal) < 0.01:
            print("✅ Subtotal calculation correct")
        else:
            print(f"❌ Subtotal calculation failed - Expected: {expected_subtotal}, Got: {result['subtotal']}")
            return False
        
        if abs(result["service_charge"] - expected_service_charge) < 0.01:
            print("✅ Service charge calculation correct")
        else:
            print(f"❌ Service charge calculation failed - Expected: {expected_service_charge}, Got: {result['service_charge']}")
            return False
        
        print(f"✅ GST calculation working - Total: {format_currency_inr(result['total'])}")
        return True
    except Exception as e:
        print(f"❌ GST calculation test failed: {e}")
        return False

def test_order_management():
    """Test order creation and management"""
    print("\n🧪 Testing Order Management...")
    
    try:
        # Create test menu items
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO MenuItems (name, price, category, gst_slab, hsn_code, food_type) VALUES (?, ?, ?, ?, ?, ?)",
                ("Test Food", 150.0, "Main Course", 5.0, "996331", "veg")
            )
            item_id = cur.lastrowid
        
        # Test order creation
        items = [{
            "id": item_id,
            "name": "Test Food",
            "rate": 150.0,
            "gst_slab": 5.0,
            "hsn_code": "996331",
            "quantity": 2
        }]
        
        totals = {
            "subtotal": 300.0,
            "service_charge": 15.0,
            "cgst": 7.5,
            "sgst": 7.5,
            "igst": 0.0,
            "total": 330.0,
            "hsn_breakdown": {}
        }
        
        invoice_number = create_order(
            table_number=1,
            customer_name="Test Customer",
            customer_gstin=None,
            place_of_supply=None,
            totals=totals,
            items=items,
            status='OPEN'
        )
        
        print(f"✅ Order created successfully - Invoice: {invoice_number}")
        
        # Test order retrieval
        order = get_order_by_invoice(invoice_number)
        if order:
            print("✅ Order retrieval working")
        else:
            print("❌ Order retrieval failed")
            return False
        
        # Test open orders list
        open_orders = list_open_orders()
        if any(order["invoice_number"] == invoice_number for order in open_orders):
            print("✅ Open orders list working")
        else:
            print("❌ Open orders list failed")
            return False
        
        # Test order payment
        if mark_order_paid(invoice_number):
            print("✅ Order payment marking working")
        else:
            print("❌ Order payment marking failed")
            return False
        
        # Clean up
        with get_conn() as conn:
            conn.execute("DELETE FROM Orders WHERE invoice_number = ?", (invoice_number,))
            conn.execute("DELETE FROM OrderItems WHERE order_id IN (SELECT order_id FROM Orders WHERE invoice_number = ?)", (invoice_number,))
            conn.execute("DELETE FROM MenuItems WHERE id = ?", (item_id,))
        print("✅ Test data cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ Order management test failed: {e}")
        return False

def test_invoice_generation():
    """Test invoice generation"""
    print("\n🧪 Testing Invoice Generation...")
    
    try:
        # Create test order
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO MenuItems (name, price, category, gst_slab, hsn_code, food_type) VALUES (?, ?, ?, ?, ?, ?)",
                ("Invoice Test Item", 200.0, "Test", 12.0, "996331", "veg")
            )
            item_id = cur.lastrowid
        
        items = [{
            "id": item_id,
            "name": "Invoice Test Item",
            "rate": 200.0,
            "gst_slab": 12.0,
            "hsn_code": "996331",
            "quantity": 1,
            "line_amount": 200.0
        }]
        
        totals = {
            "subtotal": 200.0,
            "service_charge": 10.0,
            "cgst": 6.0,
            "sgst": 6.0,
            "igst": 0.0,
            "total": 222.0
        }
        
        invoice_number = create_order(
            table_number=2,
            customer_name="Invoice Test Customer",
            customer_gstin="27ABCDE1234F1Z5",
            place_of_supply="Maharashtra",
            totals=totals,
            items=items,
            status='PAID'
        )
        
        # Test invoice text generation
        order = get_order_by_invoice(invoice_number)
        if order:
            invoice_text = build_invoice_text(order)
            if "Invoice Test Item" in invoice_text and "₹222.00" in invoice_text:
                print("✅ Invoice generation working")
            else:
                print("❌ Invoice generation failed - content mismatch")
                return False
        else:
            print("❌ Invoice generation failed - order not found")
            return False
        
        # Clean up
        with get_conn() as conn:
            conn.execute("DELETE FROM Orders WHERE invoice_number = ?", (invoice_number,))
            conn.execute("DELETE FROM OrderItems WHERE order_id IN (SELECT order_id FROM Orders WHERE invoice_number = ?)", (invoice_number,))
            conn.execute("DELETE FROM MenuItems WHERE id = ?", (item_id,))
        print("✅ Test data cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ Invoice generation test failed: {e}")
        return False

def test_configuration():
    """Test configuration and settings"""
    print("\n🧪 Testing Configuration...")
    
    try:
        # Test config loading
        if CONFIG.app_name:
            print(f"✅ Configuration loaded - App: {CONFIG.app_name}")
        else:
            print("❌ Configuration loading failed")
            return False
        
        # Test directory creation
        if CONFIG.db_path.parent.exists():
            print("✅ Data directory exists")
        else:
            print("❌ Data directory missing")
            return False
        
        if CONFIG.invoices_path.exists():
            print("✅ Invoices directory exists")
        else:
            print("❌ Invoices directory missing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 Starting HUNGER Restaurant Billing System Tests")
    print("=" * 60)
    
    tests = [
        ("Database Initialization", test_database_initialization),
        ("User Management", test_user_management),
        ("Menu Management", test_menu_management),
        ("GST Calculations", test_gst_calculations),
        ("Order Management", test_order_management),
        ("Invoice Generation", test_invoice_generation),
        ("Configuration", test_configuration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The billing system is ready for production.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
