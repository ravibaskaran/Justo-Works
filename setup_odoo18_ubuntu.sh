#!/bin/bash
# Odoo 18 Setup Script for OCI Ampere Ubuntu ARM64
# This script automates the initial setup of Odoo 18 on Ubuntu
#
# Usage: sudo bash setup_odoo18_ubuntu.sh
#
# IMPORTANT: Review and customize the variables below before running!

set -e  # Exit on error

# ============================================================================
# CONFIGURATION VARIABLES - CUSTOMIZE THESE BEFORE RUNNING
# ============================================================================

ODOO_VERSION="18.0"
ODOO_USER="odoo18"
ODOO_HOME="/opt/odoo18"
ODOO_CONFIG="/etc/odoo18/odoo18.conf"
ODOO_LOG_DIR="/var/log/odoo18"
ODOO_PORT="8069"

# PostgreSQL Configuration
DB_USER="odoo18"
DB_PASSWORD="YOUR_SECURE_DB_PASSWORD_HERE"  # CHANGE THIS!

# Odoo Admin Password
ADMIN_PASSWORD="YOUR_SECURE_ADMIN_PASSWORD_HERE"  # CHANGE THIS!

# Custom addons path (adjust if your repo is elsewhere)
CUSTOM_ADDONS_PATH="/opt/justo-wrks"

# ============================================================================
# PREFLIGHT CHECKS
# ============================================================================

echo "============================================================"
echo "Odoo 18 Ubuntu ARM64 Setup Script"
echo "============================================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: This script must be run as root (use sudo)"
    exit 1
fi

# Check Ubuntu version
if ! grep -q "Ubuntu" /etc/os-release; then
    echo "WARNING: This script is designed for Ubuntu. Continue? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if passwords were changed
if [[ "$DB_PASSWORD" == "YOUR_SECURE_DB_PASSWORD_HERE" ]] || [[ "$ADMIN_PASSWORD" == "YOUR_SECURE_ADMIN_PASSWORD_HERE" ]]; then
    echo "ERROR: Please edit this script and set secure passwords!"
    echo "Update DB_PASSWORD and ADMIN_PASSWORD variables at the top of the script."
    exit 1
fi

# Check ARM64 architecture
ARCH=$(uname -m)
if [[ "$ARCH" != "aarch64" ]]; then
    echo "WARNING: This script is optimized for ARM64 (aarch64). Current architecture: $ARCH"
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "System Information:"
echo "  OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"')"
echo "  Architecture: $ARCH"
echo "  Odoo Version: $ODOO_VERSION"
echo "  Odoo User: $ODOO_USER"
echo "  Odoo Home: $ODOO_HOME"
echo ""
echo "Ready to begin installation. Continue? (y/n)"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

# ============================================================================
# PHASE 1: SYSTEM UPDATE AND DEPENDENCIES
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 1: Updating system and installing dependencies"
echo "============================================================"

apt update
apt upgrade -y

echo "Installing system dependencies..."
apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    wget \
    git \
    libxml2-dev \
    libxslt1-dev \
    libevent-dev \
    libsasl2-dev \
    libldap2-dev \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    pkg-config \
    node-less \
    npm \
    fontconfig \
    libssl-dev \
    wkhtmltopdf

echo "✓ System dependencies installed"

# ============================================================================
# PHASE 2: POSTGRESQL INSTALLATION AND CONFIGURATION
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 2: Installing and configuring PostgreSQL"
echo "============================================================"

apt install -y postgresql postgresql-contrib

systemctl enable postgresql
systemctl start postgresql

# Create Odoo database user
echo "Creating PostgreSQL user: $DB_USER"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH CREATEDB ENCRYPTED PASSWORD '$DB_PASSWORD';" || echo "User may already exist"

echo "✓ PostgreSQL installed and configured"

# ============================================================================
# PHASE 3: ODOO USER CREATION
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 3: Creating Odoo system user"
echo "============================================================"

# Create Odoo user if it doesn't exist
if id "$ODOO_USER" &>/dev/null; then
    echo "User $ODOO_USER already exists"
else
    useradd -m -d "$ODOO_HOME" -U -r -s /bin/bash "$ODOO_USER"
    echo "✓ User $ODOO_USER created"
fi

# ============================================================================
# PHASE 4: ODOO 18 INSTALLATION
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 4: Installing Odoo 18"
echo "============================================================"

# Clone Odoo if not already cloned
if [ -d "$ODOO_HOME/odoo18" ]; then
    echo "Odoo directory already exists at $ODOO_HOME/odoo18"
    echo "Updating existing installation..."
    cd "$ODOO_HOME/odoo18"
    sudo -u "$ODOO_USER" git pull origin "$ODOO_VERSION"
else
    echo "Cloning Odoo $ODOO_VERSION..."
    sudo -u "$ODOO_USER" git clone --depth 1 --branch "$ODOO_VERSION" https://github.com/odoo/odoo.git "$ODOO_HOME/odoo18"
fi

# Create Python virtual environment
echo "Creating Python virtual environment..."
if [ ! -d "$ODOO_HOME/odoo18-venv" ]; then
    sudo -u "$ODOO_USER" python3 -m venv "$ODOO_HOME/odoo18-venv"
    echo "✓ Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Install Python dependencies
echo "Installing Python dependencies (this may take several minutes)..."
sudo -u "$ODOO_USER" bash -c "source $ODOO_HOME/odoo18-venv/bin/activate && pip install --upgrade pip && pip install wheel && pip install -r $ODOO_HOME/odoo18/requirements.txt"

echo "✓ Odoo 18 installed"

