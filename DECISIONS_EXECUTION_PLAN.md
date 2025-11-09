# Decision Execution Plan - Odoo 18 Migration
**Date:** 2025-11-09
**Status:** ✅ Decisions Approved, Ready for Execution
**Branch:** `claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx`

---

## 📋 Executive Summary

This document provides actionable execution plans for the three critical decisions made for the Odoo 15 to Odoo 18 migration project.

### Decisions Approved

✅ **Decision 1:** Replace Highcharts/FusionCharts with ApexCharts + Chart.js (Option B)
✅ **Decision 2:** Enable Google Maps API billing
⏱️ **Decision 3:** Acquire 19 missing external modules (strategy required)

### Financial Impact
- **Cost Savings:** $5,747 over 5 years (charting libraries)
- **New Costs:** $600/year (Google Maps - estimated medium usage)
- **One-time Dev Cost:** $4,000 (charting library replacement)
- **Timeline Impact:** +8 days to migration schedule

---

## 🎯 DECISION 1: Replace Charting Libraries (APPROVED)

### Decision Summary
**Approved Option:** Option B - Replace with free alternatives
**Rationale:** Save $5,747 over 5 years, eliminate license compliance risk, better OWL compatibility

### What's Being Replaced

| Current Library | Modules Affected | New Library | Effort |
|----------------|------------------|-------------|--------|
| **Highcharts** (unlicensed) | jupiter_dashboard_optima, jupiter_dashboard_tres | **ApexCharts** (MIT) | 3-4 days |
| **FusionCharts** (unclear license) | base_accounting_kit | **Chart.js v4** (MIT) | 2-3 days |

### Cost Analysis

**Current Situation (if purchased):**
- Highcharts: $1,750/year (5 developers)
- FusionCharts: $997 one-time
- **5-year total:** $12,747

**With Replacement (approved):**
- ApexCharts: $0 (MIT license)
- Chart.js v4: $0 (MIT license)
- Development: $4,000 one-time
- **5-year total:** $4,000
- **Savings:** $8,747

---

## 📅 Execution Timeline - Decision 1

### Phase 2 Week 2: Charting Library Replacement (8 days added)

#### Day 1-2: ApexCharts Migration Prep (16h)

**Morning Day 1 (4h):**
- [ ] **Study ApexCharts documentation**
  - Read: https://apexcharts.com/docs/
  - Review examples: https://apexcharts.com/javascript-chart-demos/
  - Study OWL integration patterns

- [ ] **Analyze current Highcharts usage**
  ```bash
  # Find all Highcharts references
  cd /home/user/Justo-Works
  grep -r "Highcharts" addons_custom/jupiter_dashboard_*/

  # Identify chart types used
  grep -A 10 "Highcharts.chart" addons_custom/jupiter_dashboard_*/static/src/js/*.js
  ```

- [ ] **Create migration templates**
  - Document chart type mappings (see below)
  - Create ApexCharts wrapper for OWL
  - Prepare test data

**Afternoon Day 1 (4h):**
- [ ] **Setup development environment**
  ```bash
  # Download ApexCharts
  cd addons_custom/jupiter_dashboard_tres/static/src/js/
  wget https://cdn.jsdelivr.net/npm/apexcharts@latest/dist/apexcharts.min.js
  ```

- [ ] **Create migration branch** (optional)
  ```bash
  git checkout -b feature/replace-highcharts-with-apexcharts
  ```

- [ ] **Backup current implementations**
  ```bash
  cp addons_custom/jupiter_dashboard_tres/static/src/js/dashboard.js \
     addons_custom/jupiter_dashboard_tres/static/src/js/dashboard.js.highcharts.backup
  ```

**Day 2 (8h):**
- [ ] **Migrate jupiter_dashboard_tres** (First module)
  - Replace Highcharts library with ApexCharts
  - Update chart initialization code
  - Update data format
  - Test all chart types

- [ ] **Test jupiter_dashboard_tres thoroughly**
  - Verify charts render
  - Test data updates
  - Check responsive behavior
  - Validate exports

#### Day 3-4: ApexCharts Migration Execution (16h)

