#!/bin/bash
################################################################################
# Phase 2 Migration Test Script
# Tests base_accounting_kit Chart.js v4 + OWL migration
#
# Usage: ./test_phase2_migration.sh [test_name]
#   test_name: specific test to run (optional, runs all if not specified)
#
# Available tests:
#   - files: Check file structure
#   - manifest: Validate manifest syntax
#   - javascript: Check JavaScript syntax
#   - dependencies: Verify dependencies
#   - all: Run all tests (default)
################################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_WARNINGS=0

# Base directory
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

print_test() {
    echo -e "${YELLOW}▶ Testing:${NC} $1"
}

print_pass() {
    echo -e "${GREEN}✓ PASS:${NC} $1"
    ((TESTS_PASSED++))
}

print_fail() {
    echo -e "${RED}✗ FAIL:${NC} $1"
    ((TESTS_FAILED++))
}

print_warn() {
    echo -e "${YELLOW}⚠ WARNING:${NC} $1"
    ((TESTS_WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ INFO:${NC} $1"
}

################################################################################
# Test Functions
################################################################################

test_file_structure() {
    print_header "TEST 1: File Structure"

    # Check if module exists
    print_test "Module directory exists"
    if [ -d "$MODULE_PATH" ]; then
        print_pass "Module found at $MODULE_PATH"
    else
        print_fail "Module not found at $MODULE_PATH"
        return 1
    fi

    # Check new OWL file
    print_test "OWL dashboard component exists"
    if [ -f "$MODULE_PATH/static/src/js/account_dashboard_owl.js" ]; then
        print_pass "account_dashboard_owl.js found"
    else
        print_fail "account_dashboard_owl.js not found"
    fi

    # Check backup directory
    print_test "Backup directory exists"
    if [ -d "$MODULE_PATH/.backup_v15_libs" ]; then
        print_pass "Backup directory found"
        backup_count=$(ls -1 "$MODULE_PATH/.backup_v15_libs" | wc -l)
        print_info "Backup contains $backup_count files"
    else
        print_warn "Backup directory not found (may not be created yet)"
    fi

    # Check old Chart.js files removed
    print_test "Old Chart.js v2.8 files removed"
    if [ -f "$MODULE_PATH/static/lib/Chart.js" ]; then
        print_fail "Old Chart.js still present in static/lib/"
    else
        print_pass "Old Chart.js files removed"
    fi

    # Check FusionCharts files removed
    print_test "FusionCharts files removed"
    if [ -f "$MODULE_PATH/static/lib/fusioncharts.js" ]; then
        print_fail "FusionCharts still present in static/lib/"
    else
        print_pass "FusionCharts files removed"
    fi

    # Check original dashboard backup
    print_test "Original dashboard backed up"
    if [ -f "$MODULE_PATH/static/src/js/account_dashboard.js.v15.bak" ]; then
        print_pass "Original dashboard backed up"
    else
        print_warn "Original dashboard not backed up"
    fi

    echo ""
}

test_manifest_syntax() {
    print_header "TEST 2: Manifest Validation"

    print_test "Manifest file exists"
    if [ ! -f "$MODULE_PATH/__manifest__.py" ]; then
        print_fail "Manifest file not found"
        return 1
    fi
    print_pass "Manifest file found"

    print_test "Manifest Python syntax"
    if python3 -m py_compile "$MODULE_PATH/__manifest__.py" 2>/dev/null; then
        print_pass "Manifest syntax is valid"
    else
        print_fail "Manifest has syntax errors"
        python3 -m py_compile "$MODULE_PATH/__manifest__.py"
    fi

    print_test "Chart.js v4 CDN link present"
    if grep -q "chart.js@4" "$MODULE_PATH/__manifest__.py"; then
        print_pass "Chart.js v4 CDN link found in manifest"
    else
        print_warn "Chart.js v4 CDN link not found (may use npm install instead)"
    fi

    print_test "Old Chart.js references removed"
    if grep -q "Chart.bundle.js\|Chart.min.js" "$MODULE_PATH/__manifest__.py"; then
        print_fail "Old Chart.js references still in manifest"
    else
        print_pass "Old Chart.js references removed from manifest"
    fi

    print_test "OWL component referenced in manifest"
    if grep -q "account_dashboard_owl.js" "$MODULE_PATH/__manifest__.py"; then
        print_pass "OWL component referenced in manifest"
    else
        print_warn "OWL component not referenced in manifest"
    fi

    echo ""
}

test_javascript_syntax() {
    print_header "TEST 3: JavaScript Syntax"

    print_test "OWL component JavaScript syntax"
    owl_file="$MODULE_PATH/static/src/js/account_dashboard_owl.js"

    if [ ! -f "$owl_file" ]; then
        print_fail "OWL component file not found"
        return 1
    fi

    # Check for basic syntax issues
    if node -c "$owl_file" 2>/dev/null; then
        print_pass "JavaScript syntax is valid"
    else
        # If node is not available, do basic checks
        print_info "Node.js not available, performing basic checks"

        # Check for @odoo-module annotation
        if grep -q "@odoo-module" "$owl_file"; then
            print_pass "@odoo-module annotation found"
        else
            print_fail "@odoo-module annotation missing"
        fi

        # Check for OWL imports
        if grep -q "import.*@odoo/owl" "$owl_file"; then
            print_pass "OWL imports found"
        else
            print_fail "OWL imports missing"
        fi

        # Check for Component class
        if grep -q "class.*Component" "$owl_file"; then
            print_pass "Component class defined"
        else
            print_fail "Component class not found"
        fi

        # Check for registry add
        if grep -q "registry.category.*add.*invoice_dashboard" "$owl_file"; then
            print_pass "Component registered in action registry"
        else
            print_fail "Component not registered"
        fi
    fi

    print_test "Chart.js v4 syntax patterns"
    if grep -q "new Chart(" "$owl_file"; then
        print_pass "Chart.js instantiation found"
    else
        print_warn "Chart.js instantiation not found"
    fi

    if grep -q "plugins:" "$owl_file"; then
        print_pass "Chart.js v4 plugins configuration found"
    else
        print_warn "Chart.js v4 plugins configuration not found"
    fi

    echo ""
}

test_dependencies() {
    print_header "TEST 4: Dependencies Check"

    print_test "Python dependencies"
    if python3 --version >/dev/null 2>&1; then
        python_version=$(python3 --version)
        print_pass "Python 3 available: $python_version"
    else
        print_fail "Python 3 not available"
    fi

    print_test "Node.js (for Chart.js)"
    if node --version >/dev/null 2>&1; then
        node_version=$(node --version)
        print_pass "Node.js available: $node_version"
    else
        print_warn "Node.js not available (optional, for npm install)"
    fi

    print_test "Chart.js installation"
    if [ -d "$BASE_DIR/node_modules/chart.js" ]; then
        chartjs_version=$(node -p "require('$BASE_DIR/node_modules/chart.js/package.json').version" 2>/dev/null)
        if [ ! -z "$chartjs_version" ]; then
            print_pass "Chart.js installed via npm: v$chartjs_version"

            # Check if it's v4
            if [[ "$chartjs_version" == 4.* ]]; then
                print_pass "Chart.js v4.x detected"
            else
                print_warn "Chart.js version is not v4.x: v$chartjs_version"
            fi
        fi
    else
        print_info "Chart.js not installed via npm (using CDN in manifest)"
    fi

    print_test "Odoo manifest dependencies"
    required_deps=("base" "account" "sale" "account_check_printing" "base_account_budget")
    for dep in "${required_deps[@]}"; do
        if grep -q "'$dep'" "$MODULE_PATH/__manifest__.py"; then
            print_pass "Dependency declared: $dep"
        else
            print_warn "Dependency not declared: $dep"
        fi
    done

    echo ""
}

test_code_quality() {
    print_header "TEST 5: Code Quality Checks"

    print_test "OWL file line count"
    if [ -f "$MODULE_PATH/static/src/js/account_dashboard_owl.js" ]; then
        line_count=$(wc -l < "$MODULE_PATH/static/src/js/account_dashboard_owl.js")
        print_info "OWL component: $line_count lines"

        if [ "$line_count" -lt 2000 ]; then
            print_pass "Component size is reasonable (< 2000 lines)"
        else
            print_warn "Component is large ($line_count lines), consider splitting"
        fi
    fi

    print_test "No TODO comments in critical sections"
    todo_count=$(grep -c "TODO" "$MODULE_PATH/static/src/js/account_dashboard_owl.js" 2>/dev/null || echo "0")
    if [ "$todo_count" -eq 0 ]; then
        print_pass "No TODO comments found"
    else
        print_warn "$todo_count TODO comments found (migration incomplete)"
    fi

    print_test "jQuery usage in OWL component"
    jquery_usage=$(grep -c "\$(" "$MODULE_PATH/static/src/js/account_dashboard_owl.js" 2>/dev/null || echo "0")
    if [ "$jquery_usage" -eq 0 ]; then
        print_pass "No jQuery usage detected (pure OWL)"
    else
        print_warn "$jquery_usage jQuery usages found (should convert to OWL patterns)"
    fi

    echo ""
}

test_migration_completeness() {
    print_header "TEST 6: Migration Completeness"

    print_test "Chart types migrated"
    chart_types=("bar" "doughnut" "line")
    for chart_type in "${chart_types[@]}"; do
        if grep -q "type: '$chart_type'" "$MODULE_PATH/static/src/js/account_dashboard_owl.js"; then
            print_pass "Chart type supported: $chart_type"
        else
            print_warn "Chart type not found: $chart_type"
        fi
    done

    print_test "ORM service usage"
    if grep -q "this.orm.call" "$MODULE_PATH/static/src/js/account_dashboard_owl.js"; then
        print_pass "ORM service used for RPC calls"
    else
        print_warn "ORM service not used (old rpc.query pattern?)"
    fi

    print_test "Action service usage"
    if grep -q "this.action.doAction" "$MODULE_PATH/static/src/js/account_dashboard_owl.js"; then
        print_pass "Action service used for navigation"
    else
        print_warn "Action service not used"
    fi

    print_test "Reactive state usage"
    if grep -q "useState" "$MODULE_PATH/static/src/js/account_dashboard_owl.js"; then
        print_pass "Reactive state (useState) implemented"
    else
        print_warn "Reactive state not implemented (jQuery DOM?)"
    fi

    print_test "Chart lifecycle management"
    if grep -q "destroy()" "$MODULE_PATH/static/src/js/account_dashboard_owl.js"; then
        print_pass "Chart cleanup implemented"
    else
        print_warn "Chart cleanup (destroy) not implemented"
    fi

    echo ""
}

test_documentation() {
    print_header "TEST 7: Documentation"

    print_test "Migration guide exists"
    if [ -f "$BASE_DIR/CHARTJS_OWL_MIGRATION_GUIDE.md" ]; then
        guide_size=$(wc -l < "$BASE_DIR/CHARTJS_OWL_MIGRATION_GUIDE.md")
        print_pass "Migration guide found ($guide_size lines)"
    else
        print_fail "Migration guide not found"
    fi

    print_test "Phase 2 analysis exists"
    if [ -f "$BASE_DIR/PHASE2_ANALYSIS.md" ]; then
        analysis_size=$(wc -l < "$BASE_DIR/PHASE2_ANALYSIS.md")
        print_pass "Phase 2 analysis found ($analysis_size lines)"
    else
        print_fail "Phase 2 analysis not found"
    fi

    print_test "README or installation instructions"
    readme_files=("$BASE_DIR/README.md" "$MODULE_PATH/README.rst" "$MODULE_PATH/README.md")
    readme_found=false
    for readme in "${readme_files[@]}"; do
        if [ -f "$readme" ]; then
            print_pass "Documentation found: $(basename $readme)"
            readme_found=true
            break
        fi
    done

    if [ "$readme_found" = false ]; then
        print_warn "No README file found"
    fi

    echo ""
}

################################################################################
# Main Test Runner
################################################################################

run_all_tests() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         Phase 2 Migration Test Suite                          ║"
    echo "║         Chart.js v4 + OWL Migration for base_accounting_kit   ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""

    test_file_structure
    test_manifest_syntax
    test_javascript_syntax
    test_dependencies
    test_code_quality
    test_migration_completeness
    test_documentation

    # Summary
    print_header "TEST SUMMARY"
    echo -e "${GREEN}✓ Passed:  $TESTS_PASSED${NC}"
    echo -e "${RED}✗ Failed:  $TESTS_FAILED${NC}"
    echo -e "${YELLOW}⚠ Warnings: $TESTS_WARNINGS${NC}"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  ✓ ALL TESTS PASSED                                            ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"

        if [ $TESTS_WARNINGS -gt 0 ]; then
            echo -e "${YELLOW}Note: $TESTS_WARNINGS warning(s) found. Review before production.${NC}"
        fi

        return 0
    else
        echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  ✗ SOME TESTS FAILED                                           ║${NC}"
        echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
        return 1
    fi
}

################################################################################
# Script Entry Point
################################################################################

# Check if specific test requested
if [ $# -eq 0 ]; then
    run_all_tests
else
    case "$1" in
        files)
            test_file_structure
            ;;
        manifest)
            test_manifest_syntax
            ;;
        javascript)
            test_javascript_syntax
            ;;
        dependencies)
            test_dependencies
            ;;
        quality)
            test_code_quality
            ;;
        completeness)
            test_migration_completeness
            ;;
        documentation)
            test_documentation
            ;;
        all)
            run_all_tests
            ;;
        *)
            echo "Unknown test: $1"
            echo "Available tests: files, manifest, javascript, dependencies, quality, completeness, documentation, all"
            exit 1
            ;;
    esac
fi

exit $?
