#!/usr/bin/env python3
"""
GitHub Actions Build Monitor
Monitors and displays the status of GitHub Actions workflows
"""

import requests
import json
import time
from datetime import datetime
import sys

class GitHubActionsMonitor:
    def __init__(self, repo_owner="shihan84", repo_name="hunger-rest"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        
    def get_workflow_runs(self, workflow_name=None, status=None):
        """Get workflow runs from GitHub API"""
        url = f"{self.api_base}/actions/runs"
        params = {}
        
        if workflow_name:
            params['workflow_id'] = workflow_name
        if status:
            params['status'] = status
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching workflow runs: {e}")
            return None
    
    def get_workflow_details(self, run_id):
        """Get detailed information about a specific workflow run"""
        url = f"{self.api_base}/actions/runs/{run_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching workflow details: {e}")
            return None
    
    def get_jobs_for_run(self, run_id):
        """Get jobs for a specific workflow run"""
        url = f"{self.api_base}/actions/runs/{run_id}/jobs"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs: {e}")
            return None
    
    def format_duration(self, start_time, end_time=None):
        """Format duration between start and end times"""
        if not end_time:
            end_time = datetime.now()
        
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
        duration = end_time - start_time
        return str(duration).split('.')[0]  # Remove microseconds
    
    def display_workflow_runs(self, runs_data):
        """Display workflow runs in a formatted way"""
        if not runs_data or 'workflow_runs' not in runs_data:
            print("No workflow runs found.")
            return
            
        runs = runs_data['workflow_runs']
        print(f"\n🔄 GitHub Actions Workflow Status for {self.repo_owner}/{self.repo_name}")
        print("=" * 80)
        
        for run in runs[:10]:  # Show last 10 runs
            status_emoji = {
                'completed': '✅',
                'in_progress': '🔄',
                'queued': '⏳',
                'cancelled': '❌',
                'failure': '❌',
                'success': '✅'
            }.get(run['status'], '❓')
            
            conclusion_emoji = {
                'success': '✅',
                'failure': '❌',
                'cancelled': '⏹️',
                'skipped': '⏭️'
            }.get(run['conclusion'], '❓')
            
            # Format timestamps
            created_at = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
            updated_at = datetime.fromisoformat(run['updated_at'].replace('Z', '+00:00'))
            
            print(f"\n{status_emoji} {run['name']} (#{run['run_number']})")
            print(f"   Status: {run['status']} {conclusion_emoji if run['conclusion'] else ''}")
            print(f"   Triggered by: {run['triggering_actor']['login']}")
            print(f"   Branch: {run['head_branch']}")
            print(f"   Commit: {run['head_sha'][:8]}")
            print(f"   Created: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Updated: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if run['status'] == 'completed':
                duration = self.format_duration(run['created_at'], run['updated_at'])
                print(f"   Duration: {duration}")
            
            print(f"   URL: {run['html_url']}")
    
    def display_job_details(self, run_id):
        """Display detailed job information for a workflow run"""
        jobs_data = self.get_jobs_for_run(run_id)
        if not jobs_data or 'jobs' not in jobs_data:
            print("No job details found.")
            return
            
        jobs = jobs_data['jobs']
        print(f"\n📋 Job Details for Run #{run_id}")
        print("=" * 50)
        
        for job in jobs:
            status_emoji = {
                'completed': '✅',
                'in_progress': '🔄',
                'queued': '⏳',
                'cancelled': '❌',
                'failure': '❌',
                'success': '✅'
            }.get(job['status'], '❓')
            
            print(f"\n{status_emoji} {job['name']}")
            print(f"   Status: {job['status']}")
            print(f"   Conclusion: {job['conclusion'] or 'N/A'}")
            print(f"   Started: {job['started_at'] or 'Not started'}")
            print(f"   Completed: {job['completed_at'] or 'Not completed'}")
            
            if job['steps']:
                print("   Steps:")
                for step in job['steps']:
                    step_emoji = {
                        'completed': '✅',
                        'in_progress': '🔄',
                        'queued': '⏳',
                        'cancelled': '❌',
                        'failure': '❌',
                        'success': '✅'
                    }.get(step['status'], '❓')
                    
                    print(f"     {step_emoji} {step['name']} ({step['status']})")
    
    def monitor_live(self, interval=30):
        """Monitor workflows in real-time"""
        print(f"🔄 Starting live monitoring (checking every {interval} seconds)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking workflows...")
                
                # Get in-progress runs
                in_progress = self.get_workflow_runs(status='in_progress')
                if in_progress and in_progress.get('workflow_runs'):
                    print(f"🔄 {len(in_progress['workflow_runs'])} workflow(s) currently running")
                    self.display_workflow_runs(in_progress)
                else:
                    print("✅ No workflows currently running")
                
                # Get recent completed runs
                recent = self.get_workflow_runs()
                if recent and recent.get('workflow_runs'):
                    print(f"\n📊 Recent workflow runs:")
                    self.display_workflow_runs(recent)
                
                print(f"\n⏳ Waiting {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")
    
    def check_specific_run(self, run_id):
        """Check details of a specific workflow run"""
        run_details = self.get_workflow_details(run_id)
        if not run_details:
            print(f"❌ Could not fetch details for run {run_id}")
            return
            
        print(f"\n📋 Workflow Run Details: #{run_details['run_number']}")
        print("=" * 50)
        print(f"Name: {run_details['name']}")
        print(f"Status: {run_details['status']}")
        print(f"Conclusion: {run_details['conclusion'] or 'N/A'}")
        print(f"Triggered by: {run_details['triggering_actor']['login']}")
        print(f"Branch: {run_details['head_branch']}")
        print(f"Commit: {run_details['head_sha']}")
        print(f"Created: {run_details['created_at']}")
        print(f"Updated: {run_details['updated_at']}")
        print(f"URL: {run_details['html_url']}")
        
        # Show job details
        self.display_job_details(run_id)

def main():
    monitor = GitHubActionsMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "live":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            monitor.monitor_live(interval)
        elif command == "check":
            if len(sys.argv) > 2:
                run_id = sys.argv[2]
                monitor.check_specific_run(run_id)
            else:
                print("❌ Please provide a run ID: python monitor_builds.py check <run_id>")
        elif command == "jobs":
            if len(sys.argv) > 2:
                run_id = sys.argv[2]
                monitor.display_job_details(run_id)
            else:
                print("❌ Please provide a run ID: python monitor_builds.py jobs <run_id>")
        else:
            print("❌ Unknown command. Use: live, check, or jobs")
    else:
        # Default: show recent workflow runs
        print("📊 Recent GitHub Actions Workflow Runs")
        runs_data = monitor.get_workflow_runs()
        monitor.display_workflow_runs(runs_data)
        
        print("\n💡 Usage:")
        print("  python monitor_builds.py                    # Show recent runs")
        print("  python monitor_builds.py live [interval]     # Live monitoring")
        print("  python monitor_builds.py check <run_id>      # Check specific run")
        print("  python monitor_builds.py jobs <run_id>       # Show job details")

if __name__ == "__main__":
    main()
