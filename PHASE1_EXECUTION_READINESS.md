# Phase 1 Execution Readiness Checklist
**Phase:** Odoo 18 Environment Setup
**Platform:** OCI Ampere Ubuntu ARM64
**Script:** setup_odoo18_ubuntu.sh
**Status:** Ready to execute

---

## 📋 Pre-Flight Checklist

Before running the Odoo 18 setup script, verify all prerequisites are met.

### System Requirements

- [ ] **Server Access**
  - SSH access to OCI Ampere Ubuntu server
  - Root or sudo privileges
  - Stable internet connection

- [ ] **System Specifications**
  - Platform: Ubuntu 22.04 or 24.04 ARM64
  - RAM: Minimum 4GB (8GB recommended)
  - Disk Space: Minimum 20GB free
  - CPU: ARM64 architecture

- [ ] **Network Requirements**
  - Internet access for package downloads
  - Ports available: 8069 (Odoo), 5432 (PostgreSQL)
  - Firewall configured to allow HTTP/HTTPS

### Repository Status

- [ ] **Git Repository**
  - Repository cloned at `/opt/justo-wrks` or `/home/user/Justo-Works`
  - Branch: `claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx`
  - All documentation files present
  - setup_odoo18_ubuntu.sh script exists

- [ ] **Backup Current System**
  - Odoo 15 database backed up (if applicable)
  - Custom module code committed to git
  - Configuration files backed up

---

## 🚀 Execution Steps

### Step 1: Verify Prerequisites (5 minutes)

```bash
# Check Ubuntu version
lsb_release -a
# Should show: Ubuntu 22.04 or 24.04

# Check architecture
uname -m
# Should show: aarch64 (ARM64)

# Check available disk space
df -h /opt
# Should have at least 20GB free

# Check available memory
free -h
# Should have at least 4GB

# Check if on correct branch
cd /home/user/Justo-Works
git branch
# Should show: * claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx

# Verify setup script exists
ls -lh setup_odoo18_ubuntu.sh
# Should exist and be ~25-30KB
```

### Step 2: Review Setup Script (10 minutes)

```bash
# Read the setup script to understand what it will do
less setup_odoo18_ubuntu.sh

# Check script permissions
ls -la setup_odoo18_ubuntu.sh
# If not executable, make it executable:
chmod +x setup_odoo18_ubuntu.sh
```

**What the script will do:**
1. Update system packages
2. Install Python 3.10+ and dependencies
3. Install PostgreSQL 15+
4. Create `odoo18` system user
5. Install wkhtmltopdf (ARM64)
6. Clone Odoo 18 repository
7. Create Python virtual environment
8. Install Python dependencies
9. Configure odoo.conf
10. Create systemd service
11. Run 7 verification tests

**Expected runtime:** 10-15 minutes

### Step 3: Execute Setup Script (15 minutes)

```bash
# Navigate to repository
cd /home/user/Justo-Works

# Pull latest changes (if not already done)
git pull origin claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx

# Run setup script with sudo
sudo bash setup_odoo18_ubuntu.sh

# Monitor output
# Script will show progress and run verification tests
```

**During execution, watch for:**
- ✅ Green checkmarks for successful steps
- ⚠️ Yellow warnings (usually safe to ignore)
- ❌ Red errors (script should stop and show details)

### Step 4: Verify Installation (10 minutes)

**After script completes, verify:**

```bash
# 1. Check Odoo 18 service status
sudo systemctl status odoo18
# Should show: active (running)

# 2. Check PostgreSQL status
sudo systemctl status postgresql
# Should show: active (running)

# 3. Check Odoo 18 logs
sudo tail -50 /var/log/odoo18/odoo.log
# Should show: Odoo started successfully

# 4. Check if web interface is accessible
curl http://localhost:8069
# Should return HTML (not error)

# 5. Verify odoo18 user exists
id odoo18
# Should show: uid=... gid=... groups=...

# 6. Check Python virtual environment
ls -la /opt/odoo18/odoo18-venv/
# Should exist with bin/, lib/, etc.

# 7. Check Odoo 18 directory
ls -la /opt/odoo18/odoo18/
# Should show Odoo source files
```

### Step 5: Access Web Interface (5 minutes)

```bash
# If running locally, open browser to:
http://localhost:8069

# If running on remote server, use SSH tunnel:
ssh -L 8069:localhost:8069 user@your-server-ip

# Then open browser to:
http://localhost:8069
```

**Expected:**
- Odoo 18 database selection page
- Clean interface, no errors
- "Create Database" option available

### Step 6: Create Test Database (10 minutes)

**In web interface:**