- [ ] **Migrate jupiter_dashboard_optima** (8h)
  - Apply pattern from jupiter_dashboard_tres
  - Update dashboard configuration
  - Test with live data
  - Verify all chart widgets

- [ ] **Integration testing** (4h)
  - Test both modules together
  - Verify dashboard settings persistence
  - Check performance
  - Browser compatibility testing

- [ ] **Documentation** (2h)
  - Update module READMEs
  - Document ApexCharts API usage
  - Create upgrade notes

- [ ] **Commit changes** (2h)
  ```bash
  git add addons_custom/jupiter_dashboard_tres/
  git add addons_custom/jupiter_dashboard_optima/
  git commit -m "Replace Highcharts with ApexCharts in Jupiter dashboards

  - Migrated jupiter_dashboard_tres to ApexCharts (MIT license)
  - Migrated jupiter_dashboard_optima to ApexCharts (MIT license)
  - Removed commercial Highcharts dependency
  - Saves $1,750/year in licensing costs
  - Better OWL compatibility for Odoo 18

  Chart types migrated:
  - Column charts
  - Line charts
  - Pie charts
  - Area charts

  Tested: All chart rendering, data updates, exports
  "
  ```

#### Day 5-6: Chart.js v4 Migration (16h)

**Day 5 (8h):**
- [ ] **Analyze base_accounting_kit charting**
  ```bash
  # Find Chart.js usage
  grep -r "Chart(" addons_custom/base_accounting_kit/static/

  # Find FusionCharts usage
  grep -r "FusionCharts" addons_custom/base_accounting_kit/static/
  ```

- [ ] **Upgrade Chart.js v2.9 → v4.4**
  ```bash
  cd addons_custom/base_accounting_kit/static/lib/

  # Backup old version
  mv Chart.js Chart.js.v2.9.backup
  mv Chart.min.js Chart.min.js.v2.9.backup

  # Download Chart.js v4.4
  wget https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js -O Chart.min.js
  ```

- [ ] **Update Chart.js v2 code to v4 syntax**
  - Change: `new Chart(ctx, {...})` to Chart.js v4 syntax
  - Update plugin registration
  - Update options structure
  - Test existing Chart.js charts

**Day 6 (8h):**
- [ ] **Replace FusionCharts with Chart.js v4**
  - Identify FusionCharts chart types
  - Create equivalent Chart.js v4 charts
  - Update dashboard.js code
  - Remove FusionCharts library

- [ ] **Remove FusionCharts completely**
  ```bash
  # Remove FusionCharts files
  rm addons_custom/base_accounting_kit/static/lib/fusioncharts.js
  rm addons_custom/base_accounting_kit/static/lib/fusioncharts.charts.js

  # Update manifest.py to remove FusionCharts assets
  ```

- [ ] **Update manifest.py**
  ```python
  # Remove FusionCharts references
  # Add Chart.js v4 reference
  'assets': {
      'web.assets_backend': [
          'base_accounting_kit/static/lib/Chart.min.js',
          # Remove: fusioncharts references
      ],
  }
  ```

#### Day 7-8: Testing & Documentation (16h)

**Day 7 (8h):**
- [ ] **Comprehensive testing**
  - Test all accounting dashboards
  - Verify chart interactions
  - Test data filtering
  - Check mobile responsiveness
  - Browser compatibility (Chrome, Firefox, Safari)

- [ ] **Performance testing**
  - Compare render times
  - Test with large datasets
  - Memory usage monitoring

- [ ] **User acceptance testing preparation**
  - Create test scenarios
  - Document expected behaviors
  - Prepare demo data

**Day 8 (8h):**
- [ ] **Documentation updates**
  - Update LICENSE_DECISION_SUMMARY.md
  - Create CHARTING_LIBRARY_MIGRATION.md
  - Update module READMEs
  - Document API changes

- [ ] **Create migration report**
  - Document charts migrated
  - Performance comparisons
  - Feature parity validation
  - Known issues/limitations

