#!/usr/bin/env python3
"""
Trigger Professional Installer Build
Triggers the GitHub Actions workflow to build professional installer and create release
"""

import requests
import json
import sys
from datetime import datetime

class GitHubWorkflowTrigger:
    def __init__(self, repo_owner="shihan84", repo_name="hunger-rest"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        
    def trigger_workflow(self, workflow_name, inputs=None):
        """Trigger a GitHub Actions workflow"""
        url = f"{self.api_base}/actions/workflows/{workflow_name}/dispatches"
        
        data = {
            "ref": "master",
            "inputs": inputs or {}
        }
        
        try:
            # Note: This requires authentication token
            print(f"📝 Would trigger workflow: {workflow_name}")
            print(f"   Inputs: {inputs}")
            print(f"   URL: {url}")
            print("\n💡 To trigger the workflow manually:")
            print("1. Go to: https://github.com/shihan84/hunger-rest/actions")
            print("2. Click 'Build Professional Installer'")
            print("3. Click 'Run workflow'")
            print("4. Enter version: v1.0.0")
            print("5. Check 'Create GitHub release'")
            print("6. Click 'Run workflow'")
            return True
        except Exception as e:
            print(f"❌ Error triggering workflow: {e}")
            return False
    
    def show_workflow_info(self):
        """Show information about available workflows"""
        print("🔍 Available Workflows:")
        print("=" * 50)
        
        workflows = [
            {
                "name": "Build Professional Installer",
                "description": "Creates professional GUI installer with NSIS",
                "url": "https://github.com/shihan84/hunger-rest/actions/workflows/build-professional-installer.yml",
                "manual_trigger": True
            },
            {
                "name": "Build and Package HUNGER Restaurant Billing System", 
                "description": "Creates cross-platform packages",
                "url": "https://github.com/shihan84/hunger-rest/actions/workflows/build-and-package.yml",
                "manual_trigger": True
            },
            {
                "name": "Create Release",
                "description": "Creates GitHub release from existing artifacts",
                "url": "https://github.com/shihan84/hunger-rest/actions/workflows/create-release.yml",
                "manual_trigger": True
            }
        ]
        
        for i, workflow in enumerate(workflows, 1):
            print(f"\n{i}. {workflow['name']}")
            print(f"   Description: {workflow['description']}")
            print(f"   Manual Trigger: {'Yes' if workflow['manual_trigger'] else 'No'}")
            print(f"   URL: {workflow['url']}")
        
        print(f"\n💡 To trigger workflows manually:")
        print("1. Go to: https://github.com/shihan84/hunger-rest/actions")
        print("2. Click on the workflow you want to run")
        print("3. Click 'Run workflow'")
        print("4. Fill in the required inputs")
        print("5. Click 'Run workflow'")
        
        return workflows

def main():
    trigger = GitHubWorkflowTrigger()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "trigger":
            version = sys.argv[2] if len(sys.argv) > 2 else "v1.0.0"
            inputs = {
                "create_release": "true",
                "version": version
            }
            trigger.trigger_workflow("build-professional-installer.yml", inputs)
        elif command == "info":
            trigger.show_workflow_info()
        else:
            print("❌ Unknown command. Use: trigger, info")
    else:
        trigger.show_workflow_info()

if __name__ == "__main__":
    main()
