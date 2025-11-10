# Phase 3 Python-Only Modules Review for Odoo 18 Compatibility
Date: 2025-11-10
Reviewer: Migration Agent
Branch: claude/odoo-migration-continuation-011CUzBKMrTYXpfuRTe9LDbd

---

## Executive Summary
- **Total Modules Reviewed:** 6
- **Ready for Odoo 18:** 2 (hide_menu_user, kg_hide_menu)
- **Need Minor Fixes:** 2 (base_account_budget, ms_query)
- **Need Major Changes:** 2 (payment_adjustment, partner_account_creation)

---

## Detailed Module Reviews

### 1. base_account_budget ⚠️ NEEDS MINOR FIXES
**Priority:** HIGH
**Status:** ⚠️ NEEDS MINOR FIXES
**Current Version:** 15.0.1.1.0
**Recommended Version:** 18.0.1.1.0
**Location:** `/home/user/Justo-Works/addons_custom/base_account_budget/`

#### Issues Found:

##### 1. **[HIGH]** Manifest version outdated
   - File: `__manifest__.py:24`
   - Pattern: `'version': '15.0.1.1.0'`
   - Fix: Update to `'version': '18.0.1.1.0'`

##### 2. **[HIGH]** Deprecated `track_visibility` parameter
   - File: `models/account_budget.py:73`
   - Pattern: `track_visibility='always'`
   - Fix: Replace with `tracking=True`
   - Code:
     ```python
     state = fields.Selection([...], track_visibility='always')
     ```
   - Should be:
     ```python
     state = fields.Selection([...], tracking=True)
     ```

##### 3. **[MEDIUM]** Deprecated `_company_default_get()` method
   - File: `models/account_budget.py:37` and `models/account_budget.py:77`
   - Pattern: `self.env['res.company']._company_default_get('account.budget.post')`
   - Fix: Replace with `default=lambda self: self.env.company`
   - Impact: This method was deprecated in Odoo 13+ and removed in later versions

#### Recommendations:
- Update manifest version to 18.0.1.1.0
- Replace `track_visibility='always'` with `tracking=True`
- Replace `_company_default_get()` with `self.env.company`
- Test budget creation and state transitions after changes
- Verify mail tracking functionality works correctly

---

### 2. payment_adjustment ❌ NEEDS MAJOR CHANGES
**Priority:** HIGH
**Status:** ❌ NEEDS MAJOR CHANGES
**Current Version:** 13.0.1.1.0
**Recommended Version:** 18.0.1.1.0
**Location:** `/home/user/Justo-Works/addons_custom/payment_adjustment/`

#### Issues Found:

##### 1. **[CRITICAL]** Missing license field in manifest
   - File: `__manifest__.py`
   - Pattern: No `'license'` key present
   - Fix: Add `'license': 'LGPL-3'` or appropriate license to manifest
   - Impact: Required field in Odoo 18, module may fail to load

##### 2. **[CRITICAL]** Manifest version severely outdated
   - File: `__manifest__.py:3`
   - Pattern: `'version': '13.0.1.1.0'`
   - Fix: Update to `'version': '18.0.1.1.0'`

##### 3. **[HIGH]** Deprecated `view_type` in wizard action
   - File: `models/account_payment.py:113`
   - Pattern: `'view_type': 'form'`
   - Fix: Remove this line from the action dictionary
   - Code:
     ```python
     return {
         'name': 'Warning',
         'type': 'ir.actions.act_window',
         'res_model': 'warning.wizard',
         'view_mode': 'form',
         'view_type': 'form',  # <- Remove this line
         'target': 'new',
         ...
     }
     ```

##### 4. **[HIGH]** Deprecated `account_internal_type` field
   - File: `wizard/warning_wizard.py:68`
   - Pattern: `('account_internal_type', '=', 'payable')`
   - Fix: Replace with `('account_type', '=', 'liability_payable')`
   - Impact: Field was renamed in Odoo 16+, and values changed

##### 5. **[MEDIUM]** Missing `_description` field
   - File: `models/payment_invoice.py:7`
   - Pattern: Model `payment.invoice` has no `_description`
   - Fix: Add `_description = "Payment Invoice"` after `_name`

##### 6. **[LOW]** Debug print statements
   - Files: Multiple locations (lines 82, 98, 104, 105, 138, 213)
   - Pattern: `print()` statements throughout code
   - Fix: Remove or replace with proper logging using `_logger`

#### Recommendations:
- **CRITICAL:** Add license field to manifest immediately
- Update manifest version to 18.0.1.1.0
- Remove all `view_type` occurrences from action dictionaries
- Update `account_internal_type` to `account_type` with correct values
- Add proper `_description` fields to all models
- Replace print statements with proper logging
- Test payment reconciliation workflow thoroughly
- Test payment reset/draft functionality
- Verify warning wizard displays correctly

---

