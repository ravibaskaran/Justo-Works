# Implementation Tasks - API Validation Fixes

## 1. Customer API Validation
- [ ] 1.1 Add required field validation (name, state_code, country_code)
- [ ] 1.2 Uncomment and fix state/country code validation (lines 718-722)
- [ ] 1.3 Add email format validation
- [ ] 1.4 Add phone number format validation
- [ ] 1.5 Return proper HTTP status codes (400, 404, 500)
- [ ] 1.6 Include customer_id and odoo_partner_id in success response

## 2. Channel Partner API Validation
- [ ] 2.1 Add required field validation (name, state_code, country_code, mobile)
- [ ] 2.2 Add state/country code validation
- [ ] 2.3 Add email format validation
- [ ] 2.4 Add RERA number format validation
- [ ] 2.5 Add mobile number format validation
- [ ] 2.6 Return proper HTTP status codes

## 3. Employee API Validation
- [ ] 3.1 Validate gender codes (F/f, M/m, O/o)
- [ ] 3.2 Validate marital status values
- [ ] 3.3 Validate active status (T/t, F/f)
- [ ] 3.4 Validate date formats (DD/MM/YYYY, DD-MM-YYYY)
- [ ] 3.5 Return proper HTTP status codes
- [ ] 3.6 Fix URL mismatch (/fetch_employee_code123 → /fetch_employee_code)

## 4. Create Validation Utility Module
- [ ] 4.1 Create `validation_utils.py` with reusable validators
- [ ] 4.2 Implement email_validator()
- [ ] 4.3 Implement phone_validator()
- [ ] 4.4 Implement state_country_validator()
- [ ] 4.5 Implement date_format_validator()
- [ ] 4.6 Implement required_fields_validator()

## 5. Standardize Error Responses
- [ ] 5.1 Create error response builder
- [ ] 5.2 Map validation errors to HTTP 400
- [ ] 5.3 Map not found errors to HTTP 404
- [ ] 5.4 Map server errors to HTTP 500
- [ ] 5.5 Include error details in response

## 6. Testing
- [ ] 6.1 Test required field validation
- [ ] 6.2 Test state/country code validation
- [ ] 6.3 Test email validation
- [ ] 6.4 Test phone validation
- [ ] 6.5 Test proper error codes returned
- [ ] 6.6 Test response format includes IDs

## 7. Documentation
- [ ] 7.1 Update API specifications with validation rules
- [ ] 7.2 Document error codes and responses
- [ ] 7.3 Create migration guide for API consumers
