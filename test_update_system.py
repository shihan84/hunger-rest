#!/usr/bin/env python3
"""
HUNGER Restaurant Billing System - Update System Test
Test the automatic update checking functionality
"""

import sys
import os
from pathlib import Path
import json
import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from restaurant_billing.updater import (
    check_for_updates, 
    get_update_settings, 
    save_update_settings,
    should_check_for_updates,
    get_last_check_time,
    save_last_check_time
)

def test_update_settings():
    """Test update settings functionality"""
    print("🧪 Testing Update Settings...")
    
    try:
        # Test default settings
        config_path = Path.cwd() / "data" / "test_update_config.json"
        settings = get_update_settings(config_path)
        
        expected_defaults = {
            "auto_check_enabled": True,
            "check_interval_days": 7,
            "notify_on_update": True,
            "auto_install": False,
            "github_repo": "shihan84/hunger-rest"
        }
        
        for key, expected_value in expected_defaults.items():
            if settings.get(key) == expected_value:
                print(f"✅ Default setting '{key}' is correct: {settings[key]}")
            else:
                print(f"❌ Default setting '{key}' is incorrect: Expected {expected_value}, Got {settings.get(key)}")
                return False
        
        # Test saving settings
        test_settings = {
            "auto_check_enabled": False,
            "check_interval_days": 3,
            "notify_on_update": False,
            "auto_install": True,
            "github_repo": "test/repo"
        }
        
        save_update_settings(config_path, test_settings)
        
        # Test loading saved settings
        loaded_settings = get_update_settings(config_path)
        for key, expected_value in test_settings.items():
            if loaded_settings.get(key) == expected_value:
                print(f"✅ Setting '{key}' saved and loaded correctly: {loaded_settings[key]}")
            else:
                print(f"❌ Setting '{key}' not saved correctly: Expected {expected_value}, Got {loaded_settings.get(key)}")
                return False
        
        # Clean up test file
        if config_path.exists():
            config_path.unlink()
        
        print("✅ Update settings functionality working")
        return True
        
    except Exception as e:
        print(f"❌ Update settings test failed: {e}")
        return False

def test_check_interval():
    """Test update check interval functionality"""
    print("\n🧪 Testing Update Check Interval...")
    
    try:
        config_path = Path.cwd() / "data" / "test_interval_config.json"
        
        # Test with no previous check (should return True)
        if should_check_for_updates(config_path, 7):
            print("✅ First check (no previous check) returns True")
        else:
            print("❌ First check should return True")
            return False
        
        # Save current time
        save_last_check_time(config_path)
        
        # Test with recent check (should return False)
        if not should_check_for_updates(config_path, 7):
            print("✅ Recent check returns False")
        else:
            print("❌ Recent check should return False")
            return False
        
        # Test with old check (should return True)
        # Manually set an old timestamp
        with open(config_path, 'w') as f:
            old_time = datetime.datetime.now() - datetime.timedelta(days=8)
            json.dump({"last_update_check": old_time.isoformat()}, f)
        
        if should_check_for_updates(config_path, 7):
            print("✅ Old check returns True")
        else:
            print("❌ Old check should return True")
            return False
        
        # Clean up test file
        if config_path.exists():
            config_path.unlink()
        
        print("✅ Update check interval functionality working")
        return True
        
    except Exception as e:
        print(f"❌ Update check interval test failed: {e}")
        return False

def test_update_check():
    """Test update check functionality"""
    print("\n🧪 Testing Update Check...")
    
    try:
        # Test update check (this will try to fetch from GitHub)
        has_update, update_info = check_for_updates(Path.cwd(), "shihan84/hunger-rest")
        
        if isinstance(has_update, bool):
            print("✅ Update check returns boolean result")
        else:
            print("❌ Update check should return boolean")
            return False
        
        if update_info is None or isinstance(update_info, dict):
            print("✅ Update info is properly formatted")
        else:
            print("❌ Update info should be None or dict")
            return False
        
        print(f"✅ Update check completed - Has update: {has_update}")
        return True
        
    except Exception as e:
        print(f"❌ Update check test failed: {e}")
        return False

def test_config_file_creation():
    """Test configuration file creation"""
    print("\n🧪 Testing Configuration File Creation...")
    
    try:
        config_path = Path.cwd() / "data" / "test_config.json"
        
        # Ensure data directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Test saving settings
        test_settings = {
            "auto_check_enabled": True,
            "check_interval_days": 7,
            "notify_on_update": True,
            "auto_install": False,
            "github_repo": "shihan84/hunger-rest"
        }
        
        save_update_settings(config_path, test_settings)
        
        if config_path.exists():
            print("✅ Configuration file created successfully")
        else:
            print("❌ Configuration file not created")
            return False
        
        # Test file content
        with open(config_path, 'r') as f:
            content = json.load(f)
            if content.get('update_settings') == test_settings:
                print("✅ Configuration file content is correct")
            else:
                print("❌ Configuration file content is incorrect")
                return False
        
        # Clean up test file
        if config_path.exists():
            config_path.unlink()
        
        print("✅ Configuration file creation working")
        return True
        
    except Exception as e:
        print(f"❌ Configuration file creation test failed: {e}")
        return False

def run_update_tests():
    """Run all update system tests"""
    print("🚀 Starting HUNGER Restaurant Update System Tests")
    print("=" * 60)
    
    tests = [
        ("Update Settings", test_update_settings),
        ("Check Interval", test_check_interval),
        ("Update Check", test_update_check),
        ("Config File Creation", test_config_file_creation)
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
    print("📊 UPDATE SYSTEM TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All update system tests passed! Automatic updates are ready.")
        return True
    else:
        print("⚠️  Some update tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = run_update_tests()
    sys.exit(0 if success else 1)
