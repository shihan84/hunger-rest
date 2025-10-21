# 🔍 GitHub Actions Build Monitoring

This directory contains several tools to monitor GitHub Actions builds for the HUNGER Restaurant Billing System.

## 📊 Available Monitoring Tools

### 1. **Quick Monitor** (`quick_monitor.py`)
Simple status checker with browser integration.

```bash
# Show current build status
python3 quick_monitor.py

# Open GitHub Actions page
python3 quick_monitor.py open

# Open latest run in browser
python3 quick_monitor.py latest
```

### 2. **Interactive Dashboard** (`build_dashboard.py`)
Full-featured interactive dashboard.

```bash
# Launch interactive dashboard
python3 build_dashboard.py
```

**Dashboard Commands:**
- `r` - Refresh status
- `o` - Open GitHub Actions page
- `l` - Open latest run
- `[number]` - View run details
- `q` - Quit

### 3. **Detailed Monitor** (`monitor_builds.py`)
Comprehensive monitoring with live updates.

```bash
# Show recent runs
python3 monitor_builds.py

# Live monitoring (every 30 seconds)
python3 monitor_builds.py live

# Live monitoring (every 60 seconds)
python3 monitor_builds.py live 60

# Check specific run
python3 monitor_builds.py check <run_id>

# Show job details
python3 monitor_builds.py jobs <run_id>
```

### 4. **Build Notifier** (`notify_builds.py`)
Desktop notifications for build completion.

```bash
# Monitor with notifications (every 30 seconds)
python3 notify_builds.py

# Monitor with notifications (every 60 seconds)
python3 notify_builds.py 60
```

### 5. **Shell Script** (`monitor_builds.sh`)
Quick shell-based monitoring.

```bash
# Show status
./monitor_builds.sh

# Open in browser
./monitor_builds.sh open

# Live monitoring
./monitor_builds.sh live 30
```

## 🚀 Quick Start

### Check Current Status
```bash
python3 quick_monitor.py
```

### Open GitHub Actions
```bash
python3 quick_monitor.py open
```

### Interactive Dashboard
```bash
python3 build_dashboard.py
```

## 📱 Desktop Notifications

The notifier script will send desktop notifications when:
- ✅ Builds complete successfully
- ❌ Builds fail
- 🔄 Build status changes

**Supported Systems:**
- macOS (using `osascript`)
- Linux (using `notify-send`)
- Fallback to console output

## 🔗 Direct Links

- **GitHub Actions**: https://github.com/shihan84/hunger-rest/actions
- **Repository**: https://github.com/shihan84/hunger-rest

## 📋 Build Status Meanings

| Status | Emoji | Meaning |
|--------|-------|---------|
| `completed` + `success` | ✅ | Build completed successfully |
| `completed` + `failure` | ❌ | Build failed |
| `in_progress` | 🔄 | Build currently running |
| `queued` | ⏳ | Build waiting to start |
| `cancelled` | ⏹️ | Build was cancelled |

## 🛠️ Troubleshooting

### No Data Available
- Check internet connection
- Verify repository exists: `shihan84/hunger-rest`
- Ensure GitHub API is accessible

### Notifications Not Working
- macOS: Ensure `osascript` is available
- Linux: Install `notify-send` package
- Check system notification settings

### Permission Errors
```bash
chmod +x *.py *.sh
```

## 🔄 Live Monitoring

For continuous monitoring during development:

```bash
# Terminal 1: Live status updates
python3 monitor_builds.py live 30

# Terminal 2: Desktop notifications
python3 notify_builds.py 60

# Terminal 3: Interactive dashboard
python3 build_dashboard.py
```

## 📊 Build Workflows

The repository has these main workflows:

1. **Build and Package** - Creates packages for Windows, Linux, macOS
2. **Continuous Integration** - Runs tests and checks
3. **Release** - Creates releases (triggered manually)

## 🎯 Pro Tips

1. **Use the dashboard** for detailed investigation of failed builds
2. **Set up notifications** to know immediately when builds complete
3. **Check specific runs** when debugging issues
4. **Use live monitoring** during active development
5. **Open GitHub Actions** for full logs and details

## 🔧 Customization

Edit the repository details in the scripts:
```python
REPO_OWNER = "shihan84"
REPO_NAME = "hunger-rest"
```

Change monitoring intervals:
```bash
python3 monitor_builds.py live 60  # Check every 60 seconds
```
