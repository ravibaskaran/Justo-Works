# API Logging and Audit Trail

## Purpose

Provide comprehensive logging and audit trail capabilities for all API operations in the Odoo real estate system. This specification ensures security monitoring, compliance auditing, debugging support, and usage analytics for external API integrations.

## Scope

**Included:**
- API request/response logging
- Authentication attempt logging
- Error and exception logging
- Performance metrics capture
- Audit trail for data modifications
- Log retention and archival policies

**Excluded:**
- System-level logging (handled by Odoo framework)
- Application error logging (separate concern)
- User activity logging in UI (handled by Odoo audit log)

---

## Requirements

### Requirement: API Log Model

The system SHALL maintain an API log model to store all API operation records.

#### Scenario: Log model structure
- **WHEN** API log record is created
- **THEN** record contains following fields:
  - `log_id` - Unique log identifier (auto-generated)
  - `timestamp` - Request timestamp (UTC)
  - `api_user` - API key identifier or username
  - `endpoint` - API endpoint called (e.g., "/project/customer_master_create")
  - `http_method` - HTTP method (POST, GET, etc.)
  - `ip_address` - Client IP address
  - `user_agent` - Client user agent string
  - `request_payload` - JSON request body (sanitized)
  - `response_code` - HTTP response code (200, 400, 401, 500, etc.)
  - `response_message` - Response status message
  - `response_payload` - JSON response body (optional, configurable)
  - `execution_time` - Request processing time in milliseconds
  - `error_message` - Error details if request failed
  - `scope_used` - API scope used for authorization

---

### Requirement: Request Logging

ALL API requests SHALL be logged before processing.

#### Scenario: Successful request logging
- **WHEN** API request is received
- **THEN** system logs request with: timestamp, endpoint, user, IP, payload
- **AND** assigns unique request ID for tracing

#### Scenario: Failed authentication logging
- **WHEN** authentication fails
- **THEN** system logs: timestamp, endpoint, attempted login, IP, failure reason
- **AND** does not log sensitive credential data (passwords/keys in plaintext)

#### Scenario: Failed authorization logging
- **WHEN** authorization check fails (insufficient scope)
- **THEN** system logs: timestamp, endpoint, API user, required scope, available scopes, IP

---

### Requirement: Response Logging

ALL API responses SHALL be logged after processing.

#### Scenario: Successful response logging
- **WHEN** API request completes successfully
- **THEN** system updates log record with: response code (200, 201), execution time, success status

#### Scenario: Error response logging
- **WHEN** API request fails
- **THEN** system updates log record with: response code (400, 401, 403, 404, 500), error message, stack trace (if debug mode)

#### Scenario: Timeout logging
- **WHEN** request processing exceeds timeout
- **THEN** system logs timeout event with: timestamp, endpoint, execution time, partial response status

---

### Requirement: Data Sanitization

Sensitive data SHALL be sanitized before logging.

#### Scenario: Password sanitization
- **WHEN** logging request payload containing passwords
- **THEN** password fields are replaced with "***REDACTED***"

#### Scenario: API key sanitization
- **WHEN** logging authentication data
- **THEN** API keys are masked (show only first/last 4 characters)

#### Scenario: PII sanitization
- **WHEN** logging contains Personally Identifiable Information
- **THEN** sensitive fields (Aadhar, PAN, account numbers, DOB) are partially masked
- **AND** masking follows format: "XXXX-XXXX-1234" (last 4 digits visible)

#### Scenario: Configurable payload logging
- **WHEN** response payload logging is enabled
- **THEN** only configured endpoints log full response
- **AND** sensitive endpoints log only status without payload

---

### Requirement: Performance Metrics

API performance metrics SHALL be captured for monitoring.

#### Scenario: Execution time tracking
- **WHEN** processing API request
- **THEN** system captures total execution time in milliseconds
- **AND** breaks down time by: authentication, validation, business logic, database operations, response generation

#### Scenario: Slow query alerting
- **WHEN** API request execution exceeds threshold (e.g., 5 seconds)
- **THEN** system flags log entry as slow query
- **AND** sends alert to monitoring system

---

### Requirement: Error and Exception Logging

All API errors SHALL be logged with detailed context.

#### Scenario: Validation error logging
- **WHEN** request validation fails
- **THEN** system logs: validation error details, invalid field, expected format, provided value

#### Scenario: Business logic error logging
- **WHEN** business logic raises exception
- **THEN** system logs: error type, error message, affected record IDs, stack trace

#### Scenario: Database error logging
- **WHEN** database operation fails
- **THEN** system logs: SQL error code, error message, affected table/model, operation type

#### Scenario: External service error logging
- **WHEN** external service call fails (email, SMS, payment gateway)
- **THEN** system logs: service name, endpoint, error response, retry attempts

