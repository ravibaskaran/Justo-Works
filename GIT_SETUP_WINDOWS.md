# Git Setup for Windows - Complete Migration Branch

This guide helps you access the consolidated migration branch on your Windows machine.

## Quick Summary

**Single Source-of-Truth Branch:**
- `claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM`

This branch now contains:
- ✅ Phase 0: Security & Validation Fixes
- ✅ Phase 1: Odoo 18 Environment Setup
- ✅ Remote OCI Deployment Scripts

**Old branches to delete:** (already merged, no longer needed)
- `claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR`
- `claude/phase-0-security-validation-fixes-011CUwdbhDznwKoA5bRxj52G`

---

## Step-by-Step Instructions for Windows

### 1. Open Git Bash or PowerShell

Navigate to your repository:
```bash
cd /path/to/Justo-Works
```

### 2. Fetch All Remote Changes

```bash
git fetch --all --prune
```

This downloads all branches and removes references to deleted remote branches.

### 3. Switch to the Consolidated Branch

```bash
# Checkout the main migration branch
git checkout claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM

# Pull latest changes
git pull origin claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM
```

### 4. Verify You Have All the Work

```bash
# Check recent commits (should show both Phase 0 and Phase 1)
git log --oneline -20

# Expected output includes:
# - ba36d815 Merge Phase 0 and Phase 1: Complete Migration Foundation
# - a46b7e63 Phase 1: Odoo 18 Environment Setup - Complete
# - 4e8fa655 Phase 0: 90% complete
# - ... (and more Phase 0 commits)
```

### 5. Clean Up Old Local Branches

Delete old local branches (they're already merged):

```bash
# Delete old branches locally
git branch -d claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR
git branch -d claude/phase-0-security-validation-fixes-011CUwdbhDznwKoA5bRxj52G

# If above fails (branch not fully merged), force delete:
git branch -D claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR
git branch -D claude/phase-0-security-validation-fixes-011CUwdbhDznwKoA5bRxj52G
```

### 6. Delete Old Remote Branches (Optional)

**Option A: Via Git Command Line**

```bash
git push origin --delete claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR
git push origin --delete claude/phase-0-security-validation-fixes-011CUwdbhDznwKoA5bRxj52G
```

**Option B: Via GitHub Web Interface** (if command fails)

1. Go to: https://github.com/ravibaskaran/Justo-Works/branches
2. Find old branches:
   - `claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR`
   - `claude/phase-0-security-validation-fixes-011CUwdbhDznwKoA5bRxj52G`
3. Click the trash icon next to each branch to delete

### 7. Clean Up Remote References Locally

```bash
# Remove stale remote-tracking branches
git remote prune origin

# Verify - should only show the main branch now
git branch -r
```

Expected output:
```
  remotes/origin/claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM
```

### 8. Verify Your Setup

```bash
# Check current branch
git branch

# Should show:
# * claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM

# Check what files you have
ls migration/
# Should show: README.md backup/ database/ inventory/ odoo18/ openupgrade/

ls openspec/
# Should show: AGENTS.md changes/ project.md specs/

# Check remote branches
git branch -r
# Should ONLY show: remotes/origin/claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM
```

---

## What You Should Have Now

### Directory Structure

```
Justo-Works/
├── .gitignore (updated with migration artifacts)
├── GIT_SETUP_WINDOWS.md (this file)
│
├── addons_custom/
│   └── real_estate_extension/
│       ├── controllers/ (with Phase 0 security fixes)
│       ├── models/ (with sanitizer, validators)
│       └── views/ (updated API logs)
│
├── migration/                    # Phase 1
│   ├── README.md
│   ├── inventory/
│   │   ├── MODULE_INVENTORY.md
│   │   ├── odoo15_modules.csv
│   │   └── ... (551 modules documented)
│   ├── backup/
│   │   ├── backup_all.sh
│   │   └── ... (7 scripts)
│   ├── odoo18/
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   ├── REMOTE_SETUP.md
│   │   ├── deploy-to-remote.sh
│   │   └── ...
│   ├── database/
│   ├── openupgrade/
│   └── ...
│
└── openspec/                     # Phase 0
    ├── AGENTS.md
    ├── project.md
    ├── changes/
    │   ├── api-logging-security-fixes/
    │   ├── api-validation-fixes/
    │   ├── phase-0-security-validation-fixes/
    │   ├── phase-1-odoo-18-environment-setup/
    │   └── ...
    └── specs/
        ├── api-logging/
        ├── customer-api/
        ├── employee-api/
        └── ... (13 specs total)
```

### Commit History

```bash
# View full history
git log --oneline --graph --all

# Should show merged history with both Phase 0 and Phase 1 commits
```

---

## Common Issues & Solutions

### Issue: "Branch not found"

**Solution:**
```bash
# Make sure you've fetched latest
git fetch origin

# List all remote branches
git branch -r

# Checkout with full path
git checkout -b claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM origin/claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM
```

### Issue: "Cannot delete branch - not fully merged"

**Solution:**
```bash
# Force delete (safe - already merged on consolidated branch)
git branch -D branch-name
```

### Issue: "Remote branch delete fails with 403"

**Solution:**
Use GitHub web interface:
1. Go to https://github.com/ravibaskaran/Justo-Works/branches
2. Delete branches manually

### Issue: "Conflicts when pulling"

**Solution:**
```bash
# Stash your local changes
git stash

# Pull latest
git pull origin claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM

# Apply your changes back
git stash pop
```

---

## Deploying to Remote OCI Server

After you've pulled the branch on Windows:

### Transfer Files to Remote

**Option 1: Using the Deploy Script**

```bash
cd migration/odoo18
./deploy-to-remote.sh
```

**Option 2: Manual SCP from Windows**

```powershell
# From PowerShell or Git Bash
cd C:\path\to\Justo-Works\migration\odoo18

# Copy files to remote
scp -i "D:\temp\OCI\.ssh\id_ed25519" -r * ubuntu@140.245.226.156:/home/ubuntu/odoo18-migration/
```

### SSH to Remote and Start Odoo

```bash
# SSH to server
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156

# Navigate to directory
cd /home/ubuntu/odoo18-migration

# Build and start
docker compose build
docker compose up -d

# View logs
docker compose logs -f odoo18
```

### Access in Browser

**After configuring OCI firewall (see REMOTE_SETUP.md):**

http://140.245.226.156:8069

---

## Next Steps

1. ✅ Pull consolidated branch on Windows
2. ✅ Delete old local branches
3. ✅ Delete old remote branches
4. ✅ Verify all files present
5. → Deploy to OCI remote server
6. → Start Phase 2: Core Module Validation

---

## Branch Policy Going Forward

**IMPORTANT:** All future work should be done on:
- **Branch:** `claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM`
- This is now the SINGLE source of truth
- No new branches unless explicitly needed for specific PRs

When ready for production:
- Create PR: `claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM` → `main`
- After merge, use `main` as the production branch

---

## Quick Reference Commands

```bash
# Pull latest
git pull origin claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM

# Check what you have
git log --oneline -20
git status

# View branches
git branch -a

# Clean up
git remote prune origin
git branch -d old-branch-name

# Deploy to OCI
cd migration/odoo18
./deploy-to-remote.sh

# SSH to OCI
ssh -i "D:\temp\OCI\.ssh\id_ed25519" ubuntu@140.245.226.156
```

---

## Support

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review `migration/README.md` for migration workflow
3. Review `migration/odoo18/REMOTE_SETUP.md` for OCI deployment
4. Check Git status: `git status`
5. Check branch: `git branch -a`

All documentation is in the repository under `migration/` and `openspec/`.
