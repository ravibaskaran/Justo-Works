# Customer Management API

## Purpose

Provide external API for creating and updating customer master records in the Odoo real estate system. This API enables integration with external CRM systems, mobile applications, and partner portals to synchronize customer information.

## Scope

**Included:**
- Customer creation via API
- Customer update via API (upsert pattern)
- Customer data validation
- Address and contact information management
- Financial information (bank details, credit terms)
- Personal information (gender, date of birth, occupation)
- KYC documents (PAN, Aadhar, GSTIN)

**Excluded:**
- Customer deletion (must be done through Odoo UI for audit trail)
- Customer search/listing (separate read API)
- Customer relationship/hierarchy management
- Transaction history access

---

## Requirements

### Requirement: Customer Creation Endpoint

The system SHALL provide an API endpoint for creating customer records.

#### Scenario: Endpoint specification
- **WHEN** accessing customer creation API
- **THEN** endpoint is available at `/project/customer_master_create`
- **AND** endpoint accepts HTTP POST requests
- **AND** endpoint requires authentication with `customer` scope

#### Scenario: Request format
- **WHEN** creating customer via API
- **THEN** request body uses JSON format:
  ```json
  {
    "params": {
      "login": "api_username",
      "password": "api_key_hash",
      "record": {
        "customer_id": "CU1234",
        "name": "Customer Name",
        ...
      }
    }
  }
  ```

---

### Requirement: Upsert Behavior

The API SHALL support both create and update operations based on `customer_id` presence.

#### Scenario: Create new customer
- **WHEN** `customer_id` is not provided in request
- **THEN** system creates new customer record
- **AND** system generates unique `customer_id`
- **AND** returns created customer ID and success message

#### Scenario: Update existing customer
- **WHEN** `customer_id` is provided and matches existing customer
- **THEN** system updates the existing customer record
- **AND** only provided fields are updated (partial update)
- **AND** returns updated customer ID and success message

#### Scenario: Invalid customer ID
- **WHEN** `customer_id` is provided but does not match any existing customer
- **THEN** system returns error indicating customer not found
- **AND** does not create new record

---

### Requirement: Required Fields

Customer creation SHALL enforce required field validation.

#### Scenario: Minimum required fields
- **WHEN** creating new customer
- **THEN** the following fields are required:
  - `name` (Customer full name)
  - `state_code` (State code, e.g., "KL", "TN", "MH")
  - `country_code` (Country code, e.g., "IN")

#### Scenario: Missing required fields
- **WHEN** required field is missing from request
- **THEN** system returns 400 Bad Request
- **AND** error message specifies which required field is missing

---

### Requirement: Customer Data Fields

The API SHALL accept comprehensive customer information across multiple categories.

#### Scenario: Basic information
- **WHEN** creating/updating customer
- **THEN** system accepts following basic fields:
  - `customer_id` (String) - Unique customer identifier
  - `name` (String, Required) - Customer full name

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
  - `mobile` (String) - Mobile number
  - `email` (String) - Email address
  - `website` (String) - Website URL

#### Scenario: KYC and tax information
- **WHEN** providing tax/identity documents
- **THEN** system accepts:
  - `gstin` (String) - GST Identification Number
  - `pan` (String) - Permanent Account Number
  - `aadhar` (String) - Aadhar number

#### Scenario: Banking information
- **WHEN** providing bank details
- **THEN** system accepts:
  - `bank` (String) - Bank name
  - `ifsc` (String) - IFSC code
  - `account_number` (String) - Bank account number

#### Scenario: Personal information
- **WHEN** providing personal details
- **THEN** system accepts:
  - `gender` (String) - Gender code ("M", "F", "O")
  - `date_of_birth` (String) - Format: "DD-MM-YYYY"
  - `occupation` (String) - Occupation/profession

#### Scenario: Financial terms
- **WHEN** providing financial information
- **THEN** system accepts:
  - `credit_days` (Integer) - Credit period in days
  - `income` (Float) - Annual income amount

---

### Requirement: Data Validation

Customer data SHALL be validated before persisting to database.

#### Scenario: Email validation
- **WHEN** email is provided
- **THEN** system validates email format (contains @ and domain)
- **AND** rejects invalid email formats with error message

