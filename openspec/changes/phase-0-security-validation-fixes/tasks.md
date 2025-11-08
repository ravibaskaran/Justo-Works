# Phase 0 Implementation Tasks - Security & Validation Fixes

**Branch:** `claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR`
**Estimated Duration:** 2-3 weeks
**Priority:** CRITICAL (Pre-Migration)

---

## PART 1: API LOGGING SECURITY FIXES (Week 1-2)

### Task 1: Update API Log Model
**File:** `addons_custom/real_estate_extension/models/api_log.py`

- [ ] 1.1 Read current `api_log.py` model implementation
- [ ] 1.2 Add new fields to model:
  - [ ] 1.2.1 `ip_address` (Char, size=45, string="IP Address")
  - [ ] 1.2.2 `user_agent` (Text, string="User Agent")
  - [ ] 1.2.3 `execution_time` (Float, string="Execution Time (ms)")
  - [ ] 1.2.4 Rename `args` to `request_payload` (Text, string="Request Payload (Sanitized)")
  - [ ] 1.2.5 Add `response_payload` (Text, string="Response Payload (Sanitized)")
  - [ ] 1.2.6 Add `sanitized` (Boolean, string="Data Sanitized", default=False)
  - [ ] 1.2.7 Add `is_sensitive` (Boolean, string="Contains Sensitive Data", default=False)
- [ ] 1.3 Update view XML for new fields
- [ ] 1.4 Update security rules (ir.model.access.csv)
- [ ] 1.5 Test model changes in Odoo 15

### Task 2: Implement Data Sanitization
**New File:** `addons_custom/real_estate_extension/models/sanitizer.py`

- [ ] 2.1 Create sanitizer utility class
- [ ] 2.2 Implement password/API key masking:
  - [ ] 2.2.1 Detect fields: `password`, `api_key`, `token`, `secret`, `pwd`
  - [ ] 2.2.2 Mask pattern: show first 4 + last 4 chars, mask middle with `***`
  - [ ] 2.2.3 Example: `password123456` → `pass******3456`
- [ ] 2.3 Implement PII masking:
  - [ ] 2.3.1 Aadhar number: show only last 4 digits (`**** **** **34`)
  - [ ] 2.3.2 PAN number: show only last 4 chars (`******5678`)
  - [ ] 2.3.3 Bank account: show only last 4 digits (`*********1234`)
  - [ ] 2.3.4 Date of birth: mask to year only (`****-**-01` → `1990-**-**`)
  - [ ] 2.3.5 Phone/Mobile: mask middle digits (`+91 98*** ***45`)
- [ ] 2.4 Create configurable sanitization rules:
  - [ ] 2.4.1 Field name patterns (regex support)
  - [ ] 2.4.2 Data type patterns (email, phone, date)
  - [ ] 2.4.3 Whitelist for non-sensitive fields
- [ ] 2.5 Write unit tests for sanitizer:
  - [ ] 2.5.1 Test password masking
  - [ ] 2.5.2 Test PII masking (all types)
  - [ ] 2.5.3 Test nested dict sanitization
  - [ ] 2.5.4 Test list of dicts sanitization
  - [ ] 2.5.5 Test edge cases (None, empty strings, special chars)

### Task 3: Update add_api_log() Method
**File:** `addons_custom/real_estate_extension/controllers/controllers.py`

- [ ] 3.1 Locate current `add_api_log()` helper method
- [ ] 3.2 Refactor to accept new parameters:
  - [ ] 3.2.1 `request_data` (dict) - request payload
  - [ ] 3.2.2 `response_data` (dict) - response payload
  - [ ] 3.2.3 `execution_time` (float) - milliseconds
  - [ ] 3.2.4 `request_obj` (http.request) - for IP and user agent
- [ ] 3.3 Implement IP address capture:
  - [ ] 3.3.1 Get from `request.httprequest.remote_addr`
  - [ ] 3.3.2 Handle proxy headers (X-Forwarded-For, X-Real-IP)
  - [ ] 3.3.3 Validate IP format (IPv4/IPv6)
- [ ] 3.4 Implement user agent capture:
  - [ ] 3.4.1 Get from `request.httprequest.headers.get('User-Agent')`
  - [ ] 3.4.2 Truncate if > 500 chars
