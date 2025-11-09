#!/bin/bash
################################################################################
# Odoo 18 Automated Setup Script for OCI Ampere Ubuntu ARM64
#
# This script performs a complete, unattended installation of Odoo 18
# with automatic password generation and comprehensive verification tests.
#
# Usage: sudo bash setup_odoo18_ubuntu.sh
#
# Features:
# - Auto-generates secure passwords
# - ARM64 optimized
# - Full dependency installation
# - Automated testing and verification
# - No manual intervention required
#
################################################################################

set -euo pipefail  # Exit on error, undefined vars, pipe failures
trap 'error_handler $? $LINENO' ERR

# ============================================================================
# ERROR HANDLER
# ============================================================================

error_handler() {
    echo ""
    echo "❌ ERROR: Script failed at line $2 with exit code $1"
    echo "   Check logs above for details"
    exit "$1"
}

# ============================================================================
# CONFIGURATION VARIABLES
# ============================================================================

readonly ODOO_VERSION="18.0"
readonly ODOO_USER="odoo18"
readonly ODOO_HOME="/opt/odoo18"
readonly ODOO_CONFIG="/etc/odoo18/odoo18.conf"
readonly ODOO_LOG_DIR="/var/log/odoo18"
readonly ODOO_PORT="8069"
readonly ODOO_LONGPOLLING_PORT="8072"
readonly CUSTOM_ADDONS_PATH="/opt/justo-wrks"
readonly INSTALL_LOG="/var/log/odoo18_install.log"

# Auto-generate secure passwords (32 characters, alphanumeric)
DB_PASSWORD=$(openssl rand -base64 24 | tr -d "=+/" | cut -c1-32)
ADMIN_PASSWORD=$(openssl rand -base64 24 | tr -d "=+/" | cut -c1-32)
readonly DB_USER="odoo18"

# ============================================================================
# LOGGING FUNCTIONS
# ============================================================================

log_info() {
    echo "ℹ️  $1" | tee -a "$INSTALL_LOG"
}

log_success() {
    echo "✅ $1" | tee -a "$INSTALL_LOG"
}

log_warning() {
    echo "⚠️  $1" | tee -a "$INSTALL_LOG"
}

log_error() {
    echo "❌ $1" | tee -a "$INSTALL_LOG"
}

# ============================================================================
# PREFLIGHT CHECKS
# ============================================================================

preflight_checks() {
    echo "============================================================"
    echo "🚀 Odoo 18 Ubuntu ARM64 Automated Setup"
    echo "============================================================"
    echo ""

    # Create log directory early
    mkdir -p "$(dirname "$INSTALL_LOG")"

    log_info "Starting preflight checks..."

    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root (use sudo)"
        exit 1
    fi

    # Check Ubuntu
    if ! grep -q "Ubuntu" /etc/os-release; then
        log_warning "Not running Ubuntu. Proceeding with caution..."
    fi

    # Check ARM64 architecture
    ARCH=$(uname -m)
    if [[ "$ARCH" != "aarch64" ]]; then
        log_warning "Not ARM64 architecture (found: $ARCH). Some optimizations may not apply."
    else
        log_success "ARM64 architecture detected"
    fi

    # Check internet connectivity
    if ! ping -c 1 8.8.8.8 &>/dev/null; then
        log_error "No internet connectivity. Cannot proceed."
        exit 1
    fi
    log_success "Internet connectivity verified"

    # Display system information
    echo ""
    log_info "System Information:"
    echo "  OS: $(grep PRETTY_NAME /etc/os-release | cut -d'=' -f2 | tr -d '\"')"
    echo "  Kernel: $(uname -r)"
    echo "  Architecture: $ARCH"
    echo "  CPUs: $(nproc)"
    echo "  Memory: $(free -h | awk '/^Mem:/ {print $2}')"
    echo "  Disk: $(df -h / | awk 'NR==2 {print $4}') available"
    echo ""

    # Check minimum requirements
    local mem_gb=$(free -g | awk '/^Mem:/ {print $2}')
    if [ "$mem_gb" -lt 3 ]; then
        log_warning "Less than 4GB RAM detected. Odoo may run slowly."
    fi

    local disk_gb=$(df -BG / | awk 'NR==2 {print $4}' | tr -d 'G')
    if [ "$disk_gb" -lt 20 ]; then
        log_warning "Less than 20GB disk space available. May not be sufficient."
    fi

    log_success "Preflight checks completed"
}