1. Click "Create Database"
2. Fill in details:
   - Database Name: `test_odoo18`
   - Email: `admin@example.com`
   - Password: `admin` (change in production)
   - Language: English (or your language)
   - Country: Your country
   - Demo data: ✅ Check (for testing)

3. Click "Create Database"
4. Wait 2-5 minutes
5. Should redirect to Odoo 18 main interface

**Verify test database:**
- [ ] Database created successfully
- [ ] Can log in with admin credentials
- [ ] Apps menu shows Odoo 18 apps
- [ ] Settings accessible
- [ ] No error messages

---

## 🔍 Verification Tests

The setup script runs 7 automated tests. Verify all passed:

### Test 1: Python Version
```bash
python3 --version
# Should be: Python 3.10.x or higher
```
**Status:** [ ] PASS / [ ] FAIL

### Test 2: PostgreSQL Installation
```bash
sudo -u postgres psql --version
# Should be: psql (PostgreSQL) 15.x or higher
```
**Status:** [ ] PASS / [ ] FAIL

### Test 3: odoo18 User Exists
```bash
id odoo18
# Should show: uid, gid, groups
```
**Status:** [ ] PASS / [ ] FAIL

### Test 4: Virtual Environment
```bash
source /opt/odoo18/odoo18-venv/bin/activate
python --version
which python
# Should be in /opt/odoo18/odoo18-venv/bin/python
deactivate
```
**Status:** [ ] PASS / [ ] FAIL

### Test 5: Odoo 18 Source
```bash
ls /opt/odoo18/odoo18/odoo-bin
# Should exist and be executable
```
**Status:** [ ] PASS / [ ] FAIL

### Test 6: Configuration File
```bash
cat /etc/odoo18/odoo18.conf
# Should show proper configuration
```
**Status:** [ ] PASS / [ ] FAIL

### Test 7: Service Running
```bash
sudo systemctl is-active odoo18
# Should show: active
```
**Status:** [ ] PASS / [ ] FAIL

**Overall Status:** [ ] All 7 tests passed ✅

---

## 📊 Post-Installation Configuration

### Configure Custom Addons Path

```bash
# Edit odoo.conf to add custom addons
sudo nano /etc/odoo18/odoo18.conf

# Add or update addons_path:
addons_path = /opt/odoo18/odoo18/addons,/opt/justo-wrks/addons_custom,/opt/justo-wrks/demo_addons_custom

# Save and exit (Ctrl+X, Y, Enter)

# Restart Odoo 18
sudo systemctl restart odoo18

# Verify restart
sudo systemctl status odoo18
```

### Verify Custom Modules Visible

```bash
# In Odoo web interface:
# 1. Go to Apps
# 2. Click "Update Apps List"
# 3. Search for your custom modules

# Or check via command line:
sudo -u odoo18 bash -c "source /opt/odoo18/odoo18-venv/bin/activate && \
    /opt/odoo18/odoo18/odoo-bin -c /etc/odoo18/odoo18.conf \
    --addons-path=/opt/odoo18/odoo18/addons,/opt/justo-wrks/addons_custom \
    --list"
```

### Set File Permissions

```bash
# Ensure odoo18 user can read custom modules
sudo chown -R odoo18:odoo18 /opt/justo-wrks/addons_custom
sudo chown -R odoo18:odoo18 /opt/justo-wrks/demo_addons_custom

# Set proper permissions
sudo chmod -R 755 /opt/justo-wrks/addons_custom
sudo chmod -R 755 /opt/justo-wrks/demo_addons_custom

# Verify permissions
ls -la /opt/justo-wrks/addons_custom
# Should show: drwxr-xr-x odoo18 odoo18
```

---

## 🚨 Troubleshooting

### Issue 1: Script Fails with "Permission Denied"

```bash
# Solution: Run with sudo
sudo bash setup_odoo18_ubuntu.sh
```

### Issue 2: PostgreSQL Installation Fails

```bash
# Check if already installed
sudo -u postgres psql --version

# If old version exists, remove and reinstall
sudo apt remove postgresql postgresql-contrib
sudo apt update
sudo apt install postgresql-15 postgresql-contrib-15
```

### Issue 3: wkhtmltopdf Not Found for ARM64

```bash
# Install from Ubuntu repository (ARM64 compatible)
sudo apt update
sudo apt install wkhtmltopdf

# Verify installation
wkhtmltopdf --version
```

### Issue 4: Python Dependencies Fail to Install

```bash
# Check if virtual environment is activated
source /opt/odoo18/odoo18-venv/bin/activate

# Update pip
pip install --upgrade pip setuptools wheel

# Install dependencies manually
cd /opt/odoo18/odoo18
pip install -r requirements.txt

# Check for specific errors in output
```