- [ ] 3.5 Integrate sanitizer:
  - [ ] 3.5.1 Sanitize request_data before storing
  - [ ] 3.5.2 Sanitize response_data before storing
  - [ ] 3.5.3 Set `sanitized=True` flag
  - [ ] 3.5.4 Set `is_sensitive=True` if sensitive fields detected
- [ ] 3.6 Store execution time in milliseconds
- [ ] 3.7 Update method signature and calls

### Task 4: Update All API Endpoints
**Files:**
- `addons_custom/real_estate_extension/controllers/controllers.py` (8 endpoints)
- `addons_custom/itsys_real_estate/controllers/controller.py` (2 endpoints)

#### 4.1 Customer API Endpoints
- [ ] 4.1.1 `customer_master_create` (line ~698):
  - [ ] Add timer at start: `start_time = time.time()`
  - [ ] Calculate execution time: `exec_time = (time.time() - start_time) * 1000`
  - [ ] Update `add_api_log()` call with new parameters
  - [ ] Pass request object, request_data, response_data, exec_time
- [ ] 4.1.2 `customer_master_update`:
  - [ ] Same pattern as above
- [ ] 4.1.3 `customer/fetch_customer_id`:
  - [ ] Same pattern as above

#### 4.2 Channel Partner API Endpoints
- [ ] 4.2.1 `cp_master_create`:
  - [ ] Add timing and logging updates
- [ ] 4.2.2 `cp/fetch_channel_partner_id` (line ~1225):
  - [ ] Add timing and logging updates

#### 4.3 Employee API Endpoints
- [ ] 4.3.1 `employee_master_create`:
  - [ ] Add timing and logging updates
- [ ] 4.3.2 `employee/fetch_employee_code123` (line ~894):
  - [ ] Add timing and logging updates

#### 4.4 Inventory & Project API Endpoints
- [ ] 4.4.1 `inventory_api` endpoints (itsys_real_estate):
  - [ ] Review and update logging
- [ ] 4.4.2 `project_api` endpoints (itsys_real_estate):
  - [ ] Review and update logging

### Task 5: Implement Log Retention Policy
**New File:** `addons_custom/real_estate_extension/data/ir_cron.xml`

- [ ] 5.1 Create scheduled action for log archival:
  - [ ] 5.1.1 Name: "Archive API Logs (90 days)"
  - [ ] 5.1.2 Model: `api.log`
  - [ ] 5.1.3 Method: `action_archive_old_logs`
  - [ ] 5.1.4 Frequency: Daily at 2:00 AM
  - [ ] 5.1.5 Active: True
- [ ] 5.2 Create scheduled action for log purging:
  - [ ] 5.2.1 Name: "Purge Archived API Logs (2 years)"
  - [ ] 5.2.2 Model: `api.log`
  - [ ] 5.2.3 Method: `action_purge_old_logs`
  - [ ] 5.2.4 Frequency: Weekly (Sunday 3:00 AM)
  - [ ] 5.2.5 Active: True
- [ ] 5.3 Implement archival method in api_log.py:
  - [ ] 5.3.1 Find logs older than 90 days
  - [ ] 5.3.2 Set `active=False` (soft delete)
  - [ ] 5.3.3 Log archival summary
- [ ] 5.4 Implement purge method in api_log.py:
  - [ ] 5.4.1 Find archived logs older than 2 years
  - [ ] 5.4.2 Hard delete (unlink)
  - [ ] 5.4.3 Log purge summary
- [ ] 5.5 Add configuration settings:
  - [ ] 5.5.1 `api_log_retention_days` (default: 90)
  - [ ] 5.5.2 `api_log_archive_years` (default: 2)
- [ ] 5.6 Test retention policy:
  - [ ] 5.6.1 Create test logs with backdated dates
  - [ ] 5.6.2 Run archival manually
  - [ ] 5.6.3 Run purge manually
  - [ ] 5.6.4 Verify counts

### Task 6: Performance Testing
- [ ] 6.1 Measure baseline API performance (before changes)
- [ ] 6.2 Measure performance with sanitization (after changes)
- [ ] 6.3 Verify overhead < 50ms per API call
- [ ] 6.4 Optimize sanitizer if needed:
  - [ ] 6.4.1 Cache compiled regex patterns
  - [ ] 6.4.2 Optimize recursive dict traversal
  - [ ] 6.4.3 Add depth limit for nested objects

