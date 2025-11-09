# Channel Partner Management API

## Purpose

Provide external API for creating and updating channel partner records in the Odoo real estate system. Channel partners are intermediary entities (brokers, agents, agencies) who facilitate property sales and require separate management from direct customers.

## Scope

**Included:**
- Channel Partner creation via API
- Channel Partner update via API (upsert pattern)
- Channel Partner business information (RERA, GSTIN, PAN)
- Owner and contact information
- Banking details

**Excluded:**
- Channel Partner commission calculation
- Channel Partner relationship hierarchies
- Channel Partner performance metrics
- Channel Partner employee management (see cp-employee-api)

---

## Requirements

### Requirement: Channel Partner Creation Endpoint

The system SHALL provide an API endpoint for managing channel partner records.

#### Scenario: Endpoint specification
- **WHEN** accessing channel partner API
- **THEN** endpoint is available at `/cp/fetch_channel_partner_id`
- **AND** endpoint accepts HTTP POST requests
- **AND** endpoint requires authentication with `channel_partner` scope

---

### Requirement: Upsert Behavior

The API SHALL support both create and update operations based on `cp_id` presence.

#### Scenario: Create new channel partner
- **WHEN** `cp_id` is not provided in request
- **THEN** system creates new channel partner record
- **AND** system generates unique `cp_id`
- **AND** returns created CP ID and success message

#### Scenario: Update existing channel partner
- **WHEN** `cp_id` is provided and matches existing CP
- **THEN** system updates the existing CP record
- **AND** only provided fields are updated (partial update)
- **AND** returns CP ID and success message

---

### Requirement: Required Fields

Channel Partner creation SHALL enforce required field validation.

#### Scenario: Minimum required fields
- **WHEN** creating new channel partner
- **THEN** the following fields are required:
  - `name` (Channel Partner business name)
  - `state_code` (State code)
  - `country_code` (Country code, e.g., "IN")
  - `mobile` (Contact mobile number)

#### Scenario: Missing required fields
- **WHEN** required field is missing from request
- **THEN** system returns 400 Bad Request
- **AND** error message specifies which required field is missing

---

### Requirement: Channel Partner Data Fields

The API SHALL accept comprehensive channel partner information.

#### Scenario: Basic information
- **WHEN** creating/updating channel partner
- **THEN** system accepts:
  - `cp_id` (String) - Unique channel partner identifier
  - `name` (String, Required) - Business name
  - `owner_name` (String) - Owner/proprietor name

#### Scenario: Business registration
- **WHEN** providing business documents
- **THEN** system accepts:
  - `gstin` (String) - GST Identification Number
  - `rera_number` (String) - Real Estate Regulatory Authority registration
  - `pan` (String) - Permanent Account Number
  - `aadhar` (String) - Aadhar number

#### Scenario: Address information
- **WHEN** providing address
- **THEN** system accepts:
  - `street` (String) - Street address line 1
  - `street2` (String) - Street address line 2
  - `city` (String) - City name
  - `state_code` (String, Required) - State/province code
  - `country_code` (String, Required) - ISO country code
  - `zip` (String) - Postal/ZIP code

#### Scenario: Contact information
- **WHEN** providing contact details
- **THEN** system accepts:
  - `phone` (String) - Phone number
  - `mobile` (String, Required) - Mobile number
  - `email` (String) - Email address
  - `website` (String) - Website URL

#### Scenario: Banking information
- **WHEN** providing bank details
- **THEN** system accepts:
  - `bank` (String) - Bank name
  - `ifsc` (String) - IFSC code
  - `account_number` (String) - Bank account number

---

### Requirement: Data Validation

Channel Partner data SHALL be validated before persisting.

#### Scenario: RERA validation
- **WHEN** `rera_number` is provided
- **THEN** system validates format and stores for compliance

#### Scenario: Mobile validation
- **WHEN** mobile number is provided
- **THEN** system validates it contains only numeric characters and separators
- **AND** rejects invalid formats

#### Scenario: Email validation
- **WHEN** email is provided
- **THEN** system validates email format
- **AND** rejects invalid email addresses

---

### Requirement: Response Format

The API SHALL return consistent JSON responses.

#### Scenario: Successful creation
- **WHEN** channel partner is successfully created
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "message": "Channel Partner created successfully",
      "cp_id": "CP0247",
      "odoo_partner_id": 12345
    }
  }
  ```

#### Scenario: Validation error
- **WHEN** validation fails
- **THEN** response includes error code, message, and field details

---

### Requirement: Audit Trail

All channel partner API operations SHALL be logged for audit purposes.

#### Scenario: API call logging
- **WHEN** CP API is called
- **THEN** system logs: timestamp, API user, operation, cp_id, IP address, request payload, status

---

## Integration Example

```bash
curl -X POST https://odoo.example.com/cp/fetch_channel_partner_id \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "login": "api_user",
      "password": "api_key_hash",
      "record": {
        "name": "ABC Realty",
        "state_code": "KL",
        "country_code": "IN",
        "mobile": "9876543210",
        "rera_number": "RERA12345",
        "email": "contact@abcrealty.com"
      }
    }
  }'
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| MISSING_REQUIRED_FIELD | 400 | Required field missing (name, state_code, country_code, mobile) |
| VALIDATION_ERROR | 400 | Field validation failed |
| DUPLICATE_CP | 409 | Duplicate channel partner detected |
| INTERNAL_ERROR | 500 | Server error during processing |
