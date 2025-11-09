# Remote Odoo 18 Setup on OCI

Complete guide for deploying Odoo 18 to Oracle Cloud Infrastructure (OCI) Ampere Ubuntu 24.04 server.

## Server Details

- **OS**: Ubuntu 24.04 (ARM64 - Ampere)
- **Public IP**: 140.245.226.156
- **SSH Access**: `ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156`
- **Docker**: Docker Compose v2 installed

## Quick Deployment

### Option 1: Automated Deployment (Recommended)

From your local Windows machine:

```bash
cd migration/odoo18
./deploy-to-remote.sh
```

This script will:
1. Create remote directory: `/home/ubuntu/odoo18-migration`
2. Copy all Odoo 18 files to remote server
3. Build Docker images on remote
4. Start Odoo 18 and PostgreSQL containers

### Option 2: Manual Deployment

#### Step 1: Copy Files to Remote Server

```bash
# From Windows (PowerShell or Git Bash)
cd /path/to/Justo-Works/migration/odoo18

scp -i "D:\temp\OCI\.ssh\id_ed25519" -r * ubuntu@140.245.226.156:/home/ubuntu/odoo18-migration/
```

#### Step 2: SSH to Remote Server

```bash
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156
```

#### Step 3: Build and Start on Remote

```bash
cd /home/ubuntu/odoo18-migration

# Verify Docker is installed
docker --version
docker compose version

# Build images
docker compose build

# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f odoo18
```

## Accessing Odoo 18 in Browser

### 1. Configure OCI Firewall (REQUIRED)

**OCI Security List (Ingress Rules):**

You must add an ingress rule in OCI Console:

1. Go to: **OCI Console** → **Networking** → **Virtual Cloud Networks**
2. Select your VCN
3. Click **Security Lists** → Select your security list
4. Click **Add Ingress Rules**
5. Add rule:
   - **Source CIDR**: `0.0.0.0/0` (or your IP for security)
   - **IP Protocol**: TCP
   - **Destination Port Range**: `8069`
   - **Description**: Odoo 18 Web Interface

6. Save the rule

**Ubuntu Firewall (if enabled):**

```bash
# SSH to server first
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156

# Allow port 8069
sudo ufw allow 8069/tcp

# Check status
sudo ufw status
```

### 2. Access Odoo in Browser

After configuring the firewall:

**URL**: http://140.245.226.156:8069

**First Access:**
1. You'll see the Odoo database manager
2. Create a new database:
   - **Master Password**: (from odoo18.conf - change this!)
   - **Database Name**: odoo18
   - **Email**: admin@example.com
   - **Password**: (choose secure password)
   - **Language**: English
   - **Country**: India
3. Click **Create Database**

**Login:**
- **URL**: http://140.245.226.156:8069/web/login
- **Email**: admin@example.com
- **Password**: (password you set)

## Remote Server Commands

### SSH Access

```bash
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156
```

### Docker Commands on Remote

```bash
# Navigate to project directory
cd /home/ubuntu/odoo18-migration

# View running containers
docker compose ps

# View logs
docker compose logs -f odoo18

# Stop services
docker compose down

# Restart services
docker compose restart odoo18

# Access Odoo container shell
docker compose exec odoo18 bash

# Access PostgreSQL
docker compose exec db psql -U odoo18 -d odoo18
```

### Odoo Commands on Remote

```bash
cd /home/ubuntu/odoo18-migration

# Check Odoo version
docker compose exec odoo18 ./odoo-bin --version

# Access Odoo shell
docker compose exec odoo18 ./odoo-bin shell -d odoo18

# Update modules
docker compose exec odoo18 ./odoo-bin -d odoo18 -u all --stop-after-init

# Install module
docker compose exec odoo18 ./odoo-bin -d odoo18 -i module_name --stop-after-init
```

## File Transfer Between Local and Remote

### Upload Files to Remote

```bash
# From Windows
scp -i "D:\temp\OCI\.ssh\id_ed25519" -r local_folder ubuntu@140.245.226.156:/home/ubuntu/destination/
```

### Download Files from Remote

```bash
# From Windows
scp -i "D:\temp\OCI\.ssh\id_ed25519" -r ubuntu@140.245.226.156:/home/ubuntu/source/ local_folder/
```

### Upload Custom Modules

```bash
# From Justo-Works directory
cd /path/to/Justo-Works

# Upload custom modules
scp -i "D:\temp\OCI\.ssh\id_ed25519" -r addons_custom ubuntu@140.245.226.156:/home/ubuntu/odoo18-migration/

# On remote, modules are mounted in docker-compose.yml
# They'll be available in container at: /opt/odoo/custom-addons/addons_custom
```

## Configuration Updates

### Change Odoo Configuration

```bash
# SSH to server
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156

cd /home/ubuntu/odoo18-migration

# Edit configuration
nano odoo18.conf

# Restart Odoo to apply changes
docker compose restart odoo18
```