# ============================================================================
# PHASE 1: SYSTEM UPDATE AND DEPENDENCIES
# ============================================================================

install_system_dependencies() {
    echo ""
    echo "============================================================"
    echo "📦 Phase 1: Installing System Dependencies"
    echo "============================================================"
    echo ""

    log_info "Updating package lists..."
    apt-get update -qq

    log_info "Upgrading existing packages (this may take a while)..."
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -qq

    log_info "Installing core dependencies..."
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        python3-pip \
        python3-dev \
        python3-venv \
        python3-wheel \
        build-essential \
        wget \
        git \
        curl \
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
        fontconfig \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libffi-dev \
        liblzma-dev

    log_info "Installing Node.js and npm..."
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        nodejs \
        npm \
        node-less

    log_info "Installing wkhtmltopdf for PDF reports..."
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq wkhtmltopdf

    # Install ARM64 optimization libraries
    log_info "Installing ARM64 optimization libraries..."
    if apt-cache show libjemalloc2 &>/dev/null; then
        DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libjemalloc2
        log_success "Jemalloc installed for better memory management"
    fi

    log_success "System dependencies installed"
}

# ============================================================================
# PHASE 2: POSTGRESQL INSTALLATION AND CONFIGURATION
# ============================================================================

setup_postgresql() {
    echo ""
    echo "============================================================"
    echo "🗄️  Phase 2: PostgreSQL Setup"
    echo "============================================================"
    echo ""

    log_info "Installing PostgreSQL..."
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        postgresql \
        postgresql-contrib \
        postgresql-client

    # Start PostgreSQL
    systemctl enable postgresql --quiet
    systemctl start postgresql

    # Wait for PostgreSQL to be ready
    log_info "Waiting for PostgreSQL to be ready..."
    for i in {1..30}; do
        if sudo -u postgres psql -c "SELECT 1" &>/dev/null; then
            break
        fi
        sleep 1
    done

    # Create Odoo database user
    log_info "Creating PostgreSQL user: $DB_USER"
    sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;" &>/dev/null || true
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH CREATEDB ENCRYPTED PASSWORD '$DB_PASSWORD';"

    # Verify user creation
    if sudo -u postgres psql -c "\du" | grep -q "$DB_USER"; then
        log_success "PostgreSQL user created successfully"
    else
        log_error "Failed to create PostgreSQL user"
        exit 1
    fi

    # Optimize PostgreSQL for Odoo (basic tuning)
    log_info "Optimizing PostgreSQL configuration..."
    local pg_conf=$(sudo -u postgres psql -t -c "SHOW config_file;" | xargs)

    # Backup original config
    cp "$pg_conf" "${pg_conf}.backup"

    # Apply basic optimizations
    sudo -u postgres psql -c "ALTER SYSTEM SET shared_buffers = '256MB';"
    sudo -u postgres psql -c "ALTER SYSTEM SET effective_cache_size = '1GB';"
    sudo -u postgres psql -c "ALTER SYSTEM SET maintenance_work_mem = '128MB';"
    sudo -u postgres psql -c "ALTER SYSTEM SET checkpoint_completion_target = 0.9;"
    sudo -u postgres psql -c "ALTER SYSTEM SET wal_buffers = '16MB';"
    sudo -u postgres psql -c "ALTER SYSTEM SET default_statistics_target = 100;"

    systemctl restart postgresql

    log_success "PostgreSQL configured and optimized"
}

# ============================================================================
# PHASE 3: ODOO USER CREATION
# ============================================================================

create_odoo_user() {
    echo ""
    echo "============================================================"
    echo "👤 Phase 3: Creating Odoo System User"
    echo "============================================================"
    echo ""

    if id "$ODOO_USER" &>/dev/null; then
        log_warning "User $ODOO_USER already exists"
    else
        useradd -m -d "$ODOO_HOME" -U -r -s /bin/bash "$ODOO_USER"
        log_success "User $ODOO_USER created"
    fi

    # Ensure home directory exists with correct permissions
    mkdir -p "$ODOO_HOME"
    chown -R "$ODOO_USER:$ODOO_USER" "$ODOO_HOME"
}

# ============================================================================
# PHASE 4: ODOO 18 INSTALLATION
# ============================================================================

