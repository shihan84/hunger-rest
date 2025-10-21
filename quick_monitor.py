#!/usr/bin/env python3
"""
Quick GitHub Actions Monitor
Simple script to check build status and open logs
"""

import requests
import webbrowser
import sys
from datetime import datetime

def get_latest_runs():
    """Get the latest workflow runs"""
    url = "https://api.github.com/repos/shihan84/hunger-rest/actions/runs?per_page=5"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def display_status():
    """Display current build status"""
    print("🔄 HUNGER Restaurant Billing - Build Status")
    print("=" * 50)
    
    data = get_latest_runs()
    if not data or 'workflow_runs' not in data:
        print("❌ No data available")
        return
    
    runs = data['workflow_runs']
    
    for run in runs:
        status_emoji = {
            'completed': '✅' if run.get('conclusion') == 'success' else '❌',
            'in_progress': '🔄',
            'queued': '⏳'
        }.get(run['status'], '❓')
        
        print(f"\n{status_emoji} {run['name']} (#{run['run_number']})")
        print(f"   Status: {run['status']}")
        print(f"   Conclusion: {run.get('conclusion', 'N/A')}")
        print(f"   Branch: {run['head_branch']}")
        print(f"   Created: {run['created_at'][:19]}")
        print(f"   URL: {run['html_url']}")
        
        # Show if currently running
        if run['status'] == 'in_progress':
            print("   🔄 Currently running...")

def open_actions_page():
    """Open GitHub Actions page in browser"""
    url = "https://github.com/shihan84/hunger-rest/actions"
    print(f"🌐 Opening GitHub Actions: {url}")
    webbrowser.open(url)

def open_latest_run():
    """Open the latest workflow run"""
    data = get_latest_runs()
    if data and 'workflow_runs' in data and data['workflow_runs']:
        latest_run = data['workflow_runs'][0]
        url = latest_run['html_url']
        print(f"🔗 Opening latest run: {url}")
        webbrowser.open(url)
    else:
        print("❌ No runs found")

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "open":
            open_actions_page()
        elif command == "latest":
            open_latest_run()
        elif command == "status":
            display_status()
        else:
            print("❌ Unknown command. Use: open, latest, or status")
    else:
        display_status()
        print("\n💡 Commands:")
        print("  python3 quick_monitor.py status  # Show status")
        print("  python3 quick_monitor.py open    # Open Actions page")
        print("  python3 quick_monitor.py latest   # Open latest run")

if __name__ == "__main__":
    main()