### Task 7: Update OpenSpec Specification
**File:** `openspec/specs/api-logging/spec.md`

- [ ] 7.1 Review current spec requirements
- [ ] 7.2 Add requirements for data sanitization
- [ ] 7.3 Add requirements for audit fields (IP, user agent, execution time)
- [ ] 7.4 Add scenarios for retention policy
- [ ] 7.5 Document new log model fields
- [ ] 7.6 Document sanitization rules and patterns
- [ ] 7.7 Run `openspec validate api-logging --strict`

---

## PART 2: API DATA VALIDATION FIXES (Week 2-3)

### Task 8: Create Validation Utility Module
**New File:** `addons_custom/real_estate_extension/models/validators.py`

- [ ] 8.1 Create base validator class
- [ ] 8.2 Implement email validator:
  - [ ] 8.2.1 Use regex pattern for email format
  - [ ] 8.2.2 Check for `@` and domain
  - [ ] 8.2.3 Return (valid: bool, error_msg: str)
- [ ] 8.3 Implement phone validator:
  - [ ] 8.3.1 Support formats: +91-9876543210, 9876543210
  - [ ] 8.3.2 Validate length (10 digits for India)
  - [ ] 8.3.3 Allow configurable country codes
- [ ] 8.4 Implement state/country validator:
  - [ ] 8.4.1 Query `res.country.state` for state_code
  - [ ] 8.4.2 Query `res.country` for country_code
  - [ ] 8.4.3 Return validation result with error message
- [ ] 8.5 Implement date validator:
  - [ ] 8.5.1 Support formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
  - [ ] 8.5.2 Validate date ranges (e.g., birth date < today)
  - [ ] 8.5.3 Return normalized date string
- [ ] 8.6 Implement required fields validator:
  - [ ] 8.6.1 Accept field_list and data dict
  - [ ] 8.6.2 Check each required field exists and is not empty
  - [ ] 8.6.3 Return list of missing fields
- [ ] 8.7 Write unit tests for validators:
  - [ ] 8.7.1 Test email validator (valid/invalid cases)
  - [ ] 8.7.2 Test phone validator (various formats)
  - [ ] 8.7.3 Test state/country validator
  - [ ] 8.7.4 Test date validator (formats and ranges)
  - [ ] 8.7.5 Test required fields validator

### Task 9: Create Error Response Builder
**New File:** `addons_custom/real_estate_extension/controllers/response_builder.py`

- [ ] 9.1 Create standard response format:
  ```python
  {
    "status": "success|error",
    "code": 200|400|404|500,
    "message": "...",
    "data": {...},
    "errors": [...],
    "timestamp": "ISO8601"
  }
  ```
- [ ] 9.2 Implement success response builder:
  - [ ] 9.2.1 HTTP 200 for successful read/list
  - [ ] 9.2.2 HTTP 201 for successful create
  - [ ] 9.2.3 HTTP 200 for successful update
  - [ ] 9.2.4 Include created/updated record IDs
- [ ] 9.3 Implement error response builder:
  - [ ] 9.3.1 HTTP 400 for validation errors (Bad Request)
  - [ ] 9.3.2 HTTP 404 for not found errors
  - [ ] 9.3.3 HTTP 500 for server errors
  - [ ] 9.3.4 Include detailed error messages
- [ ] 9.4 Add timestamp to all responses (ISO 8601 format)
- [ ] 9.5 Write tests for response builder

### Task 10: Customer API Validation
**File:** `addons_custom/real_estate_extension/controllers/controllers.py`

#### 10.1 customer_master_create (line ~698)
- [ ] 10.1.1 Add required field validation:
  - [ ] Required: `name`, `state_code`, `country_code`
  - [ ] Return 400 if missing
- [ ] 10.1.2 Uncomment state/country validation (lines 718-722)
- [ ] 10.1.3 Fix state/country code validation:
  - [ ] Use validators.validate_state_country()
  - [ ] Return 400 with error message if invalid
- [ ] 10.1.4 Add email format validation:
  - [ ] If email provided, validate format
  - [ ] Return 400 if invalid format
- [ ] 10.1.5 Add phone number format validation:
  - [ ] If mobile/phone provided, validate format
  - [ ] Return 400 if invalid
