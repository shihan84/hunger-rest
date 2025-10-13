import subprocess
import sys
from pathlib import Path
from typing import Tuple


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