install_odoo18() {
    echo ""
    echo "============================================================"
    echo "🔧 Phase 4: Installing Odoo 18"
    echo "============================================================"
    echo ""

    # Clone Odoo 18
    if [ -d "$ODOO_HOME/odoo18/.git" ]; then
        log_info "Odoo 18 already cloned. Updating..."
        cd "$ODOO_HOME/odoo18"
        sudo -u "$ODOO_USER" git fetch --depth 1 origin "$ODOO_VERSION"
        sudo -u "$ODOO_USER" git reset --hard "origin/$ODOO_VERSION"
    else
        log_info "Cloning Odoo $ODOO_VERSION (this may take a few minutes)..."
        rm -rf "$ODOO_HOME/odoo18"
        sudo -u "$ODOO_USER" git clone --depth 1 --branch "$ODOO_VERSION" \
            https://github.com/odoo/odoo.git "$ODOO_HOME/odoo18"
    fi

    log_success "Odoo 18 source code downloaded"

    # Create Python virtual environment
    log_info "Creating Python virtual environment..."
    if [ -d "$ODOO_HOME/odoo18-venv" ]; then
        log_info "Virtual environment exists. Recreating for clean state..."
        rm -rf "$ODOO_HOME/odoo18-venv"
    fi

    sudo -u "$ODOO_USER" python3 -m venv "$ODOO_HOME/odoo18-venv"
    log_success "Virtual environment created"

    # Install Python dependencies
    log_info "Installing Python dependencies (this will take several minutes)..."
    log_info "Progress: Upgrading pip and installing wheel..."
    sudo -u "$ODOO_USER" bash -c "
        source $ODOO_HOME/odoo18-venv/bin/activate
        pip install --quiet --upgrade pip setuptools wheel
    "

    log_info "Progress: Installing Odoo requirements..."
    sudo -u "$ODOO_USER" bash -c "
        source $ODOO_HOME/odoo18-venv/bin/activate
        pip install --quiet -r $ODOO_HOME/odoo18/requirements.txt
    "

    # Install additional useful packages
    log_info "Installing additional Python packages..."
    sudo -u "$ODOO_USER" bash -c "
        source $ODOO_HOME/odoo18-venv/bin/activate
        pip install --quiet phonenumbers pycountry
    "

    log_success "All Python dependencies installed"

    # Verify Odoo installation
    log_info "Verifying Odoo installation..."
    if [ -f "$ODOO_HOME/odoo18/odoo-bin" ]; then
        log_success "Odoo binary found"
    else
        log_error "Odoo binary not found!"
        exit 1
    fi
}

# ============================================================================
# PHASE 5: CUSTOM ADDONS LINKING
# ============================================================================

link_custom_addons() {
    echo ""
    echo "============================================================"
    echo "🔗 Phase 5: Linking Custom Addons"
    echo "============================================================"
    echo ""

    local linked_count=0

    # Link addons_custom
    if [ -d "$CUSTOM_ADDONS_PATH/addons_custom" ]; then
        if [ -L "$ODOO_HOME/addons_custom" ]; then
            rm -f "$ODOO_HOME/addons_custom"
        fi
        ln -s "$CUSTOM_ADDONS_PATH/addons_custom" "$ODOO_HOME/addons_custom"
        chown -h "$ODOO_USER:$ODOO_USER" "$ODOO_HOME/addons_custom"
        log_success "Linked addons_custom ($(find "$CUSTOM_ADDONS_PATH/addons_custom" -maxdepth 1 -type d | wc -l) modules)"
        linked_count=$((linked_count + 1))
    else
        log_warning "$CUSTOM_ADDONS_PATH/addons_custom not found"
    fi

    # Link demo_addons_custom
    if [ -d "$CUSTOM_ADDONS_PATH/demo_addons_custom" ]; then
        if [ -L "$ODOO_HOME/demo_addons_custom" ]; then
            rm -f "$ODOO_HOME/demo_addons_custom"
        fi
        ln -s "$CUSTOM_ADDONS_PATH/demo_addons_custom" "$ODOO_HOME/demo_addons_custom"
        chown -h "$ODOO_USER:$ODOO_USER" "$ODOO_HOME/demo_addons_custom"
        log_success "Linked demo_addons_custom ($(find "$CUSTOM_ADDONS_PATH/demo_addons_custom" -maxdepth 1 -type d | wc -l) modules)"
        linked_count=$((linked_count + 1))
    else
        log_warning "$CUSTOM_ADDONS_PATH/demo_addons_custom not found"
    fi

    if [ $linked_count -eq 0 ]; then
        log_warning "No custom addons linked. Only standard Odoo addons will be available."
    else
        log_success "Custom addons linked successfully"
    fi
}

