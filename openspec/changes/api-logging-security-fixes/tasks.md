# Implementation Tasks - API Logging Security Fixes

## 1. Update API Log Model
- [ ] 1.1 Add `ip_address` field (Char)
- [ ] 1.2 Add `user_agent` field (Text)
- [ ] 1.3 Add `execution_time` field (Float, milliseconds)
- [ ] 1.4 Separate `args` into `request_payload` (Text, sanitized) and `response_payload` (Text)
- [ ] 1.5 Add `sanitized` field (Boolean) to track if data was sanitized
- [ ] 1.6 Add migration script for new fields

## 2. Implement Data Sanitization
- [ ] 2.1 Create `sanitize_payload()` method to mask sensitive data
- [ ] 2.2 Mask password/API key fields (show only first/last 4 chars)
- [ ] 2.3 Mask PII fields:
  - [ ] Aadhar (show only last 4 digits)
  - [ ] PAN (show only last 4 chars)
  - [ ] Bank account numbers (show only last 4 digits)
  - [ ] Date of birth (mask to year only)
- [ ] 2.4 Add configurable sanitization rules

## 3. Update add_api_log() Method
- [ ] 3.1 Capture IP address from request.httprequest.remote_addr
- [ ] 3.2 Capture user agent from request.httprequest.headers
- [ ] 3.3 Calculate execution time (start timestamp - end timestamp)
- [ ] 3.4 Sanitize request payload before logging
- [ ] 3.5 Sanitize response payload before logging
- [ ] 3.6 Update all API endpoints to pass execution time

## 4. Add Performance Tracking
- [ ] 4.1 Add timer at start of each API method
- [ ] 4.2 Calculate elapsed time before logging
- [ ] 4.3 Flag slow queries (> 5 seconds) for alerting

## 5. Implement Log Retention Policy
- [ ] 5.1 Create scheduled action to archive logs > 90 days
- [ ] 5.2 Create scheduled action to purge logs > 2 years
- [ ] 5.3 Add archive table or external storage integration
- [ ] 5.4 Add configuration for retention periods

## 6. Update OpenSpec Specification
- [ ] 6.1 Update `api-logging/spec.md` with actual implementation
- [ ] 6.2 Add new requirements for sanitization
- [ ] 6.3 Add scenarios for retention policy
- [ ] 6.4 Document new fields in log model

## 7. Testing
- [ ] 7.1 Create tests for sanitization logic
- [ ] 7.2 Verify sensitive data is masked in logs
- [ ] 7.3 Verify IP address, user agent captured correctly
- [ ] 7.4 Verify execution time tracked accurately
- [ ] 7.5 Test log archival and purging

## 8. Documentation
- [ ] 8.1 Update API logging documentation
- [ ] 8.2 Document sanitization rules
- [ ] 8.3 Document retention policy configuration
- [ ] 8.4 Create security advisory about logging changes
