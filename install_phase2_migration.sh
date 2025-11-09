#!/bin/bash
################################################################################
# Phase 2 Migration Installation Script
# Installs Chart.js v4 and sets up base_accounting_kit for Odoo 18
#
# Usage: sudo ./install_phase2_migration.sh [options]
#
# Options:
#   --odoo-path PATH    Path to Odoo 18 installation (default: /opt/odoo18)
#   --npm-install       Install Chart.js via npm (instead of using CDN)
#   --test              Run tests after installation
#   --help              Show this help message
################################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ODOO_PATH="/opt/odoo18"
NPM_INSTALL=false
RUN_TESTS=false
BASE_DIR="/home/user/Justo-Works"
MODULE_PATH="$BASE_DIR/addons_custom/base_accounting_kit"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_step() {
    echo -e "${YELLOW}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

show_help() {
    cat << EOF
Phase 2 Migration Installation Script

USAGE:
    sudo ./install_phase2_migration.sh [OPTIONS]

OPTIONS:
    --odoo-path PATH     Path to Odoo 18 installation (default: /opt/odoo18)
    --npm-install        Install Chart.js v4.4.0 via npm (instead of CDN)
    --test               Run test suite after installation
    --help               Show this help message

EXAMPLES:
    # Install using CDN (default)
    sudo ./install_phase2_migration.sh

    # Install Chart.js via npm
    sudo ./install_phase2_migration.sh --npm-install

    # Install and run tests
    sudo ./install_phase2_migration.sh --npm-install --test

    # Specify custom Odoo path
    sudo ./install_phase2_migration.sh --odoo-path /custom/path/odoo18

EOF
    exit 0
}

################################################################################
# Parse Arguments
################################################################################

while [[ $# -gt 0 ]]; do
    case $1 in
        --odoo-path)
            ODOO_PATH="$2"
            shift 2
            ;;
        --npm-install)
            NPM_INSTALL=true
            shift
            ;;
        --test)
            RUN_TESTS=true
            shift
            ;;
        --help)
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

################################################################################
# Checks
################################################################################

check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check if running as root
    print_step "Checking root privileges"
    if [ "$EUID" -ne 0 ]; then
        print_error "Please run as root (use sudo)"
        exit 1
    fi
    print_success "Running as root"

    # Check Python
    print_step "Checking Python 3"
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        print_success "Python 3 found: $python_version"
    else
        print_error "Python 3 not found"
        exit 1
    fi

    # Check Node.js (if npm install requested)
    if [ "$NPM_INSTALL" = true ]; then
        print_step "Checking Node.js and npm"
        if command -v node &> /dev/null && command -v npm &> /dev/null; then
            node_version=$(node --version)
            npm_version=$(npm --version)
            print_success "Node.js found: $node_version"
            print_success "npm found: v$npm_version"
        else
            print_error "Node.js or npm not found (required for --npm-install)"
            print_info "Install with: sudo apt-get install nodejs npm"
            exit 1
        fi
    fi

    # Check module directory
    print_step "Checking module directory"
    if [ -d "$MODULE_PATH" ]; then
        print_success "Module found at $MODULE_PATH"
    else
        print_error "Module not found at $MODULE_PATH"
        exit 1
    fi

    # Check if migration files exist
    print_step "Checking migration files"
    if [ -f "$MODULE_PATH/static/src/js/account_dashboard_owl.js" ]; then
        print_success "OWL component found"
    else
        print_error "OWL component not found (account_dashboard_owl.js)"
        exit 1
    fi

    echo ""
}

################################################################################
# Installation
################################################################################

install_chartjs() {
    print_header "Installing Chart.js v4.4.0"

    if [ "$NPM_INSTALL" = true ]; then
        print_step "Installing Chart.js via npm"

        cd "$BASE_DIR"

        # Initialize package.json if it doesn't exist
        if [ ! -f "package.json" ]; then
            print_info "Creating package.json"
            cat > package.json <<EOF
{
  "name": "justo-works-odoo18",
  "version": "18.0.0",
  "description": "Justo Works Odoo 18 Migration",
  "dependencies": {
    "chart.js": "^4.4.0"
  }
}
EOF
        fi

        # Install Chart.js
        npm install chart.js@4.4.0

        if [ $? -eq 0 ]; then
            chartjs_version=$(node -p "require('./node_modules/chart.js/package.json').version")
            print_success "Chart.js v$chartjs_version installed via npm"

            # Update manifest to use npm version
            print_step "Updating manifest for npm installation"
            sed -i "s|https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js|'base_accounting_kit/static/lib/chart.min.js',  # Chart.js v4 from npm|g" "$MODULE_PATH/__manifest__.py"

            # Create symlink to node_modules
            print_step "Creating symlink to Chart.js"
            ln -sf "$BASE_DIR/node_modules/chart.js/dist/chart.umd.min.js" "$MODULE_PATH/static/lib/chart.min.js"

            print_success "Manifest updated for npm installation"
        else
            print_error "Failed to install Chart.js via npm"
            exit 1
        fi
    else
        print_info "Using Chart.js from CDN (no installation needed)"
        print_info "CDN URL: https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"
    fi

    echo ""
}