# ============================================================================
# PHASE 6: CONFIGURATION
# ============================================================================

create_configuration() {
    echo ""
    echo "============================================================"
    echo "⚙️  Phase 6: Creating Configuration"
    echo "============================================================"
    echo ""

    # Create directories
    mkdir -p "$(dirname "$ODOO_CONFIG")"
    mkdir -p "$ODOO_LOG_DIR"
    mkdir -p "$ODOO_HOME/.local/share/Odoo"

    chown -R "$ODOO_USER:$ODOO_USER" "$ODOO_LOG_DIR"
    chown -R "$ODOO_USER:$ODOO_USER" "$ODOO_HOME/.local"

    # Build addons_path
    local addons_path="$ODOO_HOME/odoo18/addons"
    [ -L "$ODOO_HOME/addons_custom" ] && addons_path="$addons_path,$ODOO_HOME/addons_custom"
    [ -L "$ODOO_HOME/demo_addons_custom" ] && addons_path="$addons_path,$ODOO_HOME/demo_addons_custom"

    # Create configuration file
    log_info "Generating Odoo configuration..."
    cat > "$ODOO_CONFIG" <<EOF
# Odoo 18 Configuration - Auto-generated by setup script
# Generated: $(date)
# Server: $(hostname)

[options]
# ===== PATHS =====
addons_path = $addons_path
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
db_maxconn = 64

# ===== SERVER =====
http_port = $ODOO_PORT
longpolling_port = $ODOO_LONGPOLLING_PORT

# ===== LOGGING =====
logfile = $ODOO_LOG_DIR/odoo.log
log_level = info
log_handler = :INFO
log_db = False
log_db_level = warning

# ===== PERFORMANCE =====
# Adjusted for typical OCI Ampere A1 instance
workers = 4
max_cron_threads = 2
limit_time_cpu = 600
limit_time_real = 1200
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192

# ===== MULTIPROCESSING =====
# Optimized for ARM64
db_template = template0
EOF

    chown "$ODOO_USER:$ODOO_USER" "$ODOO_CONFIG"
    chmod 640 "$ODOO_CONFIG"

    log_success "Configuration file created at $ODOO_CONFIG"

    # Save credentials securely
    local creds_file="$ODOO_HOME/.credentials"
    cat > "$creds_file" <<EOF
# Odoo 18 Credentials - Keep this file secure!
# Generated: $(date)

ODOO_ADMIN_PASSWORD=$ADMIN_PASSWORD
DATABASE_USER=$DB_USER
DATABASE_PASSWORD=$DB_PASSWORD
ODOO_PORT=$ODOO_PORT

# Access Odoo at: http://$(hostname -I | awk '{print $1}'):$ODOO_PORT
EOF

    chown "$ODOO_USER:$ODOO_USER" "$creds_file"
    chmod 600 "$creds_file"

    log_success "Credentials saved to $creds_file"
}

# ============================================================================
# PHASE 7: SYSTEMD SERVICE
# ============================================================================

create_systemd_service() {
    echo ""
    echo "============================================================"
    echo "🔄 Phase 7: Creating Systemd Service"
    echo "============================================================"
    echo ""

    log_info "Creating systemd service file..."

    # Detect if jemalloc is available for ARM64 optimization
    local jemalloc_path=""
    if [ -f "/usr/lib/aarch64-linux-gnu/libjemalloc.so.2" ]; then
        jemalloc_path="/usr/lib/aarch64-linux-gnu/libjemalloc.so.2"
        log_info "Jemalloc detected - will be used for memory optimization"
    fi

    cat > /etc/systemd/system/odoo18.service <<EOF
[Unit]
Description=Odoo 18 ERP System
Documentation=https://www.odoo.com/documentation/18.0/
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
StandardError=journal
Restart=on-failure
RestartSec=10
KillMode=mixed
TimeoutStopSec=60
$([ -n "$jemalloc_path" ] && echo "Environment=\"LD_PRELOAD=$jemalloc_path\"")

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$ODOO_HOME $ODOO_LOG_DIR /run

# Resource limits
LimitNOFILE=65535
LimitNPROC=8192

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable odoo18 --quiet

    log_success "Systemd service created and enabled"
}

# ============================================================================
# PHASE 8: START SERVICE
# ============================================================================