- [ ] **Final commit**
  ```bash
  git add addons_custom/base_accounting_kit/
  git commit -m "Replace FusionCharts with Chart.js v4 and upgrade Chart.js v2.9

  - Upgraded Chart.js from v2.9 to v4.4 (latest)
  - Replaced FusionCharts with Chart.js v4
  - Removed FusionCharts library (unclear license)
  - Saves $997 one-time licensing cost
  - All charts now use free MIT-licensed libraries

  Charts migrated:
  - Accounting dashboard charts
  - Financial report visualizations
  - Asset management charts

  Tested: Dashboard rendering, data updates, exports, mobile view
  "

  git push origin claude/review-justo-works-setup-011CUwnFauUo7h1dU7TKrvkx
  ```

---

## 🗺️ DECISION 2: Google Maps API Setup (APPROVED)

### Decision Summary
**Approved:** Enable Google Maps API billing
**Rationale:** Essential for real estate business, no viable free alternative

### Current Status
- **Module:** itsys_real_estate
- **APIs Used:** Maps JavaScript API, Places API, Geocoding API
- **Current Key:** Stored in `ir.config_parameter` as 'google_maps_api_key'
- **Billing:** ⚠️ NOT ENABLED (needs activation)

### Cost Structure
- **Free Credit:** $200/month
- **Estimated Usage (Medium):** $0-$600/year
- **Alert Threshold:** $100/month (recommended)

---

## 📋 Execution Steps - Decision 2

### Step 1: Enable Google Cloud Billing (1 hour)

- [ ] **Go to Google Cloud Console**
  - URL: https://console.cloud.google.com/

- [ ] **Select or Create Project**
  ```
  Project Name: Justo-Works-Odoo18
  Project ID: justo-works-odoo18-[unique-id]
  ```

- [ ] **Enable Billing Account**
  - Navigate to: Billing → Link a billing account
  - Add payment method (credit card required)
  - ⚠️ You will NOT be charged without your permission (free tier applies first)

### Step 2: Enable Required APIs (30 minutes)

- [ ] **Enable APIs**
  - Navigate to: APIs & Services → Library
  - Enable:
    1. Maps JavaScript API
    2. Places API
    3. Geocoding API

### Step 3: Create and Secure API Key (30 minutes)

- [ ] **Create API Key**
  - Navigate to: APIs & Services → Credentials
  - Click: Create Credentials → API Key
  - Copy the API key (save securely)

- [ ] **Restrict API Key (CRITICAL for security)**
  ```
  Application restrictions:
  - HTTP referrers (websites)
  - Add your domain: https://your-odoo-domain.com/*

  API restrictions:
  - Restrict key to specific APIs:
    ✓ Maps JavaScript API
    ✓ Places API
    ✓ Geocoding API
  ```

### Step 4: Set Usage Quotas and Alerts (30 minutes)

- [ ] **Set Billing Alerts**
  - Navigate to: Billing → Budgets & alerts
  - Create budget alert: $100/month
  - Email notifications to: your-email@company.com

- [ ] **Set API Quotas** (Optional but recommended)
  ```
  Maps JavaScript API: 25,000 loads/day
  Places API: 10,000 requests/day
  Geocoding API: 5,000 requests/day
  ```

### Step 5: Update Odoo Configuration (15 minutes)

- [ ] **Update API key in Odoo**
  ```python
  # After Odoo 18 is running:
  # Settings → Technical → Parameters → System Parameters
  # Key: google_maps_api_key
  # Value: [YOUR_NEW_API_KEY]
  ```

- [ ] **Test in itsys_real_estate module**
  - Create test property
  - Test map widget
  - Test place autocomplete
  - Verify geocoding works

### Step 6: Optimize Usage (Ongoing)

- [ ] **Implement caching**
  - Cache geocoding results in database
  - Avoid redundant API calls

- [ ] **Load maps on demand**
  ```javascript
  // Don't load map on page load
  // Load only when user clicks "View Map" button
  ```

- [ ] **Monitor usage monthly**
  - Check Google Cloud Console monthly
  - Review API usage reports
  - Adjust alerts if needed

---

## ⚠️ DECISION 3: External Module Dependencies (CRITICAL)

