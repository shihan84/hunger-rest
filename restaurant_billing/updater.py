import subprocess
import sys
import json
import datetime
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import requests


def run_update(repo_path: Path) -> Tuple[bool, str]:
	"""Attempt to git pull and pip install -r requirements.txt. Returns (ok, message)."""
	try:
		# Ensure repo path
		cwd = str(repo_path)
		# Fetch and pull latest changes
		git_pull = subprocess.run(["git", "pull", "--rebase", "--autostash"], cwd=cwd, capture_output=True, text=True)
		if git_pull.returncode != 0:
			return False, f"git pull failed: {git_pull.stderr or git_pull.stdout}"
		# Install/upgrade dependencies
		req = Path(repo_path) / "requirements.txt"
		if req.exists():
			pip_cmd = [sys.executable, "-m", "pip", "install", "-r", str(req)]
			pip = subprocess.run(pip_cmd, cwd=cwd, capture_output=True, text=True)
			if pip.returncode != 0:
				return False, f"pip install failed: {pip.stderr or pip.stdout}"
		return True, git_pull.stdout.strip() or "Updated successfully"
	except Exception as e:
		return False, str(e)


def check_for_updates(repo_path: Path, github_repo: str = "shihan84/hunger-rest") -> Tuple[bool, Optional[Dict[str, Any]]]:
	"""Check for updates from GitHub repository. Returns (has_update, update_info)."""
	try:
		# Get current commit hash
		current_commit = subprocess.run(
			["git", "rev-parse", "HEAD"], 
			cwd=str(repo_path), 
			capture_output=True, 
			text=True
		).stdout.strip()
		
		# Fetch latest info from GitHub
		subprocess.run(["git", "fetch", "origin"], cwd=str(repo_path), capture_output=True)
		
		# Get remote commit hash
		remote_commit = subprocess.run(
			["git", "rev-parse", "origin/master"], 
			cwd=str(repo_path), 
			capture_output=True, 
			text=True
		).stdout.strip()
		
		if current_commit != remote_commit:
			# Get commit info
			commit_info = subprocess.run(
				["git", "log", "--oneline", "-1", "origin/master"], 
				cwd=str(repo_path), 
				capture_output=True, 
				text=True
			).stdout.strip()
			
			return True, {
				"current_commit": current_commit,
				"remote_commit": remote_commit,
				"commit_message": commit_info,
				"has_update": True
			}
		
		return False, None
	except Exception as e:
		return False, {"error": str(e)}


def get_last_check_time(config_path: Path) -> Optional[datetime.datetime]:
	"""Get the last update check time from config file."""
	try:
		if config_path.exists():
			with open(config_path, 'r') as f:
				config = json.load(f)
				last_check = config.get('last_update_check')
				if last_check:
					return datetime.datetime.fromisoformat(last_check)
	except Exception:
		pass
	return None


def save_last_check_time(config_path: Path) -> None:
	"""Save the current time as last update check time."""
	try:
		config_path.parent.mkdir(parents=True, exist_ok=True)
		config = {}
		if config_path.exists():
			with open(config_path, 'r') as f:
				config = json.load(f)
		
		config['last_update_check'] = datetime.datetime.now().isoformat()
		
		with open(config_path, 'w') as f:
			json.dump(config, f, indent=2)
	except Exception:
		pass


def should_check_for_updates(config_path: Path, check_interval_days: int = 7) -> bool:
	"""Check if enough time has passed since last update check."""
	last_check = get_last_check_time(config_path)
	if not last_check:
		return True
	
	time_diff = datetime.datetime.now() - last_check
	return time_diff.days >= check_interval_days


def check_and_notify_updates(repo_path: Path, config_path: Path, github_repo: str = "shihan84/hunger-rest") -> Tuple[bool, Optional[str]]:
	"""Check for updates and return notification message if update is available."""
	try:
		# Check if we should check for updates
		if not should_check_for_updates(config_path):
			return False, None
		
		# Check for updates
		has_update, update_info = check_for_updates(repo_path, github_repo)
		
		# Save check time
		save_last_check_time(config_path)
		
		if has_update and update_info:
			commit_msg = update_info.get('commit_message', 'New update available')
			message = f"🔄 Update Available!\n\n{commit_msg}\n\nClick 'Update' button to install the latest version."
			return True, message
		
		return False, None
	except Exception as e:
		return False, f"Update check failed: {str(e)}"


def get_update_settings(config_path: Path) -> Dict[str, Any]:
	"""Get update settings from config file."""
	default_settings = {
		"auto_check_enabled": True,
		"check_interval_days": 7,
		"notify_on_update": True,
		"auto_install": False,
		"github_repo": "shihan84/hunger-rest"
	}
	
	try:
		if config_path.exists():
			with open(config_path, 'r') as f:
				config = json.load(f)
				settings = config.get('update_settings', {})
				# Merge with defaults
				for key, value in default_settings.items():
					if key not in settings:
						settings[key] = value
				return settings
	except Exception:
		pass
	
	return default_settings


def save_update_settings(config_path: Path, settings: Dict[str, Any]) -> None:
	"""Save update settings to config file."""
	try:
		config_path.parent.mkdir(parents=True, exist_ok=True)
		config = {}
		if config_path.exists():
			with open(config_path, 'r') as f:
				config = json.load(f)
		
		config['update_settings'] = settings
		
		with open(config_path, 'w') as f:
			json.dump(config, f, indent=2)
	except Exception:
		pass