- [ ] 10.1.6 Return proper HTTP status codes:
  - [ ] 201 for successful creation (with customer_id and odoo_partner_id)
  - [ ] 400 for validation errors
  - [ ] 500 for server errors
- [ ] 10.1.7 Use response_builder for all responses
- [ ] 10.1.8 Test with valid data
- [ ] 10.1.9 Test with missing required fields
- [ ] 10.1.10 Test with invalid state/country codes
- [ ] 10.1.11 Test with invalid email
- [ ] 10.1.12 Test with invalid phone

#### 10.2 customer_master_update
- [ ] 10.2.1 Add same validation as create
- [ ] 10.2.2 Add record existence check (404 if not found)
- [ ] 10.2.3 Return 200 with updated record ID
- [ ] 10.2.4 Test update scenarios

#### 10.3 customer/fetch_customer_id
- [ ] 10.3.1 Validate request parameters
- [ ] 10.3.2 Return 404 if customer not found
- [ ] 10.3.3 Return 200 with customer data
- [ ] 10.3.4 Test fetch scenarios

### Task 11: Channel Partner API Validation
**File:** `addons_custom/real_estate_extension/controllers/controllers.py`

#### 11.1 cp_master_create
- [ ] 11.1.1 Add required field validation:
  - [ ] Required: `name`, `state_code`, `country_code`, `mobile`
- [ ] 11.1.2 Add state/country code validation
- [ ] 11.1.3 Add email format validation
- [ ] 11.1.4 Add RERA number format validation (if applicable)
- [ ] 11.1.5 Add mobile number format validation
- [ ] 11.1.6 Return proper HTTP status codes
- [ ] 11.1.7 Use response_builder
- [ ] 11.1.8 Test all validation scenarios

#### 11.2 cp/fetch_channel_partner_id (line ~1225)
- [ ] 11.2.1 Validate request parameters
- [ ] 11.2.2 Return 404 if not found
- [ ] 11.2.3 Return 200 with partner data
- [ ] 11.2.4 Test fetch scenarios

### Task 12: Employee API Validation
**File:** `addons_custom/real_estate_extension/controllers/controllers.py`

#### 12.1 employee_master_create
- [ ] 12.1.1 Add required field validation
- [ ] 12.1.2 Validate gender codes:
  - [ ] Accept: F, f, M, m, O, o
  - [ ] Return 400 if invalid
- [ ] 12.1.3 Validate marital status values:
  - [ ] Accept: single, married, divorced, widowed
  - [ ] Return 400 if invalid
- [ ] 12.1.4 Validate active status:
  - [ ] Accept: T, t, F, f, True, False
  - [ ] Convert to boolean
- [ ] 12.1.5 Validate date formats:
  - [ ] Support: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
  - [ ] Return 400 if invalid
- [ ] 12.1.6 Return proper HTTP status codes
- [ ] 12.1.7 Use response_builder
- [ ] 12.1.8 Test all validation scenarios

#### 12.2 employee/fetch_employee_code (fix URL)
- [ ] 12.2.1 Fix URL endpoint:
  - [ ] FROM: `/fetch_employee_code123`
  - [ ] TO: `/fetch_employee_code`
- [ ] 12.2.2 Add validation
- [ ] 12.2.3 Return 404 if not found
- [ ] 12.2.4 Test fetch scenarios

### Task 13: Integration Testing
- [ ] 13.1 Create test script for all API endpoints
- [ ] 13.2 Test Customer API:
  - [ ] 13.2.1 Create with valid data → 201
  - [ ] 13.2.2 Create with missing required fields → 400
  - [ ] 13.2.3 Create with invalid state → 400
  - [ ] 13.2.4 Create with invalid email → 400
  - [ ] 13.2.5 Update existing → 200
  - [ ] 13.2.6 Fetch existing → 200
  - [ ] 13.2.7 Fetch non-existent → 404
- [ ] 13.3 Test Channel Partner API (same scenarios)
- [ ] 13.4 Test Employee API (same scenarios)
- [ ] 13.5 Verify API logs contain:
  - [ ] 13.5.1 IP address
  - [ ] 13.5.2 User agent
  - [ ] 13.5.3 Execution time
  - [ ] 13.5.4 Sanitized payloads (no passwords visible)