### Problem Summary
**19 external modules** are required but NOT in repository. Migration will **FAIL** without these.

### Critical Missing Modules

| Module | Used By | Priority | Source |
|--------|---------|----------|--------|
| **purchase_extension** | jupiter_accounts, real_estate_extension | 🔴 CRITICAL | Unknown |
| **inexoft_account_voucher** | real_estate_extension | 🔴 CRITICAL | Inexoft Technologies |
| **inexoft_account_payments** | real_estate_extension | 🔴 CRITICAL | Inexoft Technologies |
| account_vouchers | real_estate_extension | 🔴 CRITICAL | Unknown |
| bank_reconciliation | real_estate_extension | 🟡 HIGH | May be in Odoo 18 |
| cash_book | real_estate_extension | 🟡 HIGH | Part of accounting suite |
| day_book | real_estate_extension | 🟡 HIGH | Part of accounting suite |
| general_ledger | real_estate_extension | 🟡 HIGH | Part of accounting suite |
| trial_balance | real_estate_extension | 🟡 HIGH | Part of accounting suite |
| manufacturing_trading | real_estate_extension | 🟢 MEDIUM | Reporting module |
| profit_loss_balance_sheet | real_estate_extension | 🟢 MEDIUM | Reporting module |
| purchase_detail | real_estate_extension | 🟢 MEDIUM | Unknown |

---

## 📋 Execution Strategy - Decision 3

### Strategy 1: Locate and Acquire Modules (Week 1-2)

#### Step 1: Contact Inexoft Technologies (Day 1)

- [ ] **Contact Inexoft Technologies**
  - Website: https://www.inexoft.com/
  - Email: info@inexoft.com / sales@inexoft.com
  - Phone: +1 (647) 948-8638 (from website, verify)

- [ ] **Email Template:**
  ```
  Subject: Odoo 18 Migration - Requesting Updated Modules

  Dear Inexoft Technologies Team,

  We are currently migrating our Odoo system from version 15 to version 18.
  Our system currently uses the following Inexoft modules:

  1. inexoft_account_voucher
  2. inexoft_account_payments

  We would like to:
  1. Confirm if Odoo 18 versions of these modules are available
  2. Understand the licensing terms and pricing
  3. Obtain upgrade path and migration assistance if available

  Our system details:
  - Current: Odoo 15
  - Target: Odoo 18
  - Platform: Ubuntu ARM64
  - Business: Real Estate Management

  Could you please provide:
  - Module availability for Odoo 18
  - Pricing information
  - Technical support options
  - Estimated delivery timeline

  Thank you for your assistance.

  Best regards,
  [Your Name]
  [Company Name]
  [Contact Information]
  ```

- [ ] **Follow-up timeline**
  - Send email: Day 1
  - Follow-up call: Day 3 (if no response)
  - Alternative search: Day 5

#### Step 2: Search Odoo App Store (Day 1-2)

- [ ] **Search for modules on Odoo Apps**
  - URL: https://apps.odoo.com/apps/modules/18.0/

  Search for:
  - [ ] purchase_extension
  - [ ] account_vouchers
  - [ ] bank_reconciliation
  - [ ] cash_book, day_book, general_ledger, trial_balance
  - [ ] manufacturing_trading
  - [ ] profit_loss_balance_sheet
  - [ ] purchase_detail

- [ ] **Check OCA (Odoo Community Association)**
  - URL: https://github.com/OCA/
  - Search repositories for similar functionality:
    - purchase modules: https://github.com/OCA/purchase-workflow
    - account modules: https://github.com/OCA/account-financial-reporting
    - reporting: https://github.com/OCA/reporting-engine

#### Step 3: Contact Original Vendor/Developer (Day 2-3)

- [ ] **Check module metadata for vendor**
  ```bash
  # Check manifest files for author/vendor info
  grep -r "author" addons_custom/real_estate_extension/__manifest__.py
  grep -r "author" addons_custom/jupiter_accounts/__manifest__.py
  ```

- [ ] **Search for vendor websites**
  - Google search: "[module_name] Odoo"
  - Check Odoo partners directory
  - LinkedIn search for developers

