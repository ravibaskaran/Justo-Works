# Odoo 18 Environment Setup

Complete Docker-based Odoo 18 environment for migration from Odoo 15.

## Quick Start

### 1. Build and Start Odoo 18

```bash
cd migration/odoo18

# Build Docker images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f odoo18
```

### 2. Access Odoo 18

- **Odoo Web Interface**: http://localhost:8069
- **Database Manager**: http://localhost:8069/web/database/manager
- **PostgreSQL**: localhost:5433
- **pgAdmin** (optional): http://localhost:5050

### 3. Verify Installation

```bash
# Check Odoo version
docker-compose exec odoo18 ./odoo-bin --version

# Should output: Odoo Server 18.0
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Environment              │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐    ┌──────────────┐   │
│  │  Odoo 18    │───▶│ PostgreSQL   │   │
│  │  App        │    │ 15           │   │
│  │  :8069      │    │ :5432        │   │
│  └─────────────┘    └──────────────┘   │
│         │                               │
│         ▼                               │
│  ┌─────────────────────────────────┐   │
│  │  Custom Addons (mounted)        │   │
│  │  - addons_custom/               │   │
│  │  - common/                      │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         │
         ▼
    Host Machine
    (Justo-Works repository)
```

## Configuration

### Database Configuration

- **Host**: db (internal) / localhost:5433 (external)
- **Database**: odoo18
- **User**: odoo18
- **Password**: odoo18_secure_password (change for production!)

**Update credentials in:**
- `docker-compose.yml` (POSTGRES_* environment variables)
- `odoo18.conf` (db_* settings)

### Odoo Configuration

Edit `odoo18.conf` to customize:

```ini
# Admin password (use for database management)
admin_passwd = $pbkdf2-sha512$25000$admin_master_password_change_me

# Workers (adjust based on CPU cores)
workers = 4

# Memory limits (adjust based on available RAM)
limit_memory_hard = 2684354560  # 2.5 GB
limit_memory_soft = 2147483648  # 2 GB

# Database filter (for multi-database)
dbfilter = ^odoo18.*$
```

### Custom Addons

Custom modules are mounted from the host:

```yaml
volumes:
  - ../../addons_custom:/opt/odoo/custom-addons/addons_custom:ro
  - ../../common:/opt/odoo/custom-addons/common:ro
```

**Note**: Modules are mounted read-only (`:ro`) during migration testing. Remove `:ro` if you need to modify modules inside the container.

## Docker Commands

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart Odoo (after config changes)
docker-compose restart odoo18

# View logs
docker-compose logs -f odoo18

# Execute commands in container
docker-compose exec odoo18 bash
```

### Database Operations

```bash
# Create new database
docker-compose exec odoo18 ./odoo-bin -d odoo18_test --init=base --stop-after-init

# Update modules
docker-compose exec odoo18 ./odoo-bin -d odoo18 -u all --stop-after-init

# Shell access to database
docker-compose exec db psql -U odoo18 -d odoo18

# Backup database
docker-compose exec db pg_dump -U odoo18 odoo18 > odoo18_backup.sql
```

### Development Mode

```bash
# Start with XML debugging and auto-reload
docker-compose up odoo18 -d
docker-compose exec odoo18 ./odoo-bin -c /opt/odoo/odoo.conf --dev=xml,reload

# Run tests for specific module
docker-compose exec odoo18 ./odoo-bin -d odoo18 -i module_name --test-enable --stop-after-init
```

## Directory Structure

```
migration/odoo18/
├── Dockerfile              # Odoo 18 container definition
├── docker-compose.yml      # Multi-container orchestration
├── odoo18.conf            # Odoo configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── init-db/               # Database initialization scripts (optional)
```

## Python Environment

- **Python Version**: 3.11+ (Debian Bookworm)
- **Package Manager**: pip3
- **Dependencies**: See `requirements.txt`

### Install Additional Packages

```bash
# Add to requirements.txt, then rebuild
docker-compose build odoo18
docker-compose up -d odoo18
```

## Volumes

Persistent data is stored in Docker volumes:

```
odoo18-db-data      # PostgreSQL database
odoo18-data         # Odoo data directory
odoo18-filestore    # Uploaded files, attachments
odoo18-sessions     # Session data
odoo18-logs         # Log files
```

### Inspect Volumes

```bash
# List volumes
docker volume ls | grep odoo18