- [ ] 13.6 Verify proper HTTP status codes returned
- [ ] 13.7 Performance testing (response time < 2 seconds)

### Task 14: Update OpenSpec Specifications
**Files:**
- `openspec/specs/customer-api/spec.md`
- `openspec/specs/channel-partner-api/spec.md`
- `openspec/specs/employee-api/spec.md`

- [ ] 14.1 Update customer-api spec:
  - [ ] 14.1.1 Document required fields
  - [ ] 14.1.2 Document validation rules
  - [ ] 14.1.3 Document HTTP status codes
  - [ ] 14.1.4 Add scenarios for validation errors
- [ ] 14.2 Update channel-partner-api spec (same pattern)
- [ ] 14.3 Update employee-api spec (same pattern)
- [ ] 14.4 Run validation:
  - [ ] `openspec validate customer-api --strict`
  - [ ] `openspec validate channel-partner-api --strict`
  - [ ] `openspec validate employee-api --strict`

---

## PART 3: DOCUMENTATION & VALIDATION (Week 3)

### Task 15: Security Documentation
- [ ] 15.1 Create security advisory document
- [ ] 15.2 Document what was fixed:
  - [ ] 15.2.1 Credential exposure vulnerability
  - [ ] 15.2.2 PII masking implementation
  - [ ] 15.2.3 Log retention policy
- [ ] 15.3 Document sanitization rules
- [ ] 15.4 Create admin guide for configuring retention policy

### Task 16: API Documentation
- [ ] 16.1 Update API documentation with:
  - [ ] 16.1.1 Required fields per endpoint
  - [ ] 16.1.2 Validation rules
  - [ ] 16.1.3 Error codes and messages
  - [ ] 16.1.4 Example requests/responses
- [ ] 16.2 Create migration guide for API consumers
- [ ] 16.3 Document breaking changes (validation now enforced)

### Task 17: Final Validation
- [ ] 17.1 Run complete test suite
- [ ] 17.2 Security audit:
  - [ ] 17.2.1 Review API logs - confirm no sensitive data visible
  - [ ] 17.2.2 Test with actual passwords/API keys
  - [ ] 17.2.3 Verify PII masking working
- [ ] 17.3 Performance validation:
  - [ ] 17.3.1 Measure API response times
  - [ ] 17.3.2 Verify < 50ms overhead from sanitization
  - [ ] 17.3.3 Load test with 100 concurrent requests
- [ ] 17.4 User acceptance testing:
  - [ ] 17.4.1 Test all API endpoints manually
  - [ ] 17.4.2 Verify error messages are clear
  - [ ] 17.4.3 Verify audit fields populated correctly
- [ ] 17.5 Create rollback plan (in case issues found)

### Task 18: Code Review & Cleanup
- [ ] 18.1 Review all modified files
- [ ] 18.2 Remove commented code
- [ ] 18.3 Add docstrings to all new methods
- [ ] 18.4 Follow PEP 8 style guide
- [ ] 18.5 Remove debug print statements
- [ ] 18.6 Update module version in `__manifest__.py`

### Task 19: Commit & Documentation
- [ ] 19.1 Stage all changes: `git add -A`
- [ ] 19.2 Create comprehensive commit message
- [ ] 19.3 Push to branch: `claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR`
- [ ] 19.4 Update OpenSpec change status
- [ ] 19.5 Mark all tasks complete in tasks.md

### Task 20: Sign-off & Next Phase Prep
- [ ] 20.1 Obtain stakeholder approval for Phase 0 completion
- [ ] 20.2 Document lessons learned
- [ ] 20.3 Update project timeline
- [ ] 20.4 Plan Phase 1 (Odoo 18 environment setup)
- [ ] 20.5 Archive Phase 0 change proposals

---

## Success Metrics

At completion of Phase 0:
- ✅ **Security:** 0 sensitive data leaks in API logs
- ✅ **Validation:** 0 invalid records in database from API
- ✅ **Performance:** API response time increase < 50ms
- ✅ **Code Quality:** All tests passing, 0 linter errors
- ✅ **Documentation:** Complete specs updated and validated
- ✅ **Compliance:** Log retention policy active

**Ready to proceed to Phase 1: Odoo 18 Environment Setup**
