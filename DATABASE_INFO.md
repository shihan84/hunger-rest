# HUNGER Restaurant Billing System - Database Information

## 🗄️ Database System Overview

The HUNGER Restaurant Billing System uses **SQLite** as its database system, which is a lightweight, file-based database that requires no separate installation or configuration.

## ✅ Database Features

### **Built-in Database**
- ✅ **SQLite Database** - No separate installation required
- ✅ **File-based Storage** - Database stored in `data/restaurant.db`
- ✅ **Automatic Creation** - Database created automatically on first run
- ✅ **Schema Management** - Automatic table creation and updates
- ✅ **Data Integrity** - Foreign key constraints and data validation

### **Database Components**
- ✅ **Restaurant Information** - Business details and settings
- ✅ **User Management** - User accounts and permissions
- ✅ **Menu Items** - Food items with pricing and GST information
- ✅ **Orders** - Customer orders and transactions
- ✅ **GST Settings** - Tax configuration and compliance
- ✅ **Invoice Data** - Complete billing and invoice records

## 📊 Database Schema

### **Core Tables**

#### **Restaurant Table**
```sql
CREATE TABLE Restaurant (
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    gstin TEXT NOT NULL,
    state_code TEXT NOT NULL,
    fssai_license TEXT
);
```

#### **Users Table**
```sql
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### **MenuItems Table**
```sql
CREATE TABLE MenuItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    gst_slab REAL NOT NULL,
    hsn_code TEXT NOT NULL,
    food_type TEXT NOT NULL CHECK(food_type IN ('veg','non-veg'))
);
```

#### **Orders Table**
```sql
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER,
    customer_name TEXT,
    customer_gstin TEXT,
    place_of_supply TEXT,
    invoice_number TEXT,
    invoice_date TEXT,
    subtotal REAL NOT NULL DEFAULT 0,
    cgst REAL NOT NULL DEFAULT 0,
    sgst REAL NOT NULL DEFAULT 0,
    igst REAL NOT NULL DEFAULT 0,
    service_charge REAL NOT NULL DEFAULT 0,
    total REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'OPEN',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### **OrderItems Table**
```sql
CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    rate REAL NOT NULL,
    line_amount REAL NOT NULL,
    gst_slab REAL NOT NULL,
    hsn_code TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);
```

#### **GSTSettings Table**
```sql
CREATE TABLE GSTSettings (
    slab_rate REAL NOT NULL,
    cgst_rate REAL NOT NULL,
    sgst_rate REAL NOT NULL,
    applicable_from TEXT NOT NULL
);
```

## 🔧 Database Management

### **Automatic Database Creation**
The database is automatically created when the application starts for the first time:

1. **Database File Location**: `data/restaurant.db`
2. **Schema Creation**: All tables created automatically
3. **Default Data**: Sample data and default users created
4. **Initialization**: Database ready for immediate use

### **Database Initialization Process**
```python
# Automatic initialization on first run
from restaurant_billing.db import init_db
init_db()  # Creates database and tables
```

### **Default Data Seeded**
- ✅ **Default Super Admin User**
  - Username: `owner`
  - Password: `1234`
  - Role: `SUPER_ADMIN`

- ✅ **GST Settings**
  - 5% GST slab (2.5% CGST + 2.5% SGST)
  - 12% GST slab (6% CGST + 6% SGST)
  - 18% GST slab (9% CGST + 9% SGST)

- ✅ **Sample Menu Items** (if configured)
- ✅ **Restaurant Information** (configurable)

## 📁 Database File Management

### **Database Location**
- **File Path**: `data/restaurant.db`
- **File Size**: Typically 1-10 MB depending on data
- **Backup**: Included in system backups
- **Portability**: Can be copied to other systems

### **Database Backup**
```bash
# Manual backup
copy "data\restaurant.db" "backup\restaurant_backup_%date%.db"

# Automatic backup (via uninstaller)
# Data is backed up before any major operations
```

### **Database Restoration**
```bash
# Restore from backup
copy "backup\restaurant_backup_2024-01-15.db" "data\restaurant.db"
```

## 🔒 Database Security