---

### Requirement: Audit Trail for Data Modifications

Data modification via API SHALL create audit trail.

#### Scenario: Record creation logging
- **WHEN** API creates new record (customer, employee, CP, etc.)
- **THEN** audit log captures: created_by (API user), created_date, record_type, record_id, initial values

#### Scenario: Record update logging
- **WHEN** API updates existing record
- **THEN** audit log captures: updated_by (API user), updated_date, record_type, record_id, changed_fields (before/after values)

#### Scenario: Bulk operation logging
- **WHEN** API performs bulk operations
- **THEN** audit log captures: operation type, record count, success count, failure count, affected record IDs

---

### Requirement: Log Retention and Archival

API logs SHALL be retained per compliance and operational needs.

#### Scenario: Active log retention
- **WHEN** API logs are created
- **THEN** logs remain in active database for minimum 90 days
- **AND** logs are indexed for fast querying

#### Scenario: Log archival
- **WHEN** logs exceed 90 days
- **THEN** logs are archived to long-term storage (file system, object storage, or archive database)
- **AND** archived logs are compressed to save space

#### Scenario: Log purging
- **WHEN** logs exceed maximum retention period (e.g., 2 years)
- **THEN** logs are permanently deleted after confirmation
- **AND** purging follows data retention compliance policies

---

### Requirement: Log Access and Querying

Authorized users SHALL be able to query and analyze API logs.

#### Scenario: Log search interface
- **WHEN** admin accesses log interface
- **THEN** system provides search by: date range, endpoint, API user, response code, IP address, error status

#### Scenario: Log export
- **WHEN** exporting logs for analysis
- **THEN** system supports export formats: CSV, JSON, Excel
- **AND** exports respect data sanitization rules

#### Scenario: Real-time log monitoring
- **WHEN** monitoring API health
- **THEN** system provides dashboard showing: request volume, error rates, average response time, top endpoints

---

### Requirement: Security and Compliance

API logging SHALL support security monitoring and compliance auditing.

#### Scenario: Suspicious activity detection
- **WHEN** analyzing API logs
- **THEN** system flags: repeated authentication failures, unusual request patterns, access from new IPs, high-volume requests

#### Scenario: Compliance reporting
- **WHEN** generating compliance reports
- **THEN** system provides: API access audit trail, data modification history, authentication/authorization events
- **AND** reports cover required compliance period (e.g., GDPR, SOC 2)

#### Scenario: Log integrity
- **WHEN** storing logs
- **THEN** logs are write-once (immutable after creation)
- **AND** tampering attempts are detected via checksums/hashing

---

## Log Structure Example

```json
{
  "log_id": "LOG-20240315-000123",
  "timestamp": "2024-03-15T10:30:45.123Z",
  "api_user": "api_partner_portal",
  "endpoint": "/project/customer_master_create",
  "http_method": "POST",
  "ip_address": "203.0.113.45",
  "user_agent": "PartnerPortal/2.1 (Android 12)",
  "request_payload": {
    "params": {
      "login": "api",
      "password": "***REDACTED***",
      "record": {
        "name": "John Doe",
        "email": "john@example.com",
        "pan": "***XX1234"
      }
    }
  },
  "response_code": 200,
  "response_message": "Customer created successfully",
  "execution_time": 245,
  "scope_used": "customer",
  "record_created_id": "CU12345"
}
```

---

## Error Log Example

```json
{
  "log_id": "LOG-20240315-000124",
  "timestamp": "2024-03-15T10:31:12.456Z",
  "api_user": "api_mobile_app",
  "endpoint": "/project/customer_master_create",
  "http_method": "POST",
  "ip_address": "198.51.100.22",
  "request_payload": "{ ... }",
  "response_code": 400,
  "response_message": "Validation failed",
  "error_message": "Invalid email format",
  "execution_time": 15,
  "scope_used": "customer"
}
```

---

## Implementation Checklist

- [ ] API log model created with all required fields
- [ ] Logging middleware implemented for all API routes
- [ ] Data sanitization functions implemented
- [ ] Performance metrics capture enabled
- [ ] Log retention policy configured
- [ ] Log archival automation implemented
- [ ] Log query interface available to admins
- [ ] Compliance reporting capabilities implemented
- [ ] Monitoring dashboards configured
- [ ] Alerting rules defined for errors and slow queries
- [ ] Log integrity verification implemented

---

## Performance Considerations

- Use asynchronous logging to avoid blocking API responses
- Batch log writes for high-volume endpoints
- Index log table on: timestamp, api_user, endpoint, response_code
- Partition log table by date for efficient querying
- Archive old logs to separate storage tier
- Limit payload logging size (e.g., max 10KB per request)
- Use log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
