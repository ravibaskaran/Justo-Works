# Inventory Fetch API

## Purpose

Provide read-only API access to real estate inventory data including unit availability, pricing, floor plans, and property details. This API enables external portals, mobile applications, and partner systems to display current property inventory status.

## Scope

**Included:**
- Inventory data retrieval by project
- Inventory filtering by property type
- Unit availability status
- Pricing information
- Floor plans and property specifications

**Excluded:**
- Inventory creation/modification (UI-only operation)
- Booking/reservation operations (see booking-api)
- Payment processing
- Customer data access

---

## Requirements

### Requirement: Inventory Fetch Endpoint

The system SHALL provide a read-only API endpoint for retrieving inventory data.

#### Scenario: Endpoint specification
- **WHEN** accessing inventory fetch API
- **THEN** endpoint is available at `/inventory/fetch_record_details`
- **AND** endpoint accepts HTTP POST requests
- **AND** endpoint requires authentication with `inventory` scope

---

### Requirement: Request Parameters

The API SHALL accept filtering parameters to retrieve specific inventory data.

#### Scenario: Filter by project
- **WHEN** `project` parameter is provided
- **THEN** system returns inventory only for specified project
- **AND** project is identified by project code or ID

#### Scenario: Filter by type
- **WHEN** `type` parameter is provided
- **THEN** system returns inventory matching the property type
- **AND** type includes: "apartment", "villa", "plot", "commercial", etc.

#### Scenario: Fetch all inventory
- **WHEN** no filters are provided
- **THEN** system returns all available inventory across all projects
- **AND** results are paginated if count exceeds limit

---

### Requirement: Inventory Data Fields

The API SHALL return comprehensive inventory information for each unit.

#### Scenario: Unit identification
- **WHEN** retrieving inventory
- **THEN** each record includes:
  - `unit_id` - Unique unit identifier
  - `unit_number` - Display unit number (e.g., "A-101", "Villa-5")
  - `project_code` - Associated project identifier
  - `project_name` - Project display name

#### Scenario: Unit specifications
- **WHEN** retrieving unit details
- **THEN** response includes:
  - `property_type` - Type of property (apartment, villa, plot, etc.)
  - `floor_number` - Floor level
  - `facing` - Unit facing direction (North, South, East, West)
  - `carpet_area` - Carpet area in sq ft/sq m
  - `built_up_area` - Built-up area in sq ft/sq m
  - `super_built_up_area` - Super built-up area
  - `bedrooms` - Number of bedrooms (BHK configuration)
  - `bathrooms` - Number of bathrooms

#### Scenario: Pricing information
- **WHEN** retrieving pricing
- **THEN** response includes:
  - `base_price` - Unit base price
  - `final_price` - Final price including applicable charges
  - `price_per_sqft` - Rate per square foot
  - `currency` - Currency code (e.g., "INR")

#### Scenario: Availability status
- **WHEN** checking availability
- **THEN** response includes:
  - `status` - Availability status: "available", "booked", "sold", "blocked", "hold"
  - `available_from_date` - Date from which unit is available
  - `last_updated` - Timestamp of last status change

#### Scenario: Additional amenities
- **WHEN** unit has special features
- **THEN** response includes:
  - `parking_slots` - Number of parking spaces
  - `balconies` - Number of balconies
  - `amenities` - List of included amenities

---

### Requirement: Response Format

The API SHALL return inventory data in consistent JSON structure.

#### Scenario: Successful data retrieval
- **WHEN** inventory data is successfully retrieved
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "count": 50,
      "inventory": [
        {
          "unit_id": "U12345",
          "unit_number": "A-101",
          "project_code": "PROJ001",
          "project_name": "Green Valley Apartments",
          "property_type": "apartment",
          "bedrooms": 3,
          "carpet_area": 1250,
          "final_price": 5500000,
          "currency": "INR",
          "status": "available"
        },
        ...
      ]
    }
  }
  ```

#### Scenario: No results found
- **WHEN** no inventory matches filter criteria
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "count": 0,
      "inventory": [],
      "message": "No inventory found matching criteria"
    }
  }
  ```

#### Scenario: Invalid project
- **WHEN** project parameter specifies non-existent project
- **THEN** system returns 404 Not Found
- **AND** error message indicates project not found

---

### Requirement: Data Security and Access Control

Inventory data SHALL respect access control and pricing visibility rules.

#### Scenario: Public pricing
- **WHEN** inventory is marked for public display
- **THEN** API returns full pricing information

#### Scenario: Restricted pricing
- **WHEN** inventory pricing is restricted
- **THEN** API returns pricing only to authorized API keys
- **AND** unauthorized keys receive inventory without pricing

#### Scenario: Sold unit details
- **WHEN** retrieving sold units
- **THEN** customer details are not included in response
- **AND** only unit specifications and sold status are returned

---

### Requirement: Performance and Caching

The API SHALL deliver inventory data efficiently with appropriate caching.

#### Scenario: Response time
- **WHEN** fetching inventory data
- **THEN** API responds within 2 seconds for up to 1000 units
- **AND** larger datasets are paginated

#### Scenario: Caching strategy
- **WHEN** inventory data is requested
- **THEN** system uses caching layer for frequently accessed data
- **AND** cache is invalidated when inventory status changes

---

### Requirement: Audit Logging

All inventory fetch operations SHALL be logged for analytics.

#### Scenario: API access logging
- **WHEN** inventory API is called
- **THEN** system logs: timestamp, API user, project filter, type filter, result count

---

## Integration Example

```bash
# Fetch all inventory for a specific project
curl -X POST https://odoo.example.com/inventory/fetch_record_details \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "login": "api_user",
      "password": "api_key_hash",
      "project": "PROJ001",
      "type": "apartment"
    }
  }'
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| MISSING_CREDENTIALS | 400 | Authentication credentials not provided |
| INVALID_CREDENTIALS | 401 | Authentication failed |
| INSUFFICIENT_SCOPE | 403 | API key lacks `inventory` scope |
| PROJECT_NOT_FOUND | 404 | Specified project does not exist |
| INVALID_TYPE | 400 | Invalid property type specified |
| INTERNAL_ERROR | 500 | Server error during processing |

---

## Implementation Notes

- Inventory data sourced from real estate property management models
- Complex SQL queries may be used for efficient data aggregation
- Response includes only active projects unless explicitly requested
- Inventory status updated real-time when bookings/sales occur
- Pricing respects user access rights and project-specific visibility rules
