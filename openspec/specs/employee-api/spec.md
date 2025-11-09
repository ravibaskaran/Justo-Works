# Employee Management API

## Purpose

Provide external API for creating and updating employee records in the Odoo real estate system. This API enables integration with HRMS systems, payroll platforms, and attendance tracking systems to synchronize employee master data.

## Scope

**Included:**
- Employee creation via API
- Employee update via API
- Personal information (name, gender, marital status, date of birth)
- Employment information (department, job position, manager, joining/relieving dates)
- Contact details (personal and corporate email, mobile, emergency contact)
- Compensation information (CTC)
- Active status management

**Excluded:**
- Attendance and leave management
- Payroll calculations
- Performance reviews
- Employee hierarchy management

---

## Requirements

### Requirement: Employee Creation Endpoint

The system SHALL provide an API endpoint for managing employee records.

#### Scenario: Endpoint specification
- **WHEN** accessing employee API
- **THEN** endpoint is available at `/employee/fetch_employee_code`
- **AND** endpoint accepts HTTP POST requests
- **AND** endpoint requires authentication with `employee_details` scope

---

### Requirement: Upsert Behavior

The API SHALL support both create and update operations based on `employee_id` presence.

#### Scenario: Create new employee
- **WHEN** `employee_id` is not provided
- **THEN** system creates new employee record
- **AND** system generates unique employee_id
- **AND** returns created employee ID

#### Scenario: Update existing employee
- **WHEN** `employee_id` is provided and matches existing employee
- **THEN** system updates the employee record
- **AND** returns employee ID and success message

---

### Requirement: Employee Data Fields

The API SHALL accept comprehensive employee information.

#### Scenario: Personal information
- **WHEN** creating/updating employee
- **THEN** system accepts:
  - `employee_id` (String) - Unique employee identifier
  - `name` (String, Required) - Employee full name
  - `gender` (String) - Gender: "F"/"f" (Female), "M"/"m" (Male), "O"/"o" (Other)
  - `date_of_birth` (String) - Format: "DD/MM/YYYY" or "DD-MM-YYYY"
  - `marital_status` (String) - Values: "single", "married", "cohabitant", "widower", "divorced"
  - `pan` (String) - PAN number

#### Scenario: Employment information
- **WHEN** providing employment details
- **THEN** system accepts:
  - `job_position` (String) - Job title/position
  - `department` (String) - Department name
  - `manager` (String) - Manager name
  - `joining_date` (String) - Format: "DD/MM/YYYY" or "DD-MM-YYYY"
  - `relieving_date` (String) - Format: "DD/MM/YYYY" or "DD-MM-YYYY"
  - `active_status` (String) - "T"/"t" (True/Active), "F"/"f" (False/Inactive)
  - `location` (String) - Work location

#### Scenario: Contact information
- **WHEN** providing contact details
- **THEN** system accepts:
  - `work_mobile` (String) - Office mobile number
  - `work_phone` (String) - Office phone number
  - `personal_mobile` (String) - Personal mobile number
  - `email` (String) - Personal email
  - `corporate_email` (String) - Corporate email address
  - `emergency_contact_number` (String) - Emergency contact

#### Scenario: Address information
- **WHEN** providing address
- **THEN** system accepts:
  - `city` (String) - City name
  - `zip` (String) - Postal code

#### Scenario: Compensation information
- **WHEN** providing salary details
- **THEN** system accepts:
  - `ctc` (Float) - Cost to Company (annual compensation)

---

### Requirement: Data Validation

Employee data SHALL be validated before persisting.

#### Scenario: Gender validation
- **WHEN** gender is provided
- **THEN** system accepts: "F", "f", "M", "m", "O", "o"
- **AND** converts to uppercase for storage
- **AND** rejects other values

#### Scenario: Marital status validation
- **WHEN** marital_status is provided
- **THEN** system accepts: "single", "married", "cohabitant", "widower", "divorced"
- **AND** rejects other values

#### Scenario: Active status validation
- **WHEN** active_status is provided
- **THEN** system accepts: "T", "t", "F", "f"
- **AND** converts to boolean (True/False)
- **AND** rejects other values

#### Scenario: Date format validation
- **WHEN** date fields are provided
- **THEN** system accepts formats: "DD/MM/YYYY" or "DD-MM-YYYY"
- **AND** validates dates are valid calendar dates
- **AND** converts to Odoo internal date format

#### Scenario: Email validation
- **WHEN** email or corporate_email is provided
- **THEN** system validates email format
- **AND** rejects invalid email addresses

---

### Requirement: Response Format

The API SHALL return consistent JSON responses.

#### Scenario: Successful creation
- **WHEN** employee is successfully created
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "message": "Employee created successfully",
      "employee_id": "EMP12345",
      "odoo_employee_id": 456
    }
  }
  ```

---

### Requirement: Audit Trail

All employee API operations SHALL be logged.

#### Scenario: API call logging
- **WHEN** employee API is called
- **THEN** system logs: timestamp, API user, operation, employee_id, status

---

## Integration Example

```bash
curl -X POST https://odoo.example.com/employee/fetch_employee_code \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "login": "api_user",
      "password": "api_key_hash",
      "record": {
        "name": "Jane Smith",
        "gender": "F",
        "date_of_birth": "15/03/1990",
        "job_position": "Sales Manager",
        "department": "Sales",
        "work_mobile": "9876543210",
        "corporate_email": "jane.smith@company.com",
        "joining_date": "01-06-2023",
        "active_status": "T",
        "ctc": 800000
      }
    }
  }'
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| MISSING_REQUIRED_FIELD | 400 | Required field missing |
| VALIDATION_ERROR | 400 | Field validation failed (gender, marital_status, date format) |
| INVALID_DATE | 400 | Date format invalid or date is not valid |
| INTERNAL_ERROR | 500 | Server error during processing |
