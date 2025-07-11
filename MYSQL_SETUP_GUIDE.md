# MySQL Setup Guide for Windows

## Step 1: Install MySQL

### Method 1: Official MySQL Installer (Recommended)
1. Visit: https://dev.mysql.com/downloads/installer/
2. Download "MySQL Installer for Windows" (mysql-installer-web-community-8.x.x.msi)
3. Run the installer
4. Choose "Developer Default" or "Server Only" setup type
5. Follow the installation wizard
6. **Important**: Set a root password and remember it!

### Method 2: Using winget
```powershell
winget install Oracle.MySQL
```

## Step 2: Verify Installation

Open PowerShell as Administrator and run:
```powershell
mysql --version
```

If you get an error, MySQL might not be in your PATH. Try:
```powershell
# Check if MySQL service is running
Get-Service MySQL*

# Start MySQL service if it's stopped
Start-Service MySQL80  # or MySQL57, depending on version
```

## Step 3: Connect to MySQL

```powershell
mysql -u root -p
```
Enter your root password when prompted.

## Step 4: Create Your Database

Once connected to MySQL, you can run your schema file:

### Method 1: From MySQL command line
```sql
SOURCE C:/Users/ELOHOME/New folder (2)/Group5_database-prediction/database/teen_phone_addiction_schema.sql;
```

### Method 2: From PowerShell
```powershell
mysql -u root -p < "database/teen_phone_addiction_schema.sql"
```

## Step 5: Verify Database Creation

Connect to MySQL and check:
```sql
mysql -u root -p
SHOW DATABASES;
USE teen_phone_addiction_db;
SHOW TABLES;
```

## Troubleshooting

### MySQL not found in PATH
If MySQL is installed but not found, add it to PATH:
1. Find MySQL installation directory (usually `C:\Program Files\MySQL\MySQL Server 8.0\bin`)
2. Add this path to your system PATH environment variable
3. Restart PowerShell

### Service not running
```powershell
# Check service status
Get-Service MySQL*

# Start the service
Start-Service MySQL80
```

### Connection refused
- Make sure MySQL service is running
- Check if you're using the correct port (default: 3306)
- Verify username and password

## Alternative: Using MySQL Workbench

If you prefer a GUI:
1. Download MySQL Workbench from the same MySQL downloads page
2. Install and open it
3. Create a new connection to localhost
4. Open your `teen_phone_addiction_schema.sql` file
5. Execute the script
