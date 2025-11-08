# Change: Phase 0 - Security & Validation Fixes (Pre-Migration)

## Why

Before migrating to Odoo 18, we must fix critical security vulnerabilities and data validation issues in the current Odoo 15 system. Migrating broken or insecure code to a new version compounds technical debt and creates security risks.

**Critical Issues Identified:**

### Security Issues (CRITICAL)
1. **API keys and passwords logged in plain text** - `add_api_log()` stores entire `kwargs` including sensitive credentials
2. **No data sanitization** - PII (Aadhar, PAN, account numbers) stored without masking
3. **Missing audit fields** - IP address, user agent, execution time not captured
4. **No retention policy** - Logs stored indefinitely

### Validation Issues (HIGH)
1. **Required fields not enforced** - Customer API doesn't validate required fields (name, state_code, country_code)
2. **State/country validation disabled** - Code commented out in customer API (lines 718-722)
3. **Email format validation missing** - Accepts invalid email addresses
4. **Inconsistent error codes** - Uses 201 for all errors instead of proper HTTP codes (400, 404, 500)

## What Changes

### Part 1: API Logging Security (CRITICAL)
- Implement data sanitization for sensitive fields (passwords, API keys, PII)
- Add audit fields: IP address, user agent, execution time
- Implement structured logging (separate request/response payloads)
- Add log retention policy (90 days active, 2 years archive)
- Update API logging specification

### Part 2: API Data Validation (HIGH)
- Enforce required field validation per specifications
- Restore and fix state/country code validation
- Add email format validation
- Standardize HTTP status codes (400 Bad Request, 404 Not Found, 500 Internal Error)
- Return created/updated record IDs in success responses
- Create reusable validation utility module

## Impact

- **Affected specs**: `api-logging`, `customer-api`, `channel-partner-api`, `employee-api`
- **Affected modules**:
  - `addons_custom/real_estate_extension` (main API controllers, api_log model)
  - `addons_custom/itsys_real_estate` (2 API endpoints)
- **Affected endpoints**: ~10 API endpoints total
- **Breaking changes**: MINOR - Previously accepted invalid requests will now be rejected
- **Security impact**: HIGH - Fixes critical credential exposure vulnerability
- **Data quality impact**: HIGH - Prevents invalid data entry

## Priority

**CRITICAL** - Must be completed BEFORE Odoo 18 migration begins

## Implementation Branch

All work will be done on: `claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR` (single branch policy)

## Success Criteria

- [ ] No sensitive data visible in API logs
- [ ] All validation rules enforced per spec
- [ ] Proper HTTP status codes returned
- [ ] Test suite passes 100%
- [ ] Security audit confirms no credential leakage
- [ ] Performance impact < 50ms per API call
