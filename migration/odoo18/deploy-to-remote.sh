#!/bin/bash
# Deploy Odoo 18 to Remote OCI Server
# Usage: ./deploy-to-remote.sh

set -e

# Remote server configuration
REMOTE_USER="ubuntu"
REMOTE_HOST="140.245.226.156"
SSH_KEY="D:/temp/OCI/.ssh/id_ed25519"  # Update this path if needed
REMOTE_DIR="/home/ubuntu/odoo18-migration"

echo "========================================="
echo "Deploying Odoo 18 to Remote OCI Server"
echo "========================================="
echo "Remote: $REMOTE_USER@$REMOTE_HOST"
echo "Target: $REMOTE_DIR"
echo "========================================="

# Create remote directory
echo "Creating remote directory..."
ssh -i "$SSH_KEY" $REMOTE_USER@$REMOTE_HOST "mkdir -p $REMOTE_DIR"

# Copy migration files to remote server
echo "Copying migration files..."
scp -i "$SSH_KEY" -r \
    migration/odoo18/* \
    $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/

echo "✓ Files copied successfully"

# Create setup script on remote
echo "Creating remote setup script..."
ssh -i "$SSH_KEY" $REMOTE_USER@$REMOTE_HOST "cat > $REMOTE_DIR/setup.sh" << 'REMOTE_SCRIPT'
#!/bin/bash
set -e

echo "========================================="
echo "Setting up Odoo 18 on OCI Server"
echo "========================================="

cd /home/ubuntu/odoo18-migration

# Check Docker
echo "Checking Docker installation..."
docker --version
docker compose version

# Create necessary directories
echo "Creating directories..."
mkdir -p backups/database backups/filestore backups/modules

# Build Docker images
echo "Building Docker images..."
docker compose build

# Start services
echo "Starting services..."
docker compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check service status
echo "Checking service status..."
docker compose ps

# Check Odoo logs
echo ""
echo "Odoo logs (last 20 lines):"
docker compose logs --tail=20 odoo18

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo "Odoo 18 is running on:"
echo "  http://140.245.226.156:8069"
echo ""
echo "To check logs:"
echo "  cd $REMOTE_DIR && docker compose logs -f odoo18"
echo ""
echo "To access Odoo CLI:"
echo "  cd $REMOTE_DIR && docker compose exec odoo18 bash"
echo "========================================="
REMOTE_SCRIPT

# Make setup script executable
ssh -i "$SSH_KEY" $REMOTE_USER@$REMOTE_HOST "chmod +x $REMOTE_DIR/setup.sh"

# Run setup script
echo ""
echo "Running remote setup..."
ssh -i "$SSH_KEY" $REMOTE_USER@$REMOTE_HOST "$REMOTE_DIR/setup.sh"

echo ""
echo "========================================="
echo "✓ Deployment Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Configure OCI firewall to allow port 8069"
echo "2. Access Odoo at: http://140.245.226.156:8069"
echo ""
echo "SSH to server:"
echo "  ssh -i \"$SSH_KEY\" $REMOTE_USER@$REMOTE_HOST"
echo ""
echo "View logs:"
echo "  ssh -i \"$SSH_KEY\" $REMOTE_USER@$REMOTE_HOST \"cd $REMOTE_DIR && docker compose logs -f\""
echo "========================================="
