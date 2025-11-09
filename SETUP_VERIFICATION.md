# Odoo 18 Setup - Pre-Installation Verification & Instructions

## Your Questions Answered

### 1. ✅ ARM64 Compatibility Confirmation

**YES - All binaries and dependencies are ARM64 compatible:**

| Component | ARM64 Status | Source |
|-----------|--------------|--------|
| Ubuntu packages | ✅ Native | Ubuntu official ARM64 repos |
| PostgreSQL 15+ | ✅ Native | postgresql.org ARM64 builds |
| Python 3.10+ | ✅ Native | Built-in Ubuntu 22.04/24.04 |
| Python packages | ✅ Compatible | Compiled from source if needed |
| wkhtmltopdf | ✅ Works | Ubuntu ARM64 package (limited features) |
| Node.js/npm | ✅ Native | nodejs.org ARM64 builds |
| GCC/Build tools | ✅ Native | GNU toolchain for ARM64 |
| Image libraries | ✅ Native | libjpeg, libpng, etc. for ARM64 |
| **Odoo 18** | ✅ Compatible | Pure Python, works on any platform |

**ARM64 Optimizations Included:**
- Jemalloc memory allocator (ARM64-optimized)
- PostgreSQL tuned for ARM64
- Proper compiler flags for ARM64

---

### 2. ✅ Dependencies Accounted For

**ALL dependencies are included in the script:**

**System Dependencies (apt-get):**
```
✓ Python build tools (python3-dev, build-essential)
✓ Database client libraries (libpq-dev, postgresql-client)
✓ XML/XSLT processing (libxml2-dev, libxslt1-dev)
✓ LDAP support (libldap2-dev, libsasl2-dev)
✓ Image processing (libjpeg-dev, libpng-dev, libfreetype6-dev, etc.)
✓ Node.js ecosystem (nodejs, npm, node-less)
✓ PDF generation (wkhtmltopdf)
✓ SSL/TLS (libssl-dev)
✓ Compression libraries (zlib1g-dev, libbz2-dev, liblzma-dev)
✓ ARM64 optimization (libjemalloc2)
```

**Python Dependencies:**
```
✓ All from Odoo 18 requirements.txt
✓ Additional utilities (phonenumbers, pycountry)
✓ Automatically installed via pip
```

**Database:**
```
✓ PostgreSQL server + client
✓ Automatic user creation
✓ Performance optimization
```

---

### 3. ✅ What Gets Installed

**The script installs:**

1. **Odoo 18 CORE Files** (from official GitHub)
   - Source: https://github.com/odoo/odoo.git (branch 18.0)
   - Location: `/opt/odoo18/odoo18/`
   - Includes: All standard Odoo 18 addons

2. **Custom Modules** (linked from your repo)
   - `addons_custom/` → Linked from `/opt/justo-wrks/addons_custom/`
   - `demo_addons_custom/` → Linked from `/opt/justo-wrks/demo_addons_custom/`
   - **Note**: Standard Odoo files are NOT tracked in git (per optimization)

3. **Complete Setup:**
   - PostgreSQL database system
   - Python virtual environment with all dependencies
   - Systemd service for auto-start
   - Logging and monitoring
   - Security hardening

---

### 4. 🔥 Firewall Ports (OCI Security List)

**Configure these ports in OCI Security List:**

| Port | Protocol | Purpose | Priority |
|------|----------|---------|----------|
| **8069** | TCP | **Odoo HTTP** | **REQUIRED** |
| **8072** | TCP | Odoo Longpolling | Optional |
| **22** | TCP | SSH | Already configured |

**Firewall configuration REMOVED from script** ✅

**How to configure in OCI:**

```
1. Go to OCI Console
2. Navigate to: Networking → Virtual Cloud Networks
3. Select your VCN
4. Click "Security Lists"
5. Click your security list
6. Click "Add Ingress Rules"
7. Add rule:
   - Source CIDR: 0.0.0.0/0 (or restrict to your IP)
   - IP Protocol: TCP
   - Destination Port Range: 8069
8. Click "Add Ingress Rules" again for port 8072 (optional)
```

---

### 5. ✅ Auto-Generated Passwords

**Passwords are auto-generated** - No user intervention needed! ✅

**How it works:**
```bash
# Script automatically generates secure 32-character passwords:
DB_PASSWORD=$(openssl rand -base64 24 | tr -d "=+/" | cut -c1-32)
ADMIN_PASSWORD=$(openssl rand -base64 24 | tr -d "=+/" | cut -c1-32)
```

