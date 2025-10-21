#!/usr/bin/env python3
"""
Create GitHub Release Script
Creates a release using the latest successful build artifacts
"""

import requests
import json
import sys
from datetime import datetime

class GitHubReleaseCreator:
    def __init__(self, repo_owner="shihan84", repo_name="hunger-rest"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        
    def get_latest_successful_run(self):
        """Get the latest successful build run"""
        url = f"{self.api_base}/actions/runs?per_page=10&status=completed"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Find the latest successful build run
            for run in data.get('workflow_runs', []):
                if (run['name'] == 'Build and Package HUNGER Restaurant Billing System' and 
                    run['conclusion'] == 'success'):
                    return run
                    
            return None
        except Exception as e:
            print(f"❌ Error fetching runs: {e}")
            return None
    
    def get_artifacts(self, run_id):
        """Get artifacts for a specific run"""
        url = f"{self.api_base}/actions/runs/{run_id}/artifacts"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching artifacts: {e}")
            return None
    
    def create_release(self, version, title, body):
        """Create a GitHub release"""
        url = f"{self.api_base}/releases"
        
        data = {
            "tag_name": version,
            "name": title,
            "body": body,
            "draft": False,
            "prerelease": False
        }
        
        try:
            # Note: This requires authentication token
            print(f"📝 Would create release: {version}")
            print(f"   Title: {title}")
            print(f"   Body: {body[:100]}...")
            print("\n💡 To create the release manually:")
            print("1. Go to: https://github.com/shihan84/hunger-rest/releases")
            print("2. Click 'Create a new release'")
            print("3. Use the information above")
            return True
        except Exception as e:
            print(f"❌ Error creating release: {e}")
            return False
    
    def show_latest_build_info(self):
        """Show information about the latest successful build"""
        print("🔍 Finding latest successful build...")
        
        run = self.get_latest_successful_run()
        if not run:
            print("❌ No successful builds found")
            return False
        
        print(f"✅ Found successful build: #{run['run_number']}")
        print(f"   Created: {run['created_at']}")
        print(f"   URL: {run['html_url']}")
        
        # Get artifacts
        artifacts = self.get_artifacts(run['id'])
        if artifacts and 'artifacts' in artifacts:
            print(f"\n📦 Available artifacts:")
            for artifact in artifacts['artifacts']:
                print(f"   - {artifact['name']} ({artifact['size_in_bytes']} bytes)")
        else:
            print("❌ No artifacts found")
            return False
        
        # Create release info
        version = f"v1.0.{run['run_number']}"
        title = f"HUNGER Restaurant Billing System {version}"
        body = f"""## HUNGER Restaurant Billing System {version}

### What's New
- Automated build and packaging
- Cross-platform support (Windows, Linux, macOS)
- Self-contained packages with virtual environments
- Easy installation scripts

### Downloads
- **Windows**: HUNGER-Restaurant-Billing-Windows.zip
- **Linux**: HUNGER-Restaurant-Billing-Linux.tar.gz  
- **macOS**: HUNGER-Restaurant-Billing-macOS.tar.gz

### Installation
1. Download the package for your platform
2. Extract the archive
3. Run the installation script
4. Launch the application

### Default Login
- Username: `owner`
- Password: `1234`

### Features
- 🧾 Complete billing system with GST compliance
- 📱 Mobile API for restaurant apps
- 💳 UPI QR code generation
- 👥 User management with roles
- 📊 Sales reports and analytics
- 🔄 Automatic updates
- 🖥️ Cross-platform support

### Build Information
- Build Number: #{run['run_number']}
- Build Date: {run['created_at']}
- Commit: {run['head_sha'][:8]}
- Branch: {run['head_branch']}
"""
        
        print(f"\n📋 Release Information:")
        print(f"   Version: {version}")
        print(f"   Title: {title}")
        print(f"   Body length: {len(body)} characters")
        
        return self.create_release(version, title, body)

def main():
    creator = GitHubReleaseCreator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "info":
            creator.show_latest_build_info()
        elif command == "create":
            creator.show_latest_build_info()
        else:
            print("❌ Unknown command. Use: info or create")
    else:
        creator.show_latest_build_info()

if __name__ == "__main__":
    main()