### Change Database Password

Edit `docker-compose.yml`:

```bash
nano docker-compose.yml

# Update these values:
POSTGRES_PASSWORD: your_new_secure_password

# Also update in odoo18.conf:
db_password = your_new_secure_password

# Recreate containers
docker compose down
docker compose up -d
```

## Port Forwarding (Alternative Access Method)

If you can't open port 8069 on OCI firewall, use SSH port forwarding:

```bash
# From Windows
ssh -i "D:\temp\OCI\.ssh\id_ed25519" -L 8069:localhost:8069 ubuntu@140.245.226.156

# Keep this terminal open
# Access in browser: http://localhost:8069
```

This creates a tunnel - Odoo runs on remote but accessible via localhost.

## Troubleshooting

### Check if Odoo is Running

```bash
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156

# Check Docker containers
docker compose ps

# Check port 8069 is listening
sudo netstat -tlnp | grep 8069

# Or
sudo ss -tlnp | grep 8069
```

### Odoo Container Won't Start

```bash
# Check logs
docker compose logs odoo18

# Common issues:
# 1. Port 8069 already in use
docker compose down
docker ps -a  # Check for other containers
docker compose up -d

# 2. PostgreSQL not ready
docker compose restart db
sleep 10
docker compose restart odoo18
```

### Can't Access in Browser

**Check firewall:**
```bash
# OCI Security List - Check OCI Console
# Ubuntu firewall
sudo ufw status

# Test port locally on server
curl http://localhost:8069

# If works locally but not externally, it's firewall issue
```

**Check Docker networking:**
```bash
docker compose exec odoo18 netstat -tlnp | grep 8069

# Should show: 0.0.0.0:8069
```

### Database Connection Issues

```bash
# Test PostgreSQL
docker compose exec db psql -U odoo18 -l

# Check network
docker network ls
docker network inspect odoo18_odoo18-network

# Restart both services
docker compose restart db odoo18
```

## Performance Optimization for ARM64

Ubuntu 24.04 on OCI Ampere (ARM64) requires some optimizations:

### Update docker-compose.yml

```yaml
# Add platform specification
services:
  odoo18:
    platform: linux/arm64
    # ... rest of config

  db:
    platform: linux/arm64
    # ... rest of config
```

### Increase Workers (if you have more CPU cores)

In `odoo18.conf`:
```ini
workers = 8  # Ampere typically has many cores
max_cron_threads = 2
```

### Memory Optimization

```ini
limit_memory_hard = 8589934592  # 8 GB (Ampere VMs often have more RAM)
limit_memory_soft = 6442450944  # 6 GB
```

## Security Best Practices

### 1. Change Default Passwords

```bash
# Generate secure password
openssl rand -base64 32

# Update odoo18.conf
admin_passwd = $pbkdf2-sha512$25000$your_generated_hash

# Update docker-compose.yml
POSTGRES_PASSWORD: your_secure_database_password
```

### 2. Restrict Database Access

In `odoo18.conf`:
```ini
list_db = False  # Hide database list from public
```

### 3. Use Firewall Restrictions

In OCI Security List, restrict source IP to your office/home IP instead of 0.0.0.0/0:
```
Source CIDR: your.public.ip.address/32
```

### 4. Enable SSL (Production)

Set up nginx reverse proxy with Let's Encrypt:
```bash
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Backup on Remote Server

```bash
# SSH to server
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156

cd /home/ubuntu/odoo18-migration

# Backup database
docker compose exec db pg_dump -U odoo18 odoo18 > backups/database/odoo18_$(date +%Y%m%d).sql

# Backup filestore
docker compose exec odoo18 tar -czf /tmp/filestore.tar.gz /opt/odoo/data/filestore
docker compose cp odoo18:/tmp/filestore.tar.gz backups/filestore/

# Download backups to local
scp -i "D:\temp\OCI\.ssh\id_ed25519" -r ubuntu@140.245.226.156:/home/ubuntu/odoo18-migration/backups/ ./local-backups/
```

## Monitoring

### View Resource Usage

```bash
# CPU and Memory
docker stats

# Disk usage
df -h
docker system df
```

### View Logs in Real-time

```bash
# Odoo logs
docker compose logs -f odoo18

# PostgreSQL logs
docker compose logs -f db

# All services
docker compose logs -f
```

## Next Steps

After successful deployment:

1. ✅ Access Odoo at http://140.245.226.156:8069
2. ✅ Create initial database
3. ✅ Install base modules
4. → Upload custom modules for Phase 3 testing
5. → Run migration scripts
6. → Validate functionality

## Support

**Common URLs:**
- Web Interface: http://140.245.226.156:8069
- Database Manager: http://140.245.226.156:8069/web/database/manager
- Health Check: http://140.245.226.156:8069/web/health

**Documentation:**
- Main migration guide: `migration/README.md`
- Odoo 18 setup: `migration/odoo18/README.md`
- Local development: Use same Docker setup locally