**Where passwords are saved:**
- Configuration file: `/etc/odoo18/odoo18.conf` (chmod 640)
- Credentials file: `/opt/odoo18/.credentials` (chmod 600)
- Installation log: `/var/log/odoo18_install.log`

**Access credentials after installation:**
```bash
sudo cat /opt/odoo18/.credentials
```

---

### 6. ✅ Automated Verification Tests

**7 comprehensive tests run automatically:**

| Test | What It Checks | Success Criteria |
|------|----------------|------------------|
| **1. Service Status** | Systemd service running | odoo18.service active |
| **2. Port Listening** | Port 8069 bound | netstat/ss shows LISTEN |
| **3. HTTP Endpoint** | Web interface responding | HTTP 200/303 response |
| **4. Log Files** | Logging working | odoo.log exists |
| **5. Database Connection** | PostgreSQL accessible | Can connect to DB |
| **6. Python Environment** | Odoo importable | Python imports Odoo |
| **7. Test Database** | Can create DB | Test DB creates successfully |

**Test execution:**
- Runs automatically after installation
- No user intervention required
- Displays pass/fail for each test
- Creates and cleans up test database
- Comprehensive results summary

**If tests fail:**
- Script provides diagnostic information
- Logs available at `/var/log/odoo18_install.log`
- Service logs: `journalctl -u odoo18 -n 100`

---

## 🚀 Execution Steps for Ubuntu Machine

### Step 1: Update Your Local Repository

```bash
# On your Ubuntu machine at /opt/justo-wrks
cd /opt/justo-wrks

# Pull latest changes
git fetch origin
git pull origin claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx

# Verify script is executable
chmod +x setup_odoo18_ubuntu.sh
```

### Step 2: Review Script (Optional)

```bash
# Check what the script will do
less setup_odoo18_ubuntu.sh

# Verify it's the latest version
head -20 setup_odoo18_ubuntu.sh
```

### Step 3: Run Installation

```bash
# Run the setup script with sudo
sudo bash setup_odoo18_ubuntu.sh

# The script will:
# - Display system information
# - Install all dependencies
# - Set up PostgreSQL
# - Install Odoo 18
# - Link your custom addons
# - Configure everything
# - Start Odoo service
# - Run 7 automated tests
# - Display summary with credentials
```

### Step 4: Monitor Installation

The script will show progress with emojis and status messages:
```
✅ Success messages
⚠️  Warning messages
ℹ️  Information messages
❌ Error messages (if any)
```

**Installation takes approximately 10-15 minutes** depending on internet speed.

### Step 5: Configure OCI Firewall

```bash
# While installation is running, configure OCI Security List:
# 1. Open OCI Console in browser
# 2. Add Ingress Rule for port 8069/TCP
# 3. Optionally add port 8072/TCP
```

### Step 6: Verify Installation

After installation completes, the script will display:
```
✅ INSTALLATION COMPLETE!

Test Results:
  Passed: 7/7
  Failed: 0/7

Access Odoo at: http://YOUR_SERVER_IP:8069
Admin Password: [displayed]
```

### Step 7: Access Odoo

```bash
# Get your server IP (if not shown)
hostname -I

# Open in browser:
http://YOUR_SERVER_IP:8069

# View saved credentials anytime:
sudo cat /opt/odoo18/.credentials
```

---

## 📋 Post-Installation Checks

### Check Service Status
```bash
sudo systemctl status odoo18
```

### View Live Logs
```bash
sudo journalctl -u odoo18 -f
```

### View Odoo Log File
```bash
sudo tail -f /var/log/odoo18/odoo.log
```

### Check Port Listening
```bash
sudo ss -tuln | grep 8069
```

### Test HTTP Endpoint
```bash
curl -I http://localhost:8069
```

---

## 🎯 What Happens During Installation

### Phase 1: System Dependencies (2-3 min)
- Updates Ubuntu packages
- Installs build tools, libraries
- Installs Node.js, PostgreSQL
- Installs ARM64 optimizations

### Phase 2: PostgreSQL Setup (1 min)
- Configures database
- Creates odoo18 user
- Optimizes for Odoo workload
- Tests connectivity

### Phase 3: Odoo User (10 sec)
- Creates system user: odoo18
- Sets up home directory
- Configures permissions