# ============================================================================
# PHASE 5: CUSTOM ADDONS LINKING
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 5: Linking custom addons"
echo "============================================================"

if [ -d "$CUSTOM_ADDONS_PATH/addons_custom" ]; then
    if [ ! -L "$ODOO_HOME/addons_custom" ]; then
        ln -s "$CUSTOM_ADDONS_PATH/addons_custom" "$ODOO_HOME/addons_custom"
        chown -h "$ODOO_USER:$ODOO_USER" "$ODOO_HOME/addons_custom"
        echo "✓ Linked addons_custom"
    else
        echo "addons_custom already linked"
    fi
else
    echo "WARNING: $CUSTOM_ADDONS_PATH/addons_custom not found. Skipping."
fi

if [ -d "$CUSTOM_ADDONS_PATH/demo_addons_custom" ]; then
    if [ ! -L "$ODOO_HOME/demo_addons_custom" ]; then
        ln -s "$CUSTOM_ADDONS_PATH/demo_addons_custom" "$ODOO_HOME/demo_addons_custom"
        chown -h "$ODOO_USER:$ODOO_USER" "$ODOO_HOME/demo_addons_custom"
        echo "✓ Linked demo_addons_custom"
    else
        echo "demo_addons_custom already linked"
    fi
else
    echo "WARNING: $CUSTOM_ADDONS_PATH/demo_addons_custom not found. Skipping."
fi

# ============================================================================
# PHASE 6: CONFIGURATION
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 6: Creating Odoo configuration"
echo "============================================================"

# Create config directory
mkdir -p /etc/odoo18
mkdir -p "$ODOO_LOG_DIR"
mkdir -p "$ODOO_HOME/.local/share/Odoo"

chown "$ODOO_USER:$ODOO_USER" "$ODOO_LOG_DIR"
chown -R "$ODOO_USER:$ODOO_USER" "$ODOO_HOME/.local"

# Create configuration file
cat > "$ODOO_CONFIG" <<EOF
[options]
# ===== PATHS =====
addons_path = $ODOO_HOME/odoo18/addons,$ODOO_HOME/addons_custom,$ODOO_HOME/demo_addons_custom
data_dir = $ODOO_HOME/.local/share/Odoo

# ===== SECURITY =====
admin_passwd = $ADMIN_PASSWORD
proxy_mode = True
list_db = False

# ===== DATABASE =====
db_host = localhost
db_port = 5432
db_user = $DB_USER
db_password = $DB_PASSWORD

# ===== SERVER =====
http_port = $ODOO_PORT

# ===== LOGGING =====
logfile = $ODOO_LOG_DIR/odoo.log
log_level = info

# ===== PERFORMANCE =====
workers = 4
max_cron_threads = 2
limit_time_cpu = 600
limit_time_real = 1200
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
EOF

chown "$ODOO_USER:$ODOO_USER" "$ODOO_CONFIG"
chmod 640 "$ODOO_CONFIG"

echo "✓ Configuration file created at $ODOO_CONFIG"

# ============================================================================
# PHASE 7: SYSTEMD SERVICE
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 7: Creating systemd service"
echo "============================================================"

cat > /etc/systemd/system/odoo18.service <<EOF
[Unit]
Description=Odoo 18 ERP
Requires=postgresql.service
After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo18
PermissionsStartOnly=true
User=$ODOO_USER
Group=$ODOO_USER
ExecStart=$ODOO_HOME/odoo18-venv/bin/python3 $ODOO_HOME/odoo18/odoo-bin -c $ODOO_CONFIG
StandardOutput=journal+console
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable odoo18

echo "✓ Systemd service created and enabled"

# ============================================================================
# PHASE 8: FIREWALL CONFIGURATION
# ============================================================================

echo ""
echo "============================================================"
echo "Phase 8: Configuring firewall"
echo "============================================================"

if command -v ufw &> /dev/null; then
    ufw allow "$ODOO_PORT"/tcp
    ufw allow OpenSSH
    echo "✓ Firewall rules added (port $ODOO_PORT opened)"
else
    echo "UFW not installed. Skipping firewall configuration."
fi

# ============================================================================
# INSTALLATION COMPLETE
# ============================================================================

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Odoo 18 has been successfully installed."
echo ""
echo "Next steps:"
echo "  1. Start Odoo service:"
echo "     sudo systemctl start odoo18"
echo ""
echo "  2. Check service status:"
echo "     sudo systemctl status odoo18"
echo ""
echo "  3. View logs:"
echo "     sudo tail -f $ODOO_LOG_DIR/odoo.log"
echo "     sudo journalctl -u odoo18 -f"
echo ""
echo "  4. Access Odoo in your browser:"
echo "     http://$(hostname -I | awk '{print $1}'):$ODOO_PORT"
echo ""
echo "  5. IMPORTANT SECURITY NOTES:"
echo "     - Admin password: Set in $ODOO_CONFIG"
echo "     - Database password: Set in $ODOO_CONFIG"
echo "     - Protect these files: chmod 640 $ODOO_CONFIG"
echo "     - Consider setting up Nginx with SSL for production"
echo ""
echo "For detailed documentation, see:"
echo "  - ODOO_18_UBUNTU_ARM64_SETUP.md"
echo "  - DEVELOPMENT_ROADMAP.md"
echo ""
echo "============================================================"

# Optionally start the service
echo ""
echo "Would you like to start Odoo 18 now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    systemctl start odoo18
    sleep 3
    systemctl status odoo18
    echo ""
    echo "Odoo 18 is starting..."
    echo "Check logs: sudo tail -f $ODOO_LOG_DIR/odoo.log"
fi

echo ""
echo "Installation script completed successfully!"
