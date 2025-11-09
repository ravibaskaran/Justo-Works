# Database Management Scripts

PostgreSQL database creation and management tools for Odoo migration.

## Quick Reference

```bash
# Create new test database
./create_test_db.sh odoo18_test

# Reset existing database (drop and recreate)
./reset_test_db.sh odoo18_test

# Connect to database
psql -h localhost -p 5434 -U odoo15_new -d odoo18_test
```

## Database Naming Convention

Use descriptive names to track migration progress:

```
odoo15              # Original Odoo 15 production database
odoo18_test         # Odoo 18 test database (fresh installation)
odoo15_to_16_test   # Migration step 1: 15 → 16
odoo16_to_17_test   # Migration step 2: 16 → 17
odoo17_to_18_test   # Migration step 3: 17 → 18
odoo18_migrated     # Final migrated database
odoo18_prod         # Production Odoo 18 database
```

## Scripts

### create_test_db.sh

Creates a new PostgreSQL database with required extensions.

**Usage:**
```bash
./create_test_db.sh <database_name>
```

**Features:**
- Creates UTF-8 encoded database
- Installs pg_trgm extension (trigram matching for search)
- Installs unaccent extension (remove accents for search)
- Checks for existing database
- Prompts before overwriting

**Examples:**
```bash
# Create test database for Odoo 18
./create_test_db.sh odoo18_test

# Create migration staging database
./create_test_db.sh odoo15_to_16_test

# Create production database
export DB_HOST=production.server.com
export DB_PORT=5432
./create_test_db.sh odoo18_prod
```

### reset_test_db.sh

Drops and recreates a database (useful for testing).

**Usage:**
```bash
./reset_test_db.sh <database_name>
```

**⚠ WARNING**: This permanently deletes all data in the database!

**Examples:**
```bash
# Reset test database
./reset_test_db.sh odoo18_test

# Reset after failed migration
./reset_test_db.sh odoo15_to_16_test
```

## Environment Variables

Configure database connection settings:

```bash
export DB_HOST=localhost        # Database host
export DB_PORT=5434             # Database port
export DB_USER=odoo15_new       # PostgreSQL user
export DB_PASSWORD=odoo15_new   # PostgreSQL password
```

## Database Extensions

### Required Extensions

**pg_trgm** - Trigram matching for text search
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

**unaccent** - Remove accents from text
```sql
CREATE EXTENSION IF NOT EXISTS unaccent;
```

### Optional Extensions

**pgcrypto** - Cryptographic functions
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

**pg_stat_statements** - Query performance tracking
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

## Database Operations

### Connect to Database

```bash
# Using psql
psql -h localhost -p 5434 -U odoo15_new -d odoo18_test

# Using environment variables
export PGHOST=localhost
export PGPORT=5434
export PGUSER=odoo15_new
export PGPASSWORD=odoo15_new
psql -d odoo18_test
```

### List Databases

```bash
psql -h localhost -p 5434 -U odoo15_new -l
```

### Check Database Size

```sql
SELECT pg_database.datname,
       pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
WHERE datname LIKE 'odoo%'
ORDER BY pg_database_size(pg_database.datname) DESC;
```

### Copy Database

```bash
# Create copy for testing
createdb -h localhost -p 5434 -U odoo15_new -T odoo15 odoo15_copy
```

### Drop Database

```bash
# Drop database
dropdb -h localhost -p 5434 -U odoo15_new odoo18_test

# Drop with force (terminate connections)
psql -h localhost -p 5434 -U odoo15_new << EOF
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'odoo18_test';
DROP DATABASE odoo18_test;
EOF
```

## Migration Workflow

### 1. Create Test Database

```bash
./create_test_db.sh odoo15_to_16_test
```

### 2. Restore Odoo 15 Backup

```bash
cd ../backup
./restore_database.sh latest.backup odoo15_to_16_test
```

### 3. Run Migration

```bash
cd ../openupgrade
# Run OpenUpgrade migration scripts
```

### 4. Validate Results

```bash
psql -h localhost -p 5434 -U odoo15_new -d odoo15_to_16_test

-- Check module states
SELECT name, state FROM ir_module_module WHERE state = 'installed';

-- Check record counts
SELECT COUNT(*) FROM res_partner;
SELECT COUNT(*) FROM sale_order;
SELECT COUNT(*) FROM account_move;
```

### 5. Reset and Retry if Needed

```bash
./reset_test_db.sh odoo15_to_16_test
# Restore and try again
```

## Troubleshooting

### Connection Refused

**Issue:** `psql: error: connection to server at "localhost" (::1), port 5434 failed`

**Solutions:**
1. Check PostgreSQL is running:
   ```bash
   systemctl status postgresql
   ```

2. Verify port number:
   ```bash
   sudo netstat -tlnp | grep 5434
   ```

3. Check pg_hba.conf allows local connections

### Permission Denied

**Issue:** `ERROR: permission denied to create database`

**Solution:** Ensure user has CREATEDB privilege:
```sql
ALTER USER odoo15_new CREATEDB;
```

### Database Exists

**Issue:** `ERROR: database "odoo18_test" already exists`

**Solution:** Drop existing database first:
```bash
dropdb -h localhost -p 5434 -U odoo15_new odoo18_test
```

Or use reset script:
```bash
./reset_test_db.sh odoo18_test
```

### Extension Not Available

**Issue:** `ERROR: could not open extension control file`

**Solution:** Install PostgreSQL contrib package:
```bash
sudo apt-get install postgresql-contrib
```

## Best Practices

1. **Use descriptive names** - Include version and purpose in database name
2. **Always backup** - Create backup before making changes
3. **Test on copy** - Never test migrations on production database
4. **Document changes** - Keep log of database operations
5. **Clean up old databases** - Remove test databases after migration complete

## Database Security

### Production Databases

For production deployments:

1. **Use strong passwords:**
   ```bash
   # Generate secure password
   openssl rand -base64 32
   ```

2. **Restrict network access:**
   Edit `pg_hba.conf`:
   ```
   # Allow localhost only
   host    odoo18_prod    odoo18    127.0.0.1/32    scram-sha-256
   ```

3. **Use SSL connections:**
   ```bash
   psql "sslmode=require host=localhost dbname=odoo18_prod"
   ```

4. **Regular backups:**
   ```bash
   # Daily automated backup
   0 2 * * * /path/to/backup_database.sh
   ```

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Odoo Database Management](https://www.odoo.com/documentation/18.0/administration/install.html)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

## Next Steps

After database setup:
1. Test database connectivity
2. Restore Odoo 15 backup
3. Proceed to OpenUpgrade migration
4. Validate migrated data