verify_installation() {
    print_header "Verifying Installation"

    # Check manifest syntax
    print_step "Validating manifest syntax"
    if python3 -m py_compile "$MODULE_PATH/__manifest__.py" 2>/dev/null; then
        print_success "Manifest syntax is valid"
    else
        print_error "Manifest has syntax errors"
        python3 -m py_compile "$MODULE_PATH/__manifest__.py"
        exit 1
    fi

    # Check JavaScript syntax
    print_step "Validating JavaScript syntax"
    if node -c "$MODULE_PATH/static/src/js/account_dashboard_owl.js" 2>/dev/null; then
        print_success "JavaScript syntax is valid"
    else
        print_error "JavaScript has syntax errors"
        exit 1
    fi

    # Check file structure
    print_step "Checking file structure"
    required_files=(
        "$MODULE_PATH/static/src/js/account_dashboard_owl.js"
        "$MODULE_PATH/__manifest__.py"
        "$BASE_DIR/CHARTJS_OWL_MIGRATION_GUIDE.md"
        "$BASE_DIR/PHASE2_ANALYSIS.md"
    )

    all_found=true
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            print_success "$(basename $file) found"
        else
            print_error "$(basename $file) not found"
            all_found=false
        fi
    done

    if [ "$all_found" = false ]; then
        exit 1
    fi

    echo ""
}

setup_odoo() {
    print_header "Setting up Odoo 18"

    # Check if Odoo path exists
    if [ -d "$ODOO_PATH" ]; then
        print_info "Odoo installation found at $ODOO_PATH"

        # Update addons path if needed
        print_step "Checking Odoo configuration"
        odoo_conf="$ODOO_PATH/odoo.conf"

        if [ -f "/etc/odoo18/odoo18.conf" ]; then
            odoo_conf="/etc/odoo18/odoo18.conf"
        fi

        if [ -f "$odoo_conf" ]; then
            print_info "Odoo config: $odoo_conf"

            # Check if addons_custom is in addons_path
            if grep -q "addons_custom" "$odoo_conf"; then
                print_success "addons_custom already in addons_path"
            else
                print_info "You may need to add addons_custom to addons_path in $odoo_conf"
            fi
        else
            print_info "Odoo config not found at standard location"
        fi
    else
        print_info "Odoo 18 not found at $ODOO_PATH"
        print_info "Migration files ready for Odoo 18 installation"
    fi

    echo ""
}

run_tests() {
    print_header "Running Test Suite"

    if [ -f "$BASE_DIR/test_phase2_migration.sh" ]; then
        print_step "Executing test suite"
        bash "$BASE_DIR/test_phase2_migration.sh"
    else
        print_error "Test script not found"
        exit 1
    fi

    echo ""
}

show_next_steps() {
    print_header "Installation Complete!"

    echo -e "${GREEN}✓ Phase 2 migration files are ready${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "1. ${YELLOW}Update Odoo Database:${NC}"
    echo "   cd $ODOO_PATH"
    echo "   ./odoo-bin -c /etc/odoo18/odoo18.conf -d your_database -u base_accounting_kit --stop-after-init"
    echo ""
    echo "2. ${YELLOW}Restart Odoo:${NC}"
    echo "   sudo systemctl restart odoo18"
    echo ""
    echo "3. ${YELLOW}Test Dashboard:${NC}"
    echo "   - Log in to Odoo 18"
    echo "   - Navigate to Accounting → Dashboard"
    echo "   - Verify charts render correctly"
    echo "   - Test all interactive features"
    echo ""
    echo "4. ${YELLOW}Review Documentation:${NC}"
    echo "   - $BASE_DIR/CHARTJS_OWL_MIGRATION_GUIDE.md"
    echo "   - $BASE_DIR/PHASE2_ANALYSIS.md"
    echo ""
    echo "5. ${YELLOW}Complete Migration:${NC}"
    echo "   - Migrate payment widgets (payment_model.js, payment_render.js, payment_matching.js)"
    echo "   - Migrate account_asset.js"
    echo "   - Update QWeb templates if needed"
    echo "   - Complete TODO items in account_dashboard_owl.js"
    echo ""

    if [ "$NPM_INSTALL" = true ]; then
        echo -e "${YELLOW}Note:${NC} Chart.js installed via npm. Remember to run 'npm install' on deployment."
    else
        echo -e "${YELLOW}Note:${NC} Chart.js loaded from CDN. Requires internet connection."
    fi

    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  Installation successful! Ready for Odoo 18 testing.          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

################################################################################
# Main
################################################################################

main() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║    Phase 2 Migration Installer                                ║"
    echo "║    Chart.js v4 + OWL for base_accounting_kit                  ║"
    echo "║    Odoo 15 → Odoo 18 Migration                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""

    check_prerequisites
    install_chartjs
    verify_installation
    setup_odoo

    if [ "$RUN_TESTS" = true ]; then
        run_tests
    fi

    show_next_steps
}

# Run main function
main

exit 0
