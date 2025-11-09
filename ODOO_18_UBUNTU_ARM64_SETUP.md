# Odoo 18 Setup Guide for OCI Ampere Ubuntu ARM64

## Current State Analysis

**Previous Setup (Detected):**
- Platform: Windows (paths like `C:\jworks\odoo15\`)
- Odoo Version: 15.0
- Database: PostgreSQL on port 5434
- HTTP Port: 8075
- Admin password: 123 (needs to be changed for production)

**Target Setup:**
- Platform: OCI Ampere Ubuntu 22.04/24.04 (ARM64)
- Odoo Version: 18.0
- Database: PostgreSQL 15+ (ARM64 compatible)
- HTTP Port: 8069 (default) or 8075 (if maintaining compatibility)
- Terminal-only access (no GUI)

## Prerequisites

### System Requirements
- **OS**: Ubuntu 22.04 LTS or 24.04 LTS (ARM64)
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 40GB
- **Python**: 3.10+ (comes with Ubuntu 22.04+)
- **PostgreSQL**: 15+ with ARM64 support

## Phase 1: System Preparation

### 1.1 Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Install System Dependencies

```bash
sudo apt install -y \
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
    libssl-dev
```

### 1.3 Install PostgreSQL 15+

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Check PostgreSQL version
psql --version

# Enable and start PostgreSQL
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### 1.4 Configure PostgreSQL for Odoo

```bash
# Switch to postgres user
sudo -u postgres psql

# Create Odoo database user
CREATE USER odoo18 WITH CREATEDB ENCRYPTED PASSWORD 'secure_password_here';

# Exit psql
\q
```

## Phase 2: Odoo 18 Installation

### 2.1 Create Odoo User

```bash
# Create system user for Odoo
sudo useradd -m -d /opt/odoo18 -U -r -s /bin/bash odoo18

# Set permissions
sudo passwd odoo18  # Set a secure password
```

### 2.2 Install Wkhtmltopdf (for PDF reports)

```bash
# For ARM64, we need to compile or use alternative
# Option 1: Use standard package (may have limited features)
sudo apt install -y wkhtmltopdf

# Option 2: Build from source for full features (advanced)
# Check: https://wkhtmltopdf.org/downloads.html
```

### 2.3 Clone Odoo 18 Repository

```bash
# Switch to odoo18 user
sudo su - odoo18

# Navigate to home directory
cd /opt/odoo18

# Clone Odoo 18 from official repository
git clone --depth 1 --branch 18.0 https://github.com/odoo/odoo.git odoo18

# Exit odoo18 user
exit
```

### 2.4 Create Python Virtual Environment

```bash
# As odoo18 user
sudo su - odoo18

# Create virtual environment
cd /opt/odoo18
python3 -m venv odoo18-venv

# Activate virtual environment
source odoo18-venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install wheel for faster package installation
pip install wheel
```

### 2.5 Install Odoo 18 Python Dependencies

```bash
# Still as odoo18 user with venv activated
cd /opt/odoo18/odoo18

# Install requirements
pip install -r requirements.txt

# Exit odoo18 user
exit
```

## Phase 3: Configure Odoo 18 for Your Project

### 3.1 Link Your Custom Addons

```bash
# As root or your regular user
cd /opt/justo-wrks

# Create symbolic links or copy custom addons
sudo ln -s /opt/justo-wrks/addons_custom /opt/odoo18/addons_custom
sudo ln -s /opt/justo-wrks/demo_addons_custom /opt/odoo18/demo_addons_custom

# Set proper ownership
sudo chown -R odoo18:odoo18 /opt/odoo18/addons_custom
sudo chown -R odoo18:odoo18 /opt/odoo18/demo_addons_custom
```

### 3.2 Create Odoo 18 Configuration File

```bash
# Create config directory
sudo mkdir -p /etc/odoo18
sudo touch /etc/odoo18/odoo18.conf
sudo chown odoo18:odoo18 /etc/odoo18/odoo18.conf
```

### 3.3 Configure odoo18.conf

Create `/etc/odoo18/odoo18.conf` with the following content:

```ini
[options]
# Server configuration
admin_passwd = CHANGE_THIS_TO_SECURE_PASSWORD
http_port = 8069
db_host = localhost
db_port = 5432
db_user = odoo18
db_password = secure_password_here

# Paths (Ubuntu/Linux style)
addons_path = /opt/odoo18/odoo18/addons,/opt/odoo18/addons_custom,/opt/odoo18/demo_addons_custom
data_dir = /opt/odoo18/.local/share/Odoo

# Logging
logfile = /var/log/odoo18/odoo.log
log_level = info

# Performance tuning
workers = 4
max_cron_threads = 2
limit_time_cpu = 600
limit_time_real = 1200
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648

# Security
proxy_mode = True
list_db = False
```

### 3.4 Create Log Directory

```bash
sudo mkdir -p /var/log/odoo18
sudo chown odoo18:odoo18 /var/log/odoo18
```

### 3.5 Create Data Directory

```bash
sudo mkdir -p /opt/odoo18/.local/share/Odoo
sudo chown -R odoo18:odoo18 /opt/odoo18/.local
```

## Phase 4: Create Systemd Service

### 4.1 Create Service File

```bash
sudo nano /etc/systemd/system/odoo18.service
```

Add the following content:

```ini
[Unit]
Description=Odoo 18 ERP
Requires=postgresql.service
After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo18
PermissionsStartOnly=true
User=odoo18
Group=odoo18
ExecStart=/opt/odoo18/odoo18-venv/bin/python3 /opt/odoo18/odoo18/odoo-bin -c /etc/odoo18/odoo18.conf
StandardOutput=journal+console
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4.2 Enable and Start Odoo 18 Service

```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Enable Odoo 18 to start on boot
sudo systemctl enable odoo18

# Start Odoo 18
sudo systemctl start odoo18

# Check status
sudo systemctl status odoo18

# View logs
sudo journalctl -u odoo18 -f
```

## Phase 5: Firewall Configuration

```bash
# Allow Odoo port
sudo ufw allow 8069/tcp

# If using custom port (8075)
sudo ufw allow 8075/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

## Phase 6: Nginx Reverse Proxy (Optional but Recommended)

### 6.1 Install Nginx

```bash
sudo apt install -y nginx
```

### 6.2 Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/odoo18
```

Add configuration:

```nginx
upstream odoo18 {
    server 127.0.0.1:8069;
}

upstream odoo18chat {
    server 127.0.0.1:8072;
}

server {
    listen 80;
    server_name your_domain.com;

    access_log /var/log/nginx/odoo18-access.log;
    error_log /var/log/nginx/odoo18-error.log;

    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;

    # Add Headers for odoo proxy mode
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;

    # Increase proxy buffer sizes
    proxy_buffers 16 64k;
    proxy_buffer_size 128k;

    # Force timeouts if the backend dies
    proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;

    # Enable data compression
    gzip on;
    gzip_min_length 1100;
    gzip_buffers 4 32k;
    gzip_types text/css text/less text/plain text/xml application/xml application/json application/javascript application/pdf image/jpeg image/png;
    gzip_vary on;
    client_header_buffer_size 4k;
    large_client_header_buffers 4 64k;
    client_max_body_size 0;

    location / {
        proxy_pass http://odoo18;
        proxy_redirect off;
    }

    location /longpolling {
        proxy_pass http://odoo18chat;
    }

    location ~* .(js|css|png|jpg|jpeg|gif|ico)$ {
        expires 2d;
        proxy_pass http://odoo18;
        add_header Cache-Control "public, no-transform";
    }

    location ~ /[a-zA-Z0-9_-]*/static/ {
        proxy_cache_valid 200 302 60m;
        proxy_buffering on;
        expires 864000;
        proxy_pass http://odoo18;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/odoo18 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Phase 7: Testing and Verification

### 7.1 Test Odoo Installation

```bash
# Check if Odoo is running
sudo systemctl status odoo18

# Check listening ports
sudo netstat -tuln | grep 8069

# View real-time logs
sudo tail -f /var/log/odoo18/odoo.log
```

### 7.2 Access Odoo Web Interface

Open browser and navigate to:
- Direct: `http://your_server_ip:8069`
- Via Nginx: `http://your_domain.com`

### 7.3 Create Database

1. Click "Create Database"
2. Master Password: Use the `admin_passwd` from odoo18.conf
3. Database Name: Choose a name (e.g., `justo_works_prod`)
4. Email: Your admin email
5. Password: Secure admin password
6. Language: Select preferred language
7. Country: Select your country
8. Demo Data: Uncheck for production

## ARM64 Specific Notes

### Python Package Compatibility

Some Python packages may need ARM64-specific compilation:

```bash
# If you encounter issues with specific packages
sudo apt install -y python3-dev gcc g++ make

# For image processing (Pillow dependencies)
sudo apt install -y libjpeg-dev zlib1g-dev libpng-dev

# For LDAP (if using LDAP authentication)
sudo apt install -y libldap2-dev libsasl2-dev
```

### Performance Optimization for ARM64

```bash
# Install ARM64 optimized libraries
sudo apt install -y libjemalloc2

# Update Odoo service to use jemalloc
sudo nano /etc/systemd/system/odoo18.service

# Add to [Service] section:
Environment="LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libjemalloc.so.2"
```

## Troubleshooting

### Check Logs

```bash
# Odoo logs
sudo tail -f /var/log/odoo18/odoo.log

# System logs
sudo journalctl -u odoo18 -f

# Nginx logs (if using)
sudo tail -f /var/log/nginx/odoo18-error.log
```

### Common Issues

1. **Port already in use**
   ```bash
   sudo lsof -i :8069
   sudo kill -9 <PID>
   ```

2. **Permission denied errors**
   ```bash
   sudo chown -R odoo18:odoo18 /opt/odoo18
   sudo chown -R odoo18:odoo18 /var/log/odoo18
   ```

3. **Database connection errors**
   ```bash
   # Test PostgreSQL connection
   sudo -u odoo18 psql -h localhost -U odoo18 -d postgres
   ```

## Maintenance Commands

```bash
# Restart Odoo
sudo systemctl restart odoo18

# Stop Odoo
sudo systemctl stop odoo18

# Start Odoo
sudo systemctl start odoo18

# View status
sudo systemctl status odoo18

# Update Odoo (when new version available)
sudo su - odoo18
cd /opt/odoo18/odoo18
git pull origin 18.0
source /opt/odoo18/odoo18-venv/bin/activate
pip install --upgrade -r requirements.txt
exit
sudo systemctl restart odoo18
```

## Migration from Odoo 15 to Odoo 18

### Database Migration

1. **Backup Odoo 15 Database**
   ```bash
   # On Windows machine
   pg_dump -U odoo15_new -h localhost -p 5434 -F c -b -v -f "odoo15_backup.dump" database_name
   ```

2. **Transfer Backup to Ubuntu**
   ```bash
   # Use scp, rsync, or your preferred method
   scp odoo15_backup.dump user@ubuntu_server:/tmp/
   ```

3. **Restore to Odoo 18**
   ```bash
   # On Ubuntu machine
   sudo -u odoo18 createdb -h localhost -U odoo18 justo_works_migrated
   sudo -u odoo18 pg_restore -h localhost -U odoo18 -d justo_works_migrated /tmp/odoo15_backup.dump
   ```

4. **Run Odoo 18 Migration**
   ```bash
   sudo su - odoo18
   source /opt/odoo18/odoo18-venv/bin/activate
   /opt/odoo18/odoo18/odoo-bin -c /etc/odoo18/odoo18.conf -d justo_works_migrated -u all --stop-after-init
   ```

**Note**: Odoo 15 to 18 is a major version jump. Consider:
- Testing migration in a staging environment first
- Reviewing module compatibility
- Custom module updates may be required
- Consider intermediate upgrades (15→16→17→18)

## Security Recommendations

1. **Change default admin password** in odoo18.conf
2. **Set strong database password** for odoo18 user
3. **Enable SSL/TLS** with Let's Encrypt if publicly accessible
4. **Set up UFW firewall** properly
5. **Regular backups** of database and filestore
6. **Keep system updated**: `sudo apt update && sudo apt upgrade`
7. **Monitor logs** for suspicious activity
8. **Disable database manager** in production: `list_db = False`

## Next Steps

See `DEVELOPMENT_ROADMAP.md` for the complete project phases and development plan.