### 3. ms_query ⚠️ NEEDS MINOR FIXES
**Priority:** MEDIUM
**Status:** ⚠️ NEEDS MINOR FIXES
**Current Version:** 1.0
**Recommended Version:** 18.0.1.0.0
**Location:** `/home/user/Justo-Works/addons_custom/ms_query/`

#### Issues Found:

##### 1. **[HIGH]** Non-standard manifest version
   - File: `__manifest__.py:3`
   - Pattern: `'version': '1.0'`
   - Fix: Update to `'version': '18.0.1.0.0'` (Odoo standard format)

##### 2. **[MEDIUM]** Direct SQL execution security concern
   - File: `models/ms_query.py:28`
   - Pattern: Direct `self._cr.execute(self.name)` without validation
   - Fix: Add proper SQL injection protection and security checks
   - Impact: This is a security-sensitive module that allows arbitrary SQL execution
   - Note: Ensure only admins/authorized users can access this functionality

#### Recommendations:
- Update manifest version to proper Odoo 18 format
- Python code is otherwise compatible with Odoo 18
- Review security model and ensure only authorized users can execute queries
- Consider adding query validation/sanitization
- Test with various SQL statements (SELECT, UPDATE, DELETE)
- Verify timezone handling works correctly

---

### 4. partner_account_creation ❌ NEEDS MAJOR CHANGES
**Priority:** MEDIUM
**Status:** ❌ NEEDS MAJOR CHANGES
**Current Version:** 15.0.0.1
**Recommended Version:** 18.0.0.1
**Location:** `/home/user/Justo-Works/addons_custom/partner_account_creation/`

#### Issues Found:

##### 1. **[CRITICAL]** Missing license field in manifest
   - File: `__manifest__.py`
   - Pattern: No `'license'` key present
   - Fix: Add `'license': 'LGPL-3'` or appropriate license to manifest

##### 2. **[CRITICAL]** Deprecated model `account.account.type`
   - File: `models/res.py:41`
   - Pattern: `self.env['account.account.type']`
   - Fix: This model was removed in Odoo 16+
   - Impact: Module will fail completely - requires major refactoring
   - New approach: Use `account.account.account_type` (Selection field) instead

##### 3. **[CRITICAL]** Deprecated field `user_type_id`
   - File: `models/res.py:43, 56, 62, 75` (multiple occurrences)
   - Pattern: `'user_type_id': user_type_id.id`
   - Fix: Replace with `'account_type': 'liability_payable'` or `'asset_receivable'`
   - Impact: Field was replaced with a Selection field in Odoo 16+

##### 4. **[HIGH]** Manifest version outdated
   - File: `__manifest__.py:15`
   - Pattern: `'version': '15.0.0.1'`
   - Fix: Update to `'version': '18.0.0.1'`

##### 5. **[HIGH]** Empty author field
   - File: `__manifest__.py:12`
   - Pattern: `'author': ""`
   - Fix: Add proper author information

##### 6. **[MEDIUM]** Account type logic needs complete rewrite
   - File: `models/res.py:42-79`
   - Pattern: Using `account.account.type` model and `type` field
   - Fix: Update to use new account_type Selection field
   - New values:
     - Payable: `'account_type': 'liability_payable'`
     - Receivable: `'account_type': 'asset_receivable'`

#### Complete Rewrite Needed for Account Type Logic:
```python
# OLD (Odoo 15):
user_type_id = account_type_obj.search([('type', '=', 'payable')], limit=1)
account_obj.create({
    'user_type_id': user_type_id.id,
    ...
})

# NEW (Odoo 18):
account_obj.create({
    'account_type': 'liability_payable',  # For payable accounts
    # OR
    'account_type': 'asset_receivable',   # For receivable accounts
    ...
})
```

#### Recommendations:
- **CRITICAL:** Add license field to manifest
- **CRITICAL:** Complete rewrite of account creation logic required
- Remove all references to `account.account.type` model
- Replace `user_type_id` with `account_type` Selection field
- Update all account type references to new Selection values
- Test partner creation for vendors and customers
- Verify account code generation still works
- Check account reconciliation flags are properly set

---

### 5. hide_menu_user ✅ READY (with version update)
**Priority:** LOW
**Status:** ✅ READY
**Current Version:** 15.0.1.0.0
**Recommended Version:** 18.0.1.0.0
**Location:** `/home/user/Justo-Works/addons_custom/hide_menu_user/`

#### Issues Found:

##### 1. **[LOW]** Manifest version outdated
   - File: `__manifest__.py:25`
   - Pattern: `'version': '15.0.1.0.0'`
   - Fix: Update to `'version': '18.0.1.0.0'`

#### Recommendations:
- Update manifest version to 18.0.1.0.0
- Python code is fully compatible with Odoo 18
- No deprecated patterns found
- Test menu hiding functionality for different users
- Verify cache clearing works correctly
- Test with admin and non-admin users

---

