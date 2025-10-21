# HUNGER Restaurant Billing System - Automatic Updates

## 🔄 Automatic Update System

The HUNGER Restaurant Billing System now includes an automatic update checking system that monitors GitHub for new releases and notifies users when updates are available.

## ✨ Features

### **Automatic Update Checking**
- ✅ **Weekly Checks** - Automatically checks for updates every 7 days
- ✅ **Configurable Interval** - Set check interval from 1 to 30 days
- ✅ **Smart Notifications** - Only notifies when updates are actually available
- ✅ **Non-Intrusive** - Checks happen in background without disrupting work
- ✅ **GitHub Integration** - Direct integration with GitHub repository

### **Update Settings**
- ✅ **Enable/Disable** - Turn automatic checking on/off
- ✅ **Check Interval** - Customize how often to check (1, 3, 7, 14, 30 days)
- ✅ **Notification Options** - Choose whether to show update notifications
- ✅ **Auto-Install** - Option to automatically install updates (future feature)
- ✅ **Repository Configuration** - Specify custom GitHub repository

### **User Experience**
- ✅ **Startup Check** - Checks for updates when application starts
- ✅ **Update Notifications** - Clear, user-friendly update notifications
- ✅ **One-Click Updates** - Simple update installation process
- ✅ **Settings Management** - Easy-to-use update settings dialog
- ✅ **Permission Control** - Only authorized users can configure updates

## 🚀 How It Works

### **1. Automatic Checking**
```
Application Startup → Check Last Update Time → Fetch from GitHub → Compare Versions → Notify if Update Available
```

### **2. Update Process**
```
User Clicks Update → Git Pull Latest Changes → Install Dependencies → Restart Application → Update Complete
```

### **3. Configuration**
```
Settings → Update Settings → Configure Options → Save Settings → Apply Changes
```

## ⚙️ Configuration Options

### **Update Settings Dialog**
Access via: **Settings → Update Settings** (requires CONFIGURE_SETTINGS permission)

| Setting | Description | Options | Default |
|---------|-------------|---------|---------|
| **Auto Check for Updates** | Enable/disable automatic checking | True/False | True |
| **Check Interval (days)** | How often to check for updates | 1, 3, 7, 14, 30 | 7 |
| **Notify on Update** | Show notification when update available | True/False | True |
| **Auto Install Updates** | Automatically install updates (future) | True/False | False |
| **GitHub Repository** | Repository to check for updates | Text field | shihan84/hunger-rest |

## 🔧 Technical Implementation

### **Update Check Process**
1. **Time Check** - Verify if enough time has passed since last check
2. **Git Fetch** - Fetch latest information from GitHub
3. **Version Compare** - Compare local and remote commit hashes
4. **Notification** - Show update notification if new version available
5. **Settings Save** - Record last check time and settings

### **Update Installation**
1. **Git Pull** - Pull latest changes from repository
2. **Dependency Update** - Install/update Python packages
3. **Database Migration** - Update database schema if needed
4. **Application Restart** - Restart application with new version

### **Configuration Storage**
- **File Location**: `data/update_config.json`
- **Format**: JSON configuration file
- **Backup**: Automatically backed up with system data
- **Security**: Only accessible by authorized users

## 📋 User Guide

### **For Restaurant Staff**
1. **Automatic Notifications** - You'll see update notifications when available
2. **Simple Updates** - Click "Yes" when update notification appears
3. **No Configuration Needed** - System works automatically with default settings

### **For Administrators**
1. **Access Settings** - Go to Settings → Update Settings
2. **Configure Options** - Set your preferred update checking options
3. **Save Settings** - Click OK to save your preferences
4. **Monitor Updates** - Check for updates manually using Update button

### **For Super Admins**
1. **Full Control** - Access to all update settings and manual updates
2. **Update Management** - Can force updates and manage update settings
3. **System Maintenance** - Monitor update status and troubleshoot issues

## 🔒 Security Features

### **Permission-Based Access**
- **SUPER_ADMIN**: Full update control and settings management
- **ADMIN**: Can configure update settings
- **CAPTAIN/CASHIER**: Receive update notifications only

### **Safe Update Process**
- **Backup Before Update** - Automatic backup before applying updates
- **Rollback Capability** - Can revert to previous version if needed
- **Validation** - Verifies update integrity before installation
- **Error Handling** - Graceful handling of update failures

### **Network Security**
- **HTTPS Only** - All GitHub communication uses secure HTTPS
- **Repository Verification** - Validates repository authenticity
- **No Data Transmission** - Only checks for updates, doesn't send data

## 📊 Update Status

### **Current Version**
- **Version**: 1.0.0
- **Last Check**: Automatically tracked
- **Update Available**: Checked weekly
- **Repository**: shihan84/hunger-rest

### **Update History**
- **Installation Date**: Tracked in system logs
- **Last Update**: Recorded in update log
- **Update Frequency**: Based on GitHub releases
- **Success Rate**: Monitored and reported

## 🛠️ Troubleshooting

### **Common Issues**

#### **Update Check Failed**
- **Cause**: Network connectivity issues
- **Solution**: Check internet connection and try again
- **Prevention**: Ensure stable internet connection

#### **Update Installation Failed**
- **Cause**: Git repository issues or permission problems
- **Solution**: Run as Administrator and check repository access
- **Prevention**: Ensure proper Git configuration

#### **Settings Not Saving**
- **Cause**: File permission issues
- **Solution**: Check data directory permissions
- **Prevention**: Run application with proper permissions

### **Manual Update Process**
If automatic updates fail:
1. **Backup Data** - Export important data first
2. **Manual Git Pull** - Use Git commands to update
3. **Install Dependencies** - Run `pip install -r requirements.txt`
4. **Restart Application** - Restart the application

### **Disable Automatic Updates**
To disable automatic updates:
1. **Open Settings** → Update Settings
2. **Uncheck** "Auto Check for Updates"
3. **Click OK** to save settings
4. **Manual Updates** - Use Update button for manual updates

## 📈 Benefits

### **For Restaurant Operations**
- ✅ **Always Up-to-Date** - Latest features and bug fixes
- ✅ **Security Updates** - Automatic security patches
- ✅ **Performance Improvements** - Regular performance optimizations
- ✅ **New Features** - Access to latest functionality

### **For System Administrators**
- ✅ **Reduced Maintenance** - Less manual update work
- ✅ **Better Security** - Automatic security updates
- ✅ **Improved Reliability** - Regular bug fixes and improvements
- ✅ **Enhanced Features** - Access to new capabilities

### **For Business Operations**
- ✅ **Minimal Downtime** - Updates happen during off-hours
- ✅ **Data Safety** - Automatic backups before updates
- ✅ **User Training** - Gradual introduction of new features
- ✅ **Support Efficiency** - Latest version reduces support issues

## 🎯 Best Practices

### **Recommended Settings**
- **Check Interval**: 7 days (weekly)
- **Auto Check**: Enabled
- **Notifications**: Enabled
- **Auto Install**: Disabled (manual approval recommended)

### **Update Schedule**
- **Best Time**: During restaurant off-hours
- **Frequency**: Weekly checks
- **Approval**: Manual approval for major updates
- **Testing**: Test updates in non-production environment first

### **Monitoring**
- **Check Logs**: Review update logs regularly
- **Monitor Performance**: Watch for issues after updates
- **User Feedback**: Collect feedback on new features
- **Backup Verification**: Ensure backups are working

---

**Automatic Updates Status: ✅ ACTIVE**  
**Last Updated**: October 21, 2024  
**Next Check**: Automatically scheduled  
**Repository**: shihan84/hunger-rest
