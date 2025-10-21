#!/usr/bin/env python3
"""
GitHub Actions Build Notifier
Sends desktop notifications when builds complete
"""

import requests
import time
import json
import os
from datetime import datetime

def send_notification(title, message, sound=True):
    """Send desktop notification"""
    try:
        if os.system("which osascript > /dev/null 2>&1") == 0:  # macOS
            cmd = f'''osascript -e 'display notification "{message}" with title "{title}"' '''
            if sound:
                cmd += " -e 'beep'"
            os.system(cmd)
        elif os.system("which notify-send > /dev/null 2>&1") == 0:  # Linux
            cmd = f'notify-send "{title}" "{message}"'
            if sound:
                cmd += " -a 'GitHub Actions'"
            os.system(cmd)
        else:
            print(f"🔔 {title}: {message}")
    except Exception as e:
        print(f"❌ Notification failed: {e}")

def get_workflow_status():
    """Get current workflow status"""
    url = "https://api.github.com/repos/shihan84/hunger-rest/actions/runs?per_page=3"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching status: {e}")
        return None

def monitor_builds(interval=30):
    """Monitor builds and send notifications"""
    print("🔔 GitHub Actions Build Notifier")
    print("Monitoring builds for notifications...")
    print("Press Ctrl+C to stop")
    
    previous_runs = {}
    
    try:
        while True:
            data = get_workflow_status()
            if not data or 'workflow_runs' not in data:
                print("❌ No data available")
                time.sleep(interval)
                continue
            
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"\n⏰ {current_time} - Checking builds...")
            
            for run in data['workflow_runs']:
                run_id = run['id']
                run_name = run['name']
                status = run['status']
                conclusion = run.get('conclusion')
                
                # Check if this is a new completion
                if run_id not in previous_runs:
                    previous_runs[run_id] = {
                        'status': status,
                        'conclusion': conclusion,
                        'name': run_name
                    }
                    print(f"📝 New run detected: {run_name} (#{run['run_number']})")
                    continue
                
                # Check for status changes
                prev_status = previous_runs[run_id]['status']
                prev_conclusion = previous_runs[run_id]['conclusion']
                
                if prev_status != status or prev_conclusion != conclusion:
                    print(f"🔄 Status change detected for {run_name}")
                    
                    if status == 'completed':
                        if conclusion == 'success':
                            send_notification(
                                "✅ Build Success!",
                                f"{run_name} completed successfully",
                                sound=True
                            )
                            print(f"✅ {run_name} completed successfully!")
                        else:
                            send_notification(
                                "❌ Build Failed",
                                f"{run_name} failed - Check logs",
                                sound=True
                            )
                            print(f"❌ {run_name} failed!")
                    
                    # Update stored status
                    previous_runs[run_id] = {
                        'status': status,
                        'conclusion': conclusion,
                        'name': run_name
                    }
                else:
                    if status == 'in_progress':
                        print(f"🔄 {run_name} still running...")
                    elif status == 'completed':
                        print(f"✅ {run_name} completed ({conclusion})")
            
            print(f"⏳ Waiting {interval} seconds...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")

def main():
    import sys
    
    if len(sys.argv) > 1:
        interval = int(sys.argv[1])
    else:
        interval = 30
    
    print(f"🔔 Starting build notifier (checking every {interval} seconds)")
    monitor_builds(interval)

if __name__ == "__main__":
    main()