#### Step 4: Community Search (Day 3-4)

- [ ] **Post on Odoo forums**
  - Forum: https://www.odoo.com/forum
  - Reddit: r/Odoo
  - LinkedIn Odoo groups

- [ ] **Forum post template:**
  ```
  Subject: Looking for Odoo 18 versions of accounting modules

  I'm migrating from Odoo 15 to 18 and looking for these modules:
  - purchase_extension
  - cash_book, day_book, general_ledger, trial_balance
  - manufacturing_trading, profit_loss_balance_sheet

  Has anyone used these modules or know where to find Odoo 18 versions?
  Willing to pay for commercial modules if available.

  Platform: Ubuntu ARM64
  ```

---

### Strategy 2: Alternative Solutions (Week 2-3)

If modules cannot be found, consider these alternatives:

#### Option A: Use Odoo 18 Built-in Features

Many features may now be in Odoo 18 core:

- [ ] **Check Odoo 18 accounting features**
  - Bank reconciliation: May be built-in
  - General ledger: Built into accounting module
  - Trial balance: Standard report in accounting

- [ ] **Review Odoo 18 documentation**
  - URL: https://www.odoo.com/documentation/18.0/
  - Compare features with missing modules

#### Option B: Find Equivalent Modules

- [ ] **Search for equivalent functionality**
  - Example: "purchase_extension" → Search for "purchase workflow" modules
  - Example: "day_book" → Search for "daily reports" modules

#### Option C: Custom Development

If no alternatives exist:

- [ ] **Analyze missing module functionality**
  ```bash
  # If you have access to old Odoo 15 system with these modules
  # Export module code and analyze features
  ```

- [ ] **Estimate custom development effort**
  - Per module: 40-80 hours
  - Total for all missing: 200-400 hours
  - Cost: $10,000-$20,000

- [ ] **Prioritize critical modules first**
  1. purchase_extension (used by 2 modules)
  2. inexoft_account_voucher (critical for real_estate_extension)
  3. inexoft_account_payments (critical for real_estate_extension)

#### Option D: Modify Dependencies

**Last resort:** Remove dependencies from modules

- [ ] **Analyze real_estate_extension dependencies**
  ```python
  # In addons_custom/real_estate_extension/__manifest__.py
  # Remove non-critical dependencies
  'depends': [
      'base',
      'base_accounting_kit',
      'itsys_real_estate',
      # Comment out unavailable modules
      # 'inexoft_account_voucher',  # Find alternative
      # 'purchase_extension',       # Find alternative
  ]
  ```

- [ ] **Refactor code to remove dependencies**
  - Comment out imports from missing modules
  - Implement minimal functionality locally
  - Test thoroughly

---

### Strategy 3: Staged Migration (Fallback Plan)

If modules can't be acquired quickly:

#### Option: Migrate to Odoo 17 First

- **Rationale:** Easier to find Odoo 17 modules than Odoo 18
- **Timeline:** 2 weeks Odoo 15→17, then 2 weeks Odoo 17→18
- **Benefit:** Less breaking changes, more time for module hunting

---

## 📊 Updated Migration Timeline

### Original Timeline (without charting library replacement)
- **Phase 2 Module Migration:** 3-4 weeks (280-350 hours)

### New Timeline (with approved decisions)
- **Phase 2 Week 1:** Foundation + Simple modules (40 hours)
- **Phase 2 Week 2:** Charting library replacement (64 hours) ⚠️ +8 days
- **Phase 2 Week 3:** JavaScript OWL migration (40 hours)
- **Phase 2 Week 4:** Complex modules (40 hours)
- **Phase 2 Week 5:** Integration testing (40 hours)

**Total: 4-5 weeks** (was 3-4 weeks)

---

## ✅ Success Criteria

### Decision 1: Charting Libraries
- [ ] Highcharts completely removed from both dashboard modules
- [ ] ApexCharts successfully integrated and working
- [ ] FusionCharts completely removed from accounting kit
- [ ] Chart.js v4 successfully integrated and working
- [ ] All charts render correctly
- [ ] No license compliance issues
- [ ] Performance equal or better than before