start_odoo_service() {
    echo ""
    echo "============================================================"
    echo "🚀 Phase 8: Starting Odoo Service"
    echo "============================================================"
    echo ""

    log_info "Starting Odoo 18 service..."
    systemctl start odoo18

    # Wait for service to start
    log_info "Waiting for Odoo to start (up to 60 seconds)..."
    for i in {1..60}; do
        if systemctl is-active --quiet odoo18; then
            log_success "Odoo service is active"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""

    # Check service status
    if systemctl is-active --quiet odoo18; then
        log_success "Odoo 18 service started successfully"
    else
        log_error "Odoo service failed to start"
        log_error "Check logs: journalctl -u odoo18 -n 50"
        exit 1
    fi
}

# ============================================================================
# PHASE 9: AUTOMATED VERIFICATION TESTS
# ============================================================================

run_verification_tests() {
    echo ""
    echo "============================================================"
    echo "🧪 Phase 9: Automated Verification Tests"
    echo "============================================================"
    echo ""

    local tests_passed=0
    local tests_failed=0

    # Test 1: Service Status
    echo "Test 1/7: Checking service status..."
    if systemctl is-active --quiet odoo18; then
        log_success "✓ Service is running"
        tests_passed=$((tests_passed + 1))
    else
        log_error "✗ Service is not running"
        tests_failed=$((tests_failed + 1))
    fi

    # Test 2: Port Listening
    echo "Test 2/7: Checking if port $ODOO_PORT is listening..."
    sleep 5  # Give Odoo time to bind to port
    if netstat -tuln 2>/dev/null | grep -q ":$ODOO_PORT " || ss -tuln 2>/dev/null | grep -q ":$ODOO_PORT "; then
        log_success "✓ Port $ODOO_PORT is listening"
        tests_passed=$((tests_passed + 1))
    else
        log_error "✗ Port $ODOO_PORT is not listening"
        tests_failed=$((tests_failed + 1))
    fi

    # Test 3: HTTP Response
    echo "Test 3/7: Testing HTTP endpoint..."
    local max_attempts=30
    local attempt=0
    local http_success=false

    while [ $attempt -lt $max_attempts ]; do
        if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$ODOO_PORT/web/database/selector" | grep -q "200\|303"; then
            http_success=true
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
    done

    if [ "$http_success" = true ]; then
        log_success "✓ HTTP endpoint responding"
        tests_passed=$((tests_passed + 1))
    else
        log_error "✗ HTTP endpoint not responding after ${max_attempts} attempts"
        tests_failed=$((tests_failed + 1))
    fi

    # Test 4: Log File Check
    echo "Test 4/7: Checking log files..."
    if [ -f "$ODOO_LOG_DIR/odoo.log" ]; then
        log_success "✓ Log file exists"
        tests_passed=$((tests_passed + 1))

        # Check for critical errors in logs
        if grep -qi "critical\|traceback" "$ODOO_LOG_DIR/odoo.log" | head -5; then
            log_warning "⚠ Critical errors found in logs (may be normal during startup)"
        fi
    else
        log_error "✗ Log file not found"
        tests_failed=$((tests_failed + 1))
    fi

    # Test 5: Database Connection
    echo "Test 5/7: Testing database connection..."
    if sudo -u "$ODOO_USER" PGPASSWORD="$DB_PASSWORD" psql -h localhost -U "$DB_USER" -d postgres -c "SELECT 1" &>/dev/null; then
        log_success "✓ Database connection successful"
        tests_passed=$((tests_passed + 1))
    else
        log_error "✗ Database connection failed"
        tests_failed=$((tests_failed + 1))
    fi

    # Test 6: Python Environment
    echo "Test 6/7: Verifying Python environment..."
    if sudo -u "$ODOO_USER" bash -c "source $ODOO_HOME/odoo18-venv/bin/activate && python -c 'import odoo; print(odoo.release.version)'" &>/dev/null; then
        local odoo_ver=$(sudo -u "$ODOO_USER" bash -c "source $ODOO_HOME/odoo18-venv/bin/activate && python -c 'import odoo; print(odoo.release.version)'")
        log_success "✓ Python environment OK (Odoo version: $odoo_ver)"
        tests_passed=$((tests_passed + 1))
    else
        log_error "✗ Python environment check failed"
        tests_failed=$((tests_failed + 1))
    fi

    # Test 7: Create Test Database
    echo "Test 7/7: Creating and validating test database..."
    local test_db="test_install_$(date +%s)"

    if sudo -u "$ODOO_USER" bash -c "source $ODOO_HOME/odoo18-venv/bin/activate && \
        $ODOO_HOME/odoo18/odoo-bin -c $ODOO_CONFIG -d $test_db --init base --stop-after-init --log-level=error" &>/dev/null; then
        log_success "✓ Test database created successfully"
        tests_passed=$((tests_passed + 1))

        # Cleanup test database
        sudo -u postgres psql -c "DROP DATABASE IF EXISTS $test_db;" &>/dev/null
    else
        log_error "✗ Failed to create test database"
        tests_failed=$((tests_failed + 1))
    fi

    # Test Summary
    echo ""
    echo "============================================================"
    echo "📊 Test Results Summary"
    echo "============================================================"
    echo "Total Tests: 7"
    echo "Passed: $tests_passed"
    echo "Failed: $tests_failed"
    echo ""

    if [ $tests_failed -eq 0 ]; then
        log_success "🎉 All verification tests passed!"
        return 0
    else
        log_warning "⚠️  Some tests failed. Review the output above."
        return 1
    fi
}