#### Scenario: Phone number validation
- **WHEN** phone or mobile is provided
- **THEN** system accepts numeric characters and common separators (+, -, space, parentheses)

#### Scenario: Date format validation
- **WHEN** date_of_birth is provided
- **THEN** system validates format is "DD-MM-YYYY"
- **AND** validates date is valid calendar date
- **AND** validates customer is of reasonable age (e.g., >= 18 years)

#### Scenario: Gender code validation
- **WHEN** gender is provided
- **THEN** system accepts only: "M" (Male), "F" (Female), "O" (Other)
- **AND** rejects invalid gender codes

#### Scenario: State and country code validation
- **WHEN** state_code or country_code provided
- **THEN** system validates against Odoo's res.country.state and res.country tables
- **AND** rejects invalid codes with error message

---

### Requirement: Response Format

The API SHALL return consistent JSON responses.

#### Scenario: Successful creation
- **WHEN** customer is successfully created
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "message": "Customer created successfully",
      "customer_id": "CU1234",
      "odoo_partner_id": 12345
    }
  }
  ```

#### Scenario: Successful update
- **WHEN** customer is successfully updated
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "message": "Customer updated successfully",
      "customer_id": "CU1234",
      "odoo_partner_id": 12345
    }
  }
  ```

#### Scenario: Validation error
- **WHEN** validation fails
- **THEN** response includes:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Validation failed",
      "details": {
        "field": "email",
        "error": "Invalid email format"
      }
    }
  }
  ```

#### Scenario: Server error
- **WHEN** unexpected error occurs
- **THEN** response includes:
  ```json
  {
    "error": {
      "code": "INTERNAL_ERROR",
      "message": "An error occurred while processing request",
      "details": "Error description (if in debug mode)"
    }
  }
  ```

---

### Requirement: Duplicate Prevention

The system SHALL prevent duplicate customer records.

#### Scenario: Duplicate customer_id
- **WHEN** creating customer with existing customer_id
- **THEN** system performs update instead of create
- **AND** returns appropriate update response

#### Scenario: Duplicate detection by name/email
- **WHEN** creating customer
- **THEN** system checks for existing customers with same name and email
- **AND** warns if potential duplicate detected (but allows creation)

---

### Requirement: Audit Trail

All customer API operations SHALL be logged for audit purposes.

#### Scenario: API call logging
- **WHEN** customer API is called
- **THEN** system logs: timestamp, API user, operation (create/update), customer_id, IP address, request payload
- **AND** logs success/failure status

#### Scenario: Change tracking
- **WHEN** customer is updated via API
- **THEN** Odoo's built-in audit trail captures field changes
- **AND** shows who made changes and when

---

## Integration Examples

### Create New Customer
```bash
curl -X POST https://odoo.example.com/project/customer_master_create \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "login": "api_user",
      "password": "api_key_hash",
      "record": {
        "name": "John Doe",
        "state_code": "KL",
        "country_code": "IN",
        "email": "john.doe@example.com",
        "mobile": "9876543210"
      }
    }
  }'
```

### Update Existing Customer
```bash
curl -X POST https://odoo.example.com/project/customer_master_create \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "login": "api_user",
      "password": "api_key_hash",
      "record": {
        "customer_id": "CU1234",
        "email": "john.doe.updated@example.com",
        "mobile": "9876543211"
      }
    }
  }'
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| MISSING_CREDENTIALS | 400 | Login or password not provided |
| INVALID_CREDENTIALS | 401 | Authentication failed |
| INSUFFICIENT_SCOPE | 403 | API key lacks `customer` scope |
| MISSING_REQUIRED_FIELD | 400 | Required field missing (name, state_code, country_code) |
| VALIDATION_ERROR | 400 | Field validation failed |
| CUSTOMER_NOT_FOUND | 404 | Customer ID provided but not found (when updating) |
| DUPLICATE_CUSTOMER | 409 | Duplicate customer detected |
| INTERNAL_ERROR | 500 | Server error during processing |

---

## Implementation Notes

- Customer records are stored in `res.partner` model with `customer_rank > 0`
- `customer_id` maps to a custom field or reference field in partner model
- State codes reference `res.country.state` model
- Country codes reference `res.country` model
- All monetary amounts stored in company's default currency
- Date fields converted to Odoo's internal date format for storage
- API logging stored in custom `api.log` model
