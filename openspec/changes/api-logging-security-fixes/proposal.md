# Change: API Logging Security Fixes

## Why

During Phase 2 API Implementation Validation (Task 1 - API Mapping), critical security
vulnerabilities were discovered in the API logging implementation:

1. **API keys and passwords logged in plain text** - The `add_api_log()` method stores
   the entire `kwargs` dict as a string, including sensitive credentials
2. **No data sanitization** - PII (Aadhar, PAN, account numbers) stored without masking
3. **Missing audit fields** - IP address, user agent, execution time not captured
4. **No retention policy** - Logs stored indefinitely without archival/purging

These issues violate security best practices and create compliance risks.

## What Changes

- **CRITICAL**: Sanitize API keys, passwords, and PII before logging
- Add missing audit fields (IP address, user agent, execution time)
- Implement structured logging (separate request_payload and response_payload fields)
- Add log retention policy (90 days active, 2 years archive)
- Update API logging specification to reflect actual requirements

## Impact

- **Affected specs**: `api-logging` (openspec/specs/api-logging/spec.md)
- **Affected code**:
  - `addons_custom/real_estate_extension/controllers/controllers.py` (~8 API endpoints)
  - `addons_custom/itsys_real_estate/controllers/controller.py` (2 API endpoints)
  - `addons_custom/real_estate_extension/models/api_log.py` (model definition)
- **Breaking changes**: None (internal logging only)
- **Security**: **HIGH IMPACT** - Fixes critical security vulnerability

## Priority

**CRITICAL** - Should be addressed before production deployment