# Inspect volume
docker volume inspect odoo18-db-data

# Backup volume
docker run --rm -v odoo18-filestore:/data -v $(pwd):/backup alpine tar czf /backup/filestore.tar.gz /data
```

## Migration Workflow

### Phase 1: Fresh Odoo 18 Installation

1. Start Odoo 18 environment
2. Create empty database
3. Install base modules
4. Verify core functionality

```bash
docker-compose up -d
docker-compose exec odoo18 ./odoo-bin -d odoo18_fresh --init=base,web --stop-after-init
```

### Phase 2: Core Module Validation

1. Install all Odoo 15 core modules on Odoo 18
2. Test each module functionality
3. Document any breaking changes

### Phase 3: Custom Module Migration

1. Copy custom modules to container
2. Update manifests for Odoo 18
3. Fix deprecated code
4. Test module installation

### Phase 4: OpenUpgrade Migration

1. Restore Odoo 15 database to PostgreSQL
2. Run OpenUpgrade migration scripts
3. Validate migrated data

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs odoo18

# Common issues:
# - Port 8069 already in use (change in docker-compose.yml)
# - PostgreSQL not ready (wait for health check)
# - Configuration error (check odoo18.conf syntax)
```

### Database Connection Failed

```bash
# Test PostgreSQL connection
docker-compose exec odoo18 psql -h db -U odoo18 -d odoo18

# If fails:
# 1. Check PostgreSQL is running: docker-compose ps db
# 2. Verify credentials in docker-compose.yml and odoo18.conf
# 3. Check network: docker network inspect odoo18_odoo18-network
```

### Module Installation Fails

```bash
# Check module path
docker-compose exec odoo18 ls -la /opt/odoo/custom-addons/

# Check Odoo logs for errors
docker-compose logs odoo18 | grep ERROR

# Validate manifest file
docker-compose exec odoo18 python3 -c "import ast; print(ast.literal_eval(open('/opt/odoo/custom-addons/addons_custom/module_name/__manifest__.py').read()))"
```

### Performance Issues

```bash
# Increase workers (in odoo18.conf)
workers = 8

# Increase memory limits
limit_memory_hard = 4294967296  # 4 GB

# Enable database connection pooling
db_maxconn = 128

# Restart container
docker-compose restart odoo18
```

## Security Notes

**IMPORTANT**: Before production deployment:

1. **Change default passwords**:
   - admin_passwd in odoo18.conf
   - PostgreSQL password in docker-compose.yml

2. **Use strong passwords**:
   ```bash
   # Generate secure password
   openssl rand -base64 32
   ```

3. **Restrict database access**:
   ```ini
   # In odoo18.conf
   list_db = False  # Hide database list
   ```

4. **Enable proxy mode** (if using nginx/Apache):
   ```ini
   proxy_mode = True
   ```

5. **Secure PostgreSQL**:
   - Don't expose port 5433 externally (remove from docker-compose.yml)
   - Use SSL connections
   - Restrict network access

## Next Steps

After environment setup:

1. ✅ Verify Odoo 18 starts correctly
2. ✅ Test database connectivity
3. ✅ Access web interface
4. → Proceed to Phase 2: Core Module Validation
5. → Set up OpenUpgrade for migration

## Resources

- [Odoo 18 Documentation](https://www.odoo.com/documentation/18.0/)
- [Odoo Docker Hub](https://hub.docker.com/_/odoo)
- [PostgreSQL 15 Documentation](https://www.postgresql.org/docs/15/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Support

For issues or questions:
1. Check logs: `docker-compose logs odoo18`
2. Review troubleshooting section above
3. Consult Odoo community forums
4. Check migration documentation in `migration/README.md`
