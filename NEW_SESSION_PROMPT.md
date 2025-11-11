# 🚀 NEW SESSION PROMPT - Phase 4 Continuation

Copy and paste this prompt into your next Claude Code session to continue the migration:

---

## Prompt for New Session

```
I'm continuing the Odoo 15 to Odoo 18 migration for Phase 4 (Advanced Web Components).

CRITICAL CONTEXT FILES (READ THESE FIRST):
1. Read SESSION_HANDOFF.md - Complete current state and context
2. Read MIGRATION_PROJECT.md - Full project overview with all phases
3. Read PHASE4_ANALYSIS.md - Detailed module breakdown

CURRENT STATUS:
- Branch: claude/odoo-migration-phase-4-011CUzPH4THuZUx9HPdFk93k
- Phase 4: 79% complete (11 of 14 modules)
- Strategy: "Migrate First, Test Later" - complete all coding before testing

COMPLETED WORK:
✅ Option 1: All 10 Python modules (100%)
   - hide_menu_user, kg_hide_menu, gst_invoice, jupiter_accounts
   - ms_query, report_pdf_options, base_account_budget
   - partner_account_creation, payment_adjustment, project_transactions

✅ Option 2 (Partial): jupiter_dashboard_deux (1 of 4 dashboards)
   - 600 lines migrated to OWL Component
   - ApexCharts integration with horizontal scroll/drag
   - All RPC endpoints functional

PENDING WORK (Option 2 - Dashboards):
🔄 jupiter_dashboard
   - File: /addons_custom/jupiter_dashboard/static/src/js/dashboard.js
   - Lines: 693 (similar to jupiter_dashboard_deux)
   - Estimated: 4-6 hours
   - Note: apexcharts.js (13 lines) is third-party library (NO MIGRATION)

⏸️ jupiter_dashboard_tres
   - Files: 5 JavaScript files (exact count TBD)
   - Estimated: 6-8 hours
   - Status: Not started

⏸️ jupiter_dashboard_optima
   - Files: 5 JavaScript files (exact count TBD)
   - Estimated: 6-8 hours
   - Status: Not started

MIGRATION PATTERN (Use jupiter_dashboard_deux as reference):
- AbstractAction → OWL Component
- ajax.jsonRpc() → useService("rpc")
- core.action_registry → registry.category("actions")
- jQuery $ → Native DOM (querySelector, querySelectorAll)
- ApexCharts: Load with loadJS() in onWillStart()
- Create helper methods: updateElement(), setAttribute(), etc.
- Include comprehensive migration notes in comments

WORKFLOW FOR EACH MODULE:
1. Read the dashboard.js file
2. Convert to OWL Component structure
3. Migrate all RPC calls to useService("rpc")
4. Replace jQuery with native DOM
5. Handle ApexCharts integration
6. Update __manifest__.py (version to 18.0.x.x.x)
7. Sync to demo_addons_custom/
8. Commit with clear message
9. Move to next module

COMMIT GUIDELINES:
- Commit after EACH complete module (not mid-module)
- Use descriptive commit messages with statistics
- Push to remote after each commit
- Format: "[Module] Complete: [Brief description]"

QUALITY STANDARDS:
- 100% quality score maintained from Phase 3
- All migrations include inline comments
- Manifest includes comprehensive description
- Testing requirements documented
- Migration notes explain all changes

AFTER ALL MODULES COMPLETE:
1. Update PHASE4_COMPLETION_SUMMARY.md
2. Update SESSION_HANDOFF.md with final status
3. Commit all documentation updates
4. Provide testing plan for Phase 5

START WITH:
Complete jupiter_dashboard migration (693 lines, similar pattern to jupiter_dashboard_deux).

Reference file: /home/user/Justo-Works/addons_custom/jupiter_dashboard_deux/static/src/js/dashboard.js (600 lines - your best example)
```

---

## Expected Session Outcome

By the end of the next session, you should have:

✅ jupiter_dashboard fully migrated (693 lines → OWL)
✅ jupiter_dashboard_tres fully migrated (5 files → OWL)
✅ jupiter_dashboard_optima fully migrated (5 files → OWL)
✅ All manifests updated to 18.0.x.x.x
✅ All changes synced to demo_addons_custom/
✅ All commits pushed to remote
✅ Documentation updated
✅ Phase 4 marked as 100% complete

**Total Expected Time:** 16-22 hours of focused work

---

## Quick Reference Commands

```bash
# Check current branch
git branch

# View file structure
ls -la /home/user/Justo-Works/addons_custom/jupiter_dashboard/static/src/js/

# Read example dashboard (BEST REFERENCE)
cat /home/user/Justo-Works/addons_custom/jupiter_dashboard_deux/static/src/js/dashboard.js

# After migration, sync to demo
cp /home/user/Justo-Works/addons_custom/MODULE/__manifest__.py \
   /home/user/Justo-Works/demo_addons_custom/MODULE/__manifest__.py

cp /home/user/Justo-Works/addons_custom/MODULE/static/src/js/*.js \
   /home/user/Justo-Works/demo_addons_custom/MODULE/static/src/js/

# Commit changes
git add -A
git commit -m "Complete [MODULE] migration to Odoo 18 OWL"
git push -u origin claude/odoo-migration-phase-4-011CUzPH4THuZUx9HPdFk93k
```

---

## Key Files Location

```
SESSION_HANDOFF.md       → Complete current context
MIGRATION_PROJECT.md     → Full project overview
PHASE4_ANALYSIS.md       → Module breakdown
NEW_SESSION_PROMPT.md    → This file

jupiter_dashboard_deux/  → Your BEST reference (600 lines OWL)
  └── static/src/js/dashboard.js

jupiter_dashboard/       → NEXT TO MIGRATE (693 lines)
  └── static/src/js/
      ├── apexcharts.js  → Third-party library (13 lines) - NO MIGRATION
      └── dashboard.js   → NEEDS MIGRATION (693 lines)
```

---

## Testing Phase (Deferred to Phase 5)

After ALL modules are migrated:
- **Phase 5 Duration:** 18-24 hours
- **Testing:** Python modules (8-10h) + Dashboards (6-8h) + Integration (4-6h)
- **Critical:** kg_hide_menu (menu system), ms_query (security), payment_adjustment
- **Focus:** Dashboard rendering, ApexCharts, RPC calls, security

---

## Success Indicators

You'll know you're done when:
- ✅ All 14 Phase 4 modules show version 18.0.x.x.x
- ✅ All JavaScript uses `/** @odoo-module **/` and ES6 imports
- ✅ No jQuery (`$`) in new code (only native DOM)
- ✅ All RPC calls use `useService("rpc")`
- ✅ All components registered with `registry.category("actions")`
- ✅ All manifests have comprehensive descriptions
- ✅ All changes synced to demo_addons_custom/
- ✅ Documentation updated (SESSION_HANDOFF.md, PHASE4_COMPLETION_SUMMARY.md)

---

**Created:** 2025-11-11
**Branch:** claude/odoo-migration-phase-4-011CUzPH4THuZUx9HPdFk93k
**Remaining Effort:** 16-22 hours coding