### Phase 4: Odoo 18 Installation (5-7 min)
- Clones Odoo 18 from GitHub
- Creates Python virtual environment
- Installs 50+ Python packages
- Verifies installation

### Phase 5: Custom Addons (10 sec)
- Links addons_custom/
- Links demo_addons_custom/
- Counts available modules
- Sets permissions

### Phase 6: Configuration (10 sec)
- Generates config file
- Sets auto-generated passwords
- Configures paths
- Saves credentials

### Phase 7: Systemd Service (10 sec)
- Creates service file
- Enables auto-start
- Adds ARM64 optimizations
- Security hardening

### Phase 8: Start Service (30 sec)
- Starts Odoo
- Waits for initialization
- Verifies service active

### Phase 9: Automated Tests (2-3 min)
- Runs 7 verification tests
- Creates test database
- Validates functionality
- Displays results

**Total Time: ~10-15 minutes**

---

## 🔐 Security Features

✅ Auto-generated secure passwords (32 chars)
✅ Credentials saved with 600 permissions
✅ Config file protected (640)
✅ Systemd security hardening
✅ PostgreSQL access control
✅ No passwords in command history
✅ Database manager disabled (list_db = False)

---

## 📊 Expected Output

```
============================================================
🚀 Odoo 18 Ubuntu ARM64 Automated Setup
============================================================

ℹ️  Starting preflight checks...
✅ ARM64 architecture detected
✅ Internet connectivity verified
✅ Preflight checks completed

============================================================
📦 Phase 1: Installing System Dependencies
============================================================
ℹ️  Updating package lists...
ℹ️  Installing core dependencies...
✅ System dependencies installed

[... continues through all 9 phases ...]

============================================================
🧪 Phase 9: Automated Verification Tests
============================================================

Test 1/7: Checking service status...
✅ ✓ Service is running

Test 2/7: Checking if port 8069 is listening...
✅ ✓ Port 8069 is listening

Test 3/7: Testing HTTP endpoint...
✅ ✓ HTTP endpoint responding

Test 4/7: Checking log files...
✅ ✓ Log file exists

Test 5/7: Testing database connection...
✅ ✓ Database connection successful

Test 6/7: Verifying Python environment...
✅ ✓ Python environment OK (Odoo version: 18.0)

Test 7/7: Creating and validating test database...
✅ ✓ Test database created successfully

============================================================
📊 Test Results Summary
============================================================
Total Tests: 7
Passed: 7
Failed: 0

✅ 🎉 All verification tests passed!

============================================================
✅ INSTALLATION COMPLETE!
============================================================

📋 Installation Summary:
  • Odoo Version: 18.0
  • Installation Path: /opt/odoo18
  • Configuration: /etc/odoo18/odoo18.conf

🔐 Security Information:
  • Admin Password: [32-char password]

🌐 Access Information:
  • URL: http://YOUR_IP:8069

⚠️  FIREWALL CONFIGURATION REQUIRED:
  Configure OCI Security List to allow:
  • Port 8069/TCP (Odoo HTTP)

🎉 Odoo 18 is ready to use!
```

---

## 🆘 Troubleshooting

### If installation fails:

1. **Check installation log:**
   ```bash
   cat /var/log/odoo18_install.log
   ```

2. **Check service status:**
   ```bash
   sudo systemctl status odoo18
   sudo journalctl -u odoo18 -n 100
   ```

3. **Check Odoo log:**
   ```bash
   sudo tail -100 /var/log/odoo18/odoo.log
   ```

4. **Re-run script:**
   ```bash
   # Script is idempotent - safe to re-run
   sudo bash /opt/justo-wrks/setup_odoo18_ubuntu.sh
   ```

---

## ✅ Ready to Install!

**The script is:**
- ✅ Robust - Error handling at every step
- ✅ Thorough - 9 phases, 7 automated tests
- ✅ Correct - ARM64 optimized, all dependencies
- ✅ Complete - Full setup from zero to running
- ✅ Automated - No manual intervention needed
- ✅ Safe - Idempotent, can be re-run
- ✅ Secure - Auto-generated passwords, hardened config

**Just run:**
```bash
cd /opt/justo-wrks
git pull origin claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx
sudo bash setup_odoo18_ubuntu.sh
```

**Then access Odoo at:** `http://YOUR_SERVER_IP:8069`

---

**Good luck with your installation! 🚀**