### 6. kg_hide_menu ✅ READY (with version update)
**Priority:** LOW
**Status:** ✅ READY
**Current Version:** 15.0.1.0.0
**Recommended Version:** 18.0.1.0.0
**Location:** `/home/user/Justo-Works/addons_custom/kg_hide_menu/`

#### Issues Found:

##### 1. **[LOW]** Manifest version outdated
   - File: `__manifest__.py:20`
   - Pattern: `'version': "15.0.1.0.0"`
   - Fix: Update to `'version': "18.0.1.0.0"`

##### 2. **[LOW]** `@api.returns('self')` decorator
   - File: `models/ir_module.py:17`
   - Pattern: `@api.returns('self')`
   - Fix: This decorator is still valid but may not be necessary - review if needed
   - Impact: Low - decorator is still supported in Odoo 18

#### Recommendations:
- Update manifest version to 18.0.1.0.0
- Python code is mostly compatible with Odoo 18
- Optional: Review if `@api.returns('self')` is still needed
- Test menu loading and filtering functionality
- Verify hidden menus don't appear for restricted users
- Test controller endpoint `/correct_user_hide_menu`

---

## Overall Recommendations by Priority

### Immediate Action Required (CRITICAL):
1. **payment_adjustment**: Add missing `license` field to manifest
2. **partner_account_creation**: Add missing `license` field to manifest
3. **partner_account_creation**: Complete rewrite of account type logic (removed model)

### High Priority Changes:
1. **payment_adjustment**: Remove deprecated `view_type` and update `account_internal_type`
2. **base_account_budget**: Update `track_visibility` and `_company_default_get()`
3. All modules: Update version numbers to 18.0.x.x.x format

### Testing Requirements:

#### base_account_budget:
- [ ] Create new budget with multiple budget lines
- [ ] Test state transitions (draft → confirm → validate → done)
- [ ] Verify budget calculations (practical vs theoretical amounts)
- [ ] Check mail tracking on state changes

#### payment_adjustment:
- [ ] Create payment with invoice selection
- [ ] Test payment reconciliation
- [ ] Test payment reset to draft
- [ ] Verify warning wizard displays correctly
- [ ] Test with multiple invoices

#### ms_query:
- [ ] Execute SELECT queries
- [ ] Execute UPDATE queries
- [ ] Test with invalid SQL
- [ ] Verify security restrictions

#### partner_account_creation:
- [ ] Create new vendor partner
- [ ] Create new customer partner
- [ ] Verify accounts are created automatically
- [ ] Check account codes are generated correctly
- [ ] Verify reconcile flag is set

#### hide_menu_user:
- [ ] Hide menu for specific user
- [ ] Verify menu is hidden in UI
- [ ] Remove menu from hidden list
- [ ] Test with admin user (should not be hideable)

#### kg_hide_menu:
- [ ] Hide menu for specific user
- [ ] Verify menu filtering works
- [ ] Test menu loading performance
- [ ] Test controller endpoint

---

## Summary of Deprecated Patterns Found

### Across All Modules:
1. **track_visibility** → Use `tracking=True` instead
2. **_company_default_get()** → Use `self.env.company` instead
3. **view_type in actions** → Remove completely
4. **account.account.type model** → Model removed, use account_type Selection
5. **user_type_id field** → Changed to account_type Selection
6. **account_internal_type** → Changed to account_type

### Not Found (Good):
- ✅ No `@api.multi` or `@api.one` decorators
- ✅ No `self.pool.get()` calls
- ✅ No old API (cr, uid, context) patterns
- ✅ No `browse(cr, uid, ids)` patterns

---

## Migration Effort Estimate

| Module | Effort | Risk | Priority |
|--------|--------|------|----------|
| base_account_budget | Low (2-4 hours) | Low | HIGH |
| payment_adjustment | Medium (4-8 hours) | Medium | HIGH |
| ms_query | Low (1-2 hours) | Low | MEDIUM |
| partner_account_creation | High (8-16 hours) | High | MEDIUM |
| hide_menu_user | Minimal (30 min) | Low | LOW |
| kg_hide_menu | Minimal (30 min) | Low | LOW |

**Total Estimated Effort:** 16-30 hours

---

## Next Steps

1. **Immediate:** Add missing `license` fields to manifests (payment_adjustment, partner_account_creation)
2. **High Priority:** Fix base_account_budget and ms_query (quick wins)
3. **Medium Priority:** Refactor partner_account_creation (most complex)
4. **Low Priority:** Update payment_adjustment (testing required)
5. **Quick Wins:** Update hide_menu modules (minimal changes)

---

## Notes

- All modules have proper `_description` fields except `payment.invoice` model
- No critical security issues found (except ms_query design)
- Print statements should be replaced with logging in payment_adjustment
- Account type changes in partner_account_creation require careful testing

---

**Report Generated:** 2025-11-10
**Reviewed By:** Migration Agent
**Status:** Complete