### Decision 2: Google Maps
- [ ] Billing account enabled
- [ ] API key created and secured
- [ ] Usage alerts configured
- [ ] API key updated in Odoo
- [ ] Map widgets working in itsys_real_estate
- [ ] Monthly cost within budget ($0-$100/month initially)

### Decision 3: External Modules
- [ ] All 19 missing modules located OR alternatives found
- [ ] Inexoft modules acquired/replaced
- [ ] purchase_extension acquired/replaced
- [ ] All reporting modules acquired/replaced
- [ ] Dependencies resolved for real_estate_extension
- [ ] Dependencies resolved for jupiter_accounts
- [ ] Migration can proceed without blockers

---

## 🚨 Risk Mitigation

### High Risk Items

**Risk 1: Cannot find external modules**
- **Impact:** Migration blocked
- **Mitigation:**
  - Start searching immediately (Week 1)
  - Have custom development budget ready
  - Consider Odoo 17 intermediate step

**Risk 2: Charting migration breaks dashboards**
- **Impact:** Business intelligence unavailable
- **Mitigation:**
  - Keep backup of Highcharts code
  - Test extensively before removing old code
  - Have rollback plan

**Risk 3: Google Maps costs exceed budget**
- **Impact:** Unexpected monthly costs
- **Mitigation:**
  - Set strict $100/month alert
  - Implement caching aggressively
  - Monitor usage weekly initially

---

## 📞 Next Steps - Priority Order

### Immediate (This Week)

1. **Day 1: External Module Search**
   - [ ] Email Inexoft Technologies
   - [ ] Search Odoo App Store
   - [ ] Post on forums

2. **Day 1: Google Maps Setup**
   - [ ] Enable Google Cloud billing
   - [ ] Create and restrict API key
   - [ ] Set up usage alerts

3. **Day 2-3: External Module Analysis**
   - [ ] Analyze dependencies in detail
   - [ ] Create fallback plans
   - [ ] Estimate custom development if needed

### Week 2: Begin Charting Migration

4. **Day 1-2: Preparation**
   - [ ] Study ApexCharts documentation
   - [ ] Analyze current Highcharts usage
   - [ ] Create migration templates

5. **Day 3-8: Execution**
   - [ ] Migrate jupiter_dashboard_tres
   - [ ] Migrate jupiter_dashboard_optima
   - [ ] Upgrade Chart.js and replace FusionCharts
   - [ ] Test thoroughly

### Week 3: Phase 1 Execution (If Ready)

6. **Execute Odoo 18 Setup**
   - [ ] Run setup_odoo18_ubuntu.sh
   - [ ] Verify 7 automated tests pass
   - [ ] Test web interface

---

## 📄 Deliverables

### Documentation Created
- [x] DECISIONS_EXECUTION_PLAN.md (this file)
- [ ] CHARTING_LIBRARY_MIGRATION_GUIDE.md (to be created)
- [ ] EXTERNAL_MODULES_SEARCH_LOG.md (to be created)
- [ ] GOOGLE_MAPS_SETUP_COMPLETE.md (to be created after setup)

### Code Changes
- [ ] ApexCharts integration
- [ ] Chart.js v4 upgrade
- [ ] Highcharts removal
- [ ] FusionCharts removal
- [ ] Google Maps API key update

### Testing Reports
- [ ] Charting library migration test report
- [ ] Performance comparison report
- [ ] External modules availability report

---

## 📅 Review Schedule

- **Week 1 Review:** External module search progress
- **Week 2 Review:** Charting migration completion
- **Week 3 Review:** Phase 1 execution readiness
- **Week 4 Review:** Overall progress assessment

---

**Status:** ✅ Ready to execute
**Blocked By:** External module dependencies (Decision 3)
**Can Proceed:** Decisions 1 & 2 (charting + Google Maps)

**Recommendation:** Start with Decision 1 (charting) and Decision 2 (Google Maps) immediately while resolving Decision 3 (external modules) in parallel.

---

**Last Updated:** 2025-11-09
**Next Review:** After Week 1 external module search
