# Project Guidelines

## Mandatory Development Rules

### AI Development Branch Policy

**MANDATORY RULE:** AI development will continue on this branch (`claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx`). No additional branches will be created unless explicitly authorized.

This ensures:
- Continuity of development work
- Clear tracking of AI-assisted changes
- Simplified review and merge processes
- Consistent development workflow

## Repository Setup

### Standard Odoo Files

This repository has been optimized to exclude standard Odoo core files, addons, and themes. These files should be downloaded separately to reduce repository clone size.

**What's excluded from git:**
- `addons/` - Standard Odoo addons (608MB)
- `themes15/` - Standard Odoo themes (298MB)
- `odoo/` - Odoo core files (72MB)
- `reports15/` - Standard reports (6.1MB)
- `common/` - Common libraries (16MB)

**What's tracked in git:**
- `addons_custom/` - Custom addons specific to this project
- `demo_addons_custom/` - Custom demo addons
- Configuration files and scripts

### Initial Setup

To set up the development environment:

```bash
# 1. Clone the repository (now much smaller!)
git clone <repository-url>
cd Justo-Works

# 2. Download Odoo core files (choose one method):

# Method A: Via pip
pip install odoo

# Method B: Via git clone
git clone --depth 1 --branch 15.0 https://github.com/odoo/odoo.git

# 3. Install custom addons dependencies (if any)
pip install -r requirements.txt

# 4. Configure Odoo
# Edit odoo.conf to point to the correct addon paths
```

### Benefit

The repository size has been reduced from **~479MB** to a much smaller footprint by excluding standard Odoo files. This means:
- Faster cloning
- Reduced bandwidth usage
- Faster git operations
- Focus on custom code only

## Odoo 18 Migration Status

This project is migrating from **Odoo 15 (Windows)** to **Odoo 18 (Ubuntu ARM64)**.

### Platform Change
- **From**: Windows-based development (`C:\jworks\odoo15\`)
- **To**: OCI Ampere Ubuntu ARM64 (`/opt/odoo18/`)

### Version Upgrade
- **From**: Odoo 15.0
- **To**: Odoo 18.0

### Key Documents
- `ODOO_18_UBUNTU_ARM64_SETUP.md` - Complete setup guide for Ubuntu ARM64
- `DEVELOPMENT_ROADMAP.md` - Full project roadmap with all phases
- `setup_odoo18_ubuntu.sh` - Automated installation script
- `odoo.conf` - Updated configuration for Linux paths

### Quick Start on Ubuntu

1. **Automated Setup** (Recommended):
   ```bash
   # Edit the script to set secure passwords first!
   sudo bash setup_odoo18_ubuntu.sh
   ```

2. **Manual Setup**:
   Follow step-by-step instructions in `ODOO_18_UBUNTU_ARM64_SETUP.md`

### Current Phase
**Phase 1**: Odoo 18 Environment Setup (In Progress)
- See `DEVELOPMENT_ROADMAP.md` for complete phase breakdown