### Issue 5: Odoo Service Won't Start

```bash
# Check logs for errors
sudo journalctl -u odoo18 -n 50

# Check Odoo log file
sudo tail -100 /var/log/odoo18/odoo.log

# Common issues:
# - Database connection error → Check PostgreSQL is running
# - Permission error → Check file ownership
# - Port already in use → Check if another process using port 8069
```

### Issue 6: Can't Access Web Interface

```bash
# Check if Odoo is listening on port 8069
sudo netstat -tlnp | grep 8069

# Check firewall
sudo ufw status
sudo ufw allow 8069/tcp

# Check Odoo config
grep "xmlrpc_port\|http_port" /etc/odoo18/odoo18.conf
# Should show: 8069
```

### Issue 7: Custom Modules Not Visible

```bash
# Check addons_path in config
grep "addons_path" /etc/odoo18/odoo18.conf

# Should include:
# /opt/justo-wrks/addons_custom
# /opt/justo-wrks/demo_addons_custom

# If not, add them and restart
sudo systemctl restart odoo18

# Update apps list in web interface
# Apps → Update Apps List
```

---

## ✅ Success Criteria

Phase 1 is complete when ALL of the following are true:

### System Level
- [ ] Ubuntu server accessible via SSH
- [ ] Sufficient disk space (20GB+ free)
- [ ] Sufficient RAM (4GB+ available)
- [ ] All system packages updated

### Odoo 18 Installation
- [ ] Python 3.10+ installed
- [ ] PostgreSQL 15+ installed and running
- [ ] odoo18 system user created
- [ ] wkhtmltopdf installed (ARM64)
- [ ] Odoo 18 source cloned to /opt/odoo18/odoo18
- [ ] Python virtual environment created
- [ ] All Python dependencies installed
- [ ] odoo.conf configured correctly
- [ ] systemd service created and enabled
- [ ] Odoo 18 service running

### Verification
- [ ] All 7 automated tests passed
- [ ] Web interface accessible at port 8069
- [ ] Test database created successfully
- [ ] Can log in to Odoo 18
- [ ] No critical errors in logs

### Custom Modules
- [ ] Custom addons path configured
- [ ] File permissions set correctly
- [ ] Custom modules visible in Apps list
- [ ] Can install a simple custom module (hide_menu_user)

---

## 📅 Timeline

**Total Time:** ~1 hour

| Task | Time | Status |
|------|------|--------|
| Prerequisites check | 5 min | [ ] |
| Review setup script | 10 min | [ ] |
| Execute setup script | 15 min | [ ] |
| Verify installation | 10 min | [ ] |
| Access web interface | 5 min | [ ] |
| Create test database | 10 min | [ ] |
| Configure custom addons | 10 min | [ ] |
| Final verification | 5 min | [ ] |

---

## 📞 Next Steps After Phase 1

Once Phase 1 is complete:

1. **Resolve External Module Dependencies** (Decision 3)
   - Contact Inexoft Technologies
   - Search for missing modules
   - See: EXTERNAL_MODULES_ACQUISITION_GUIDE.md

2. **Begin Charting Library Migration** (Decision 1)
   - Follow: CHARTING_LIBRARY_MIGRATION_GUIDE.md
   - Replace Highcharts with ApexCharts
   - Replace FusionCharts with Chart.js v4

3. **Set Up Google Maps API** (Decision 2)
   - Follow: DECISIONS_EXECUTION_PLAN.md → Decision 2
   - Enable billing
   - Create and secure API key

4. **Begin Phase 2 Module Migration**
   - Follow: PHASE2_MIGRATION_CHECKLIST.md
   - Start with simple modules
   - Progress to complex modules

---

## 📄 Related Documentation

- **Main Setup Guide:** ODOO_18_UBUNTU_ARM64_SETUP.md
- **Setup Script:** setup_odoo18_ubuntu.sh
- **Migration Checklist:** PHASE2_MIGRATION_CHECKLIST.md
- **Session Handoff:** SESSION_HANDOFF.md
- **Decisions Execution:** DECISIONS_EXECUTION_PLAN.md

---

**Status:** Ready to execute
**Risk Level:** LOW (automated script with verification)
**Estimated Time:** 1 hour
**Reversible:** Yes (can uninstall if needed)

**When ready, execute:**
```bash
cd /home/user/Justo-Works
sudo bash setup_odoo18_ubuntu.sh
```

---

**Last Updated:** 2025-11-09
**Phase:** 1 - Odoo 18 Environment Setup
**Next Phase:** 2 - Module Migration (after dependencies resolved)