### **Data Protection**
- ✅ **File Permissions** - Database file protected by Windows permissions
- ✅ **User Authentication** - Password hashing with salt
- ✅ **Role-Based Access** - Database access controlled by application
- ✅ **Data Validation** - Input validation and constraints

### **Backup Strategy**
- ✅ **Regular Backups** - Database included in system backups
- ✅ **Before Updates** - Automatic backup before system updates
- ✅ **Manual Backups** - User can create manual backups
- ✅ **Recovery Options** - Multiple restore points available

## 🚀 Database Performance

### **SQLite Advantages**
- ✅ **Lightweight** - No separate database server required
- ✅ **Fast** - Optimized for single-user applications
- ✅ **Reliable** - ACID compliant transactions
- ✅ **Portable** - Database file can be moved anywhere
- ✅ **Zero Configuration** - Works out of the box

### **Performance Characteristics**
- **Startup Time**: < 1 second
- **Query Performance**: Sub-millisecond for typical operations
- **Concurrent Users**: Optimized for single-user restaurant operations
- **Data Capacity**: Can handle thousands of orders and menu items

## 📈 Database Monitoring

### **Database Health Checks**
- ✅ **File Integrity** - Automatic database file validation
- ✅ **Schema Validation** - Table structure verification
- ✅ **Data Consistency** - Foreign key constraint checking
- ✅ **Performance Monitoring** - Query execution time tracking

### **Maintenance Tasks**
- ✅ **Automatic Cleanup** - Old data archiving (if configured)
- ✅ **Index Optimization** - Automatic index maintenance
- ✅ **Vacuum Operations** - Database file optimization
- ✅ **Backup Verification** - Backup integrity checking

## 🛠️ Database Troubleshooting

### **Common Issues**

#### **Database File Not Found**
- **Cause**: Database file deleted or moved
- **Solution**: Application will recreate database automatically
- **Prevention**: Regular backups and file protection

#### **Database Corruption**
- **Cause**: System crash or file system issues
- **Solution**: Restore from backup or recreate database
- **Prevention**: Regular backups and system maintenance

#### **Permission Issues**
- **Cause**: Insufficient file permissions
- **Solution**: Run application as Administrator
- **Prevention**: Proper user account setup

### **Database Recovery**
1. **Stop Application** - Close the billing application
2. **Restore Backup** - Copy backup file to `data/restaurant.db`
3. **Restart Application** - Launch application normally
4. **Verify Data** - Check that all data is restored correctly

## 📋 Database Requirements

### **System Requirements**
- ✅ **No Additional Software** - SQLite is built into Python
- ✅ **File System Access** - Read/write access to data directory
- ✅ **Disk Space** - Minimal space required (1-10 MB)
- ✅ **Memory** - Low memory footprint

### **Installation Requirements**
- ✅ **Python 3.11+** - SQLite included with Python
- ✅ **Data Directory** - `data/` folder with write permissions
- ✅ **No Database Server** - No MySQL, PostgreSQL, or other databases needed
- ✅ **No Configuration** - Database works immediately

## 🎯 Database Benefits

### **For Restaurant Operations**
- ✅ **Simple Setup** - No database installation required
- ✅ **Reliable Storage** - ACID compliant transactions
- ✅ **Fast Performance** - Optimized for restaurant operations
- ✅ **Easy Backup** - Single file backup and restore

### **For System Administrators**
- ✅ **Zero Maintenance** - No database server to manage
- ✅ **Portable** - Database file can be moved anywhere
- ✅ **Lightweight** - Minimal system resource usage
- ✅ **Secure** - File-based security with Windows permissions

### **For Business Operations**
- ✅ **Data Integrity** - Reliable data storage and retrieval
- ✅ **Audit Trail** - Complete transaction history
- ✅ **Compliance** - GST and tax data properly stored
- ✅ **Scalability** - Handles growing business data

---

**Database Status: ✅ READY**  
**Type: SQLite (File-based)**  
**Location: `data/restaurant.db`**  
**Size: 1-10 MB (typical)**  
**Backup: Included in system backups**  
**Maintenance: Automatic**
