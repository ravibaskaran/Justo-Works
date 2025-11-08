# API Authentication and Authorization

## Purpose

Define the authentication and authorization mechanism for external API access to the Odoo real estate system. This specification covers API key-based authentication, scope-based access control, and security patterns for protecting API endpoints.

## Scope

**Included:**
- API key generation and storage
- Scope-based authorization model
- Authentication flow for JSON endpoints
- Security best practices (key rotation, hashing, HTTPS)
- Error handling for authentication failures

**Excluded:**
- Odoo user session authentication (handled by Odoo framework)
- OAuth/JWT patterns (not currently implemented)
- Rate limiting and throttling (future enhancement)

---

## Requirements

### Requirement: API Key Model

The system SHALL provide an API key model (`api.key` or equivalent) to store and manage API credentials.

#### Scenario: API key creation
- **WHEN** creating a new API key
- **THEN** system generates a unique API key identifier
- **AND** system stores the key with associated metadata: name, user_id, scopes, active status, creation date, expiration date

#### Scenario: API key storage security
- **WHEN** storing API keys
- **THEN** keys are hashed using secure one-way hashing (e.g., SHA-256 or bcrypt)
- **AND** plaintext keys are never stored in database
- **AND** generated key is shown to user exactly once upon creation

#### Scenario: API key revocation
- **WHEN** revoking an API key
- **THEN** key's active status is set to False
- **AND** subsequent authentication attempts with revoked key fail with 401 Unauthorized

---

### Requirement: Scope-Based Authorization

API keys SHALL have associated scopes that define which API endpoints can be accessed.

#### Scenario: Scope definition
- **WHEN** defining scopes
- **THEN** each scope maps to a specific API capability:
  - `employee_details` - Employee information APIs
  - `booking` - Booking creation and management APIs
  - `project` - Project data access APIs
  - `customer` - Customer management APIs
  - `channel_partner` - Channel partner operations
  - `inventory` - Inventory data access

#### Scenario: Scope enforcement
- **WHEN** API request is received
- **THEN** system validates request API key has required scope for the endpoint
- **AND** requests without required scope return 403 Forbidden

#### Scenario: Multi-scope keys
- **WHEN** creating API key
- **THEN** key can be assigned multiple scopes
- **AND** key holder can access all endpoints covered by assigned scopes

---

### Requirement: Authentication Flow

All protected API endpoints SHALL authenticate requests using API key credentials.

#### Scenario: Authentication request format
- **WHEN** calling protected API endpoint
- **THEN** request includes credentials in JSON body:
  ```json
  {
    "params": {
      "login": "api_username",
      "password": "api_key_hash",
      ...
    }
  }
  ```

#### Scenario: Successful authentication
- **WHEN** valid credentials provided
- **THEN** system validates login and password against API key records
- **AND** system checks API key is active (not revoked/expired)
- **AND** system verifies API key has required scope for endpoint
- **AND** request proceeds to business logic

#### Scenario: Failed authentication - Invalid credentials
- **WHEN** invalid login or password provided
- **THEN** system returns 401 Unauthorized
- **AND** response includes error message: "Invalid API credentials"
- **AND** request is logged for security monitoring

#### Scenario: Failed authentication - Missing credentials
- **WHEN** login or password missing from request
- **THEN** system returns 400 Bad Request
- **AND** response includes error message: "Missing authentication credentials"

#### Scenario: Failed authentication - Expired key
- **WHEN** API key has passed expiration date
- **THEN** system returns 401 Unauthorized
- **AND** response includes error message: "API key expired"

#### Scenario: Failed authorization - Insufficient scope
- **WHEN** API key lacks required scope
- **THEN** system returns 403 Forbidden
- **AND** response includes error message: "Insufficient permissions for this endpoint"

---

### Requirement: Security Best Practices

API authentication SHALL follow industry security best practices.

#### Scenario: HTTPS enforcement
- **WHEN** API endpoints are exposed
- **THEN** all endpoints require HTTPS in production
- **AND** HTTP requests are redirected to HTTPS or rejected

#### Scenario: Key complexity requirements
- **WHEN** generating API keys
- **THEN** keys are minimum 32 characters
- **AND** keys use cryptographically secure random generation
- **AND** keys include alphanumeric and special characters

#### Scenario: API key rotation
- **WHEN** API key rotation policy is implemented
- **THEN** keys have configurable expiration period
- **AND** system sends notifications before key expiration
- **AND** users can generate new keys before old ones expire

#### Scenario: Brute force protection
- **WHEN** multiple failed authentication attempts occur
- **THEN** system implements rate limiting per IP/key
- **AND** excessive failures trigger temporary lockout
- **AND** security team is notified of suspicious activity

---

### Requirement: Authentication Logging and Monitoring

All authentication attempts SHALL be logged for security audit and monitoring.

#### Scenario: Successful authentication logging
- **WHEN** authentication succeeds
- **THEN** system logs: timestamp, API key ID, endpoint accessed, IP address, user agent

#### Scenario: Failed authentication logging
- **WHEN** authentication fails
- **THEN** system logs: timestamp, login attempted, failure reason, IP address, user agent
- **AND** repeated failures from same IP are flagged

#### Scenario: Audit trail
- **WHEN** reviewing authentication logs
- **THEN** logs are retained for minimum 90 days
- **AND** logs are accessible to security administrators
- **AND** logs can be exported for compliance audits

---

### Requirement: API Documentation and Key Management UI

Users SHALL have clear documentation and tools for managing API keys.

#### Scenario: API key management interface
- **WHEN** accessing API key management
- **THEN** users can view list of their API keys
- **AND** users can create new keys with specified scopes
- **AND** users can revoke existing keys
- **AND** users can view key metadata (name, scopes, creation date, last used)

#### Scenario: API documentation
- **WHEN** reviewing API documentation
- **THEN** each endpoint clearly states required scope
- **AND** authentication mechanism is documented with examples
- **AND** error codes and responses are documented

---

## Security Considerations

### Key Storage
- Never store plaintext API keys
- Use strong hashing algorithms (SHA-256 minimum, bcrypt/argon2 preferred)
- Salt keys before hashing to prevent rainbow table attacks

### Transport Security
- Enforce HTTPS/TLS 1.2+ for all API communication
- Use strong cipher suites
- Implement certificate pinning for mobile/embedded clients

### Scope Design
- Follow principle of least privilege
- Grant minimum scopes needed for integration
- Review and audit scope assignments regularly

### Key Lifecycle
- Implement key expiration policies
- Provide key rotation mechanisms
- Revoke keys immediately when compromise suspected
- Delete revoked keys after retention period

---

## Error Response Format

Authentication errors SHALL return consistent JSON format:

```json
{
  "error": {
    "code": "AUTH_ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional context (optional)"
  }
}
```

Common error codes:
- `MISSING_CREDENTIALS` - Login or password not provided
- `INVALID_CREDENTIALS` - Authentication failed
- `KEY_EXPIRED` - API key past expiration date
- `KEY_REVOKED` - API key has been revoked
- `INSUFFICIENT_SCOPE` - Missing required scope for endpoint
- `RATE_LIMIT_EXCEEDED` - Too many requests

---

## Implementation Checklist

- [ ] API key model created with required fields
- [ ] Hashing mechanism implemented for key storage
- [ ] Scope model and enforcement logic implemented
- [ ] Authentication decorator/middleware created
- [ ] HTTPS enforcement configured
- [ ] Authentication logging implemented
- [ ] API key management UI available
- [ ] API documentation updated with auth requirements
- [ ] Rate limiting configured
- [ ] Security monitoring and alerting configured