# ============================================================================
# INSTALLATION SUMMARY
# ============================================================================

display_summary() {
    local server_ip=$(hostname -I | awk '{print $1}')

    echo ""
    echo "============================================================"
    echo "✅ INSTALLATION COMPLETE!"
    echo "============================================================"
    echo ""
    echo "📋 Installation Summary:"
    echo "  • Odoo Version: 18.0"
    echo "  • Installation Path: $ODOO_HOME"
    echo "  • Configuration: $ODOO_CONFIG"
    echo "  • Log Files: $ODOO_LOG_DIR/odoo.log"
    echo "  • Service: odoo18.service"
    echo ""
    echo "🔐 Security Information:"
    echo "  • Credentials saved in: $ODOO_HOME/.credentials"
    echo "  • View credentials: sudo cat $ODOO_HOME/.credentials"
    echo "  • Admin Password: $ADMIN_PASSWORD"
    echo "  • Database Password: [saved in credentials file]"
    echo ""
    echo "🌐 Access Information:"
    echo "  • URL: http://$server_ip:$ODOO_PORT"
    echo "  • HTTP Port: $ODOO_PORT"
    echo "  • Longpolling Port: $ODOO_LONGPOLLING_PORT"
    echo ""
    echo "⚠️  FIREWALL CONFIGURATION REQUIRED:"
    echo "  Configure OCI Security List to allow:"
    echo "  • Port $ODOO_PORT/TCP (Odoo HTTP)"
    echo "  • Port $ODOO_LONGPOLLING_PORT/TCP (Odoo Longpolling - optional)"
    echo "  • Port 22/TCP (SSH - already configured)"
    echo ""
    echo "🔧 Useful Commands:"
    echo "  • Check status:  sudo systemctl status odoo18"
    echo "  • View logs:     sudo journalctl -u odoo18 -f"
    echo "  • Restart:       sudo systemctl restart odoo18"
    echo "  • Stop:          sudo systemctl stop odoo18"
    echo "  • Start:         sudo systemctl start odoo18"
    echo ""
    echo "📚 Documentation:"
    echo "  • Setup Guide: $CUSTOM_ADDONS_PATH/ODOO_18_UBUNTU_ARM64_SETUP.md"
    echo "  • Roadmap: $CUSTOM_ADDONS_PATH/DEVELOPMENT_ROADMAP.md"
    echo "  • Installation Log: $INSTALL_LOG"
    echo ""
    echo "🎯 Next Steps:"
    echo "  1. Configure OCI Security List for port $ODOO_PORT"
    echo "  2. Access Odoo at http://$server_ip:$ODOO_PORT"
    echo "  3. Create your first database"
    echo "  4. Install and configure your custom modules"
    echo "  5. Consider setting up Nginx with SSL for production"
    echo ""
    echo "============================================================"
    echo "🎉 Odoo 18 is ready to use!"
    echo "============================================================"
    echo ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    local start_time=$(date +%s)

    preflight_checks
    install_system_dependencies
    setup_postgresql
    create_odoo_user
    install_odoo18
    link_custom_addons
    create_configuration
    create_systemd_service
    start_odoo_service
    run_verification_tests

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))

    echo ""
    log_success "Installation completed in ${minutes}m ${seconds}s"

    display_summary
}

# Run main function
main "$@"
