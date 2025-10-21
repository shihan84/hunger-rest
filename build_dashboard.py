#!/usr/bin/env python3
"""
GitHub Actions Build Dashboard
Interactive dashboard for monitoring builds
"""

import requests
import time
import json
import os
import sys
from datetime import datetime

class BuildDashboard:
    def __init__(self):
        self.repo_owner = "shihan84"
        self.repo_name = "hunger-rest"
        self.api_base = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        
    def get_workflow_runs(self):
        """Get workflow runs"""
        url = f"{self.api_base}/actions/runs?per_page=10"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_workflow_details(self, run_id):
        """Get workflow run details"""
        url = f"{self.api_base}/actions/runs/{run_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_jobs(self, run_id):
        """Get jobs for a workflow run"""
        url = f"{self.api_base}/actions/runs/{run_id}/jobs"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def display_dashboard(self):
        """Display the main dashboard"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🚀 HUNGER Restaurant Billing - Build Dashboard")
        print("=" * 60)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        data = self.get_workflow_runs()
        if not data or 'workflow_runs' not in data:
            print("❌ No workflow data available")
            return
        
        runs = data['workflow_runs']
        
        # Group runs by workflow
        workflows = {}
        for run in runs:
            name = run['name']
            if name not in workflows:
                workflows[name] = []
            workflows[name].append(run)
        
        # Display each workflow
        for workflow_name, workflow_runs in workflows.items():
            print(f"📋 {workflow_name}")
            print("-" * 40)
            
            for run in workflow_runs[:3]:  # Show last 3 runs
                status_emoji = self.get_status_emoji(run['status'], run.get('conclusion'))
                
                print(f"  {status_emoji} Run #{run['run_number']} - {run['status']}")
                print(f"     Branch: {run['head_branch']}")
                print(f"     Created: {run['created_at'][:19]}")
                print(f"     URL: {run['html_url']}")
                
                if run['status'] == 'in_progress':
                    print("     🔄 Currently running...")
                elif run['status'] == 'completed':
                    conclusion = run.get('conclusion', 'unknown')
                    print(f"     Result: {conclusion}")
                
                print()
        
        print("💡 Commands:")
        print("  r - Refresh")
        print("  o - Open GitHub Actions")
        print("  l - Open latest run")
        print("  q - Quit")
        print("  [number] - View run details")
    
    def get_status_emoji(self, status, conclusion):
        """Get emoji for status"""
        if status == 'completed':
            return '✅' if conclusion == 'success' else '❌'
        elif status == 'in_progress':
            return '🔄'
        elif status == 'queued':
            return '⏳'
        else:
            return '❓'
    
    def open_github_actions(self):
        """Open GitHub Actions page"""
        url = f"https://github.com/{self.repo_owner}/{self.repo_name}/actions"
        print(f"🌐 Opening: {url}")
        if os.name == 'posix':
            os.system(f"open '{url}'")
        else:
            os.system(f"start '{url}'")
    
    def open_latest_run(self):
        """Open the latest workflow run"""
        data = self.get_workflow_runs()
        if data and 'workflow_runs' in data and data['workflow_runs']:
            latest_run = data['workflow_runs'][0]
            url = latest_run['html_url']
            print(f"🔗 Opening: {url}")
            if os.name == 'posix':
                os.system(f"open '{url}'")
            else:
                os.system(f"start '{url}'")
        else:
            print("❌ No runs found")
    
    def show_run_details(self, run_number):
        """Show detailed information about a specific run"""
        data = self.get_workflow_runs()
        if not data or 'workflow_runs' not in data:
            print("❌ No data available")
            return
        
        # Find the run by number
        target_run = None
        for run in data['workflow_runs']:
            if str(run['run_number']) == str(run_number):
                target_run = run
                break
        
        if not target_run:
            print(f"❌ Run #{run_number} not found")
            return
        
        print(f"\n📋 Run #{run_number} Details")
        print("=" * 40)
        print(f"Name: {target_run['name']}")
        print(f"Status: {target_run['status']}")
        print(f"Conclusion: {target_run.get('conclusion', 'N/A')}")
        print(f"Branch: {target_run['head_branch']}")
        print(f"Commit: {target_run['head_sha'][:8]}")
        print(f"Created: {target_run['created_at']}")
        print(f"Updated: {target_run['updated_at']}")
        print(f"URL: {target_run['html_url']}")
        
        # Get job details
        jobs_data = self.get_jobs(target_run['id'])
        if jobs_data and 'jobs' in jobs_data:
            print(f"\n📋 Jobs:")
            for job in jobs_data['jobs']:
                job_emoji = self.get_status_emoji(job['status'], job.get('conclusion')')
                print(f"  {job_emoji} {job['name']} - {job['status']}")
                if job.get('conclusion'):
                    print(f"     Result: {job['conclusion']}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the interactive dashboard"""
        while True:
            self.display_dashboard()
            
            try:
                command = input("\nEnter command: ").strip().lower()
                
                if command == 'q' or command == 'quit':
                    print("👋 Goodbye!")
                    break
                elif command == 'r' or command == 'refresh':
                    continue
                elif command == 'o' or command == 'open':
                    self.open_github_actions()
                    input("Press Enter to continue...")
                elif command == 'l' or command == 'latest':
                    self.open_latest_run()
                    input("Press Enter to continue...")
                elif command.isdigit():
                    self.show_run_details(command)
                else:
                    print("❌ Unknown command")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")

def main():
    dashboard = BuildDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
