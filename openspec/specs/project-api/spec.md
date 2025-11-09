# Project Fetch API

## Purpose

Provide read-only API access to real estate project master data including project details, location information, amenities, and status. This API enables external systems to display project information and maintain synchronized project catalogs.

## Scope

**Included:**
- Project master data retrieval
- Project specifications and amenities
- Location and contact information
- Project status and timeline
- Developer/builder information

**Excluded:**
- Project creation/modification (UI-only operation)
- Project financial details (internal only)
- Unit-level inventory (see inventory-api)
- Sales/booking data

---

## Requirements

### Requirement: Project Fetch Endpoint

The system SHALL provide a read-only API endpoint for retrieving project data.

#### Scenario: Endpoint specification
- **WHEN** accessing project fetch API
- **THEN** endpoint is available at `/project/fetch_record_details`
- **AND** endpoint accepts HTTP POST requests
- **AND** endpoint requires authentication with `project` scope

---

### Requirement: Request Parameters

The API SHALL support fetching all projects or specific project details.

#### Scenario: Fetch all projects
- **WHEN** no project identifier is provided
- **THEN** system returns list of all active projects

#### Scenario: Fetch specific project
- **WHEN** project identifier is provided
- **THEN** system returns detailed information for that project only

#### Scenario: Filter by status
- **WHEN** status filter is provided
- **THEN** system returns only projects matching status: "active", "upcoming", "completed", "on-hold"

---

### Requirement: Project Data Fields

The API SHALL return comprehensive project information.

#### Scenario: Basic project information
- **WHEN** retrieving project data
- **THEN** each record includes:
  - `project_id` - Unique project identifier
  - `project_code` - Project code
  - `project_name` - Display name of project
  - `description` - Project description
  - `status` - Current project status
  - `developer_name` - Builder/developer name

#### Scenario: Location information
- **WHEN** retrieving location details
- **THEN** response includes:
  - `address` - Full project address
  - `city` - City name
  - `state` - State/province
  - `country` - Country
  - `pincode` - Postal code
  - `latitude` - GPS latitude
  - `longitude` - GPS longitude
  - `locality` - Locality/neighborhood name

#### Scenario: Project specifications
- **WHEN** retrieving specifications
- **THEN** response includes:
  - `total_units` - Total number of units in project
  - `available_units` - Currently available units count
  - `sold_units` - Number of sold units
  - `property_types` - List of property types (apartments, villas, etc.)
  - `total_area` - Total project land area
  - `number_of_floors` - Number of floors/blocks
  - `rera_number` - RERA registration number

#### Scenario: Amenities and features
- **WHEN** retrieving amenities
- **THEN** response includes:
  - `amenities` - List of project amenities (clubhouse, pool, gym, etc.)
  - `features` - Key features list
  - `specifications` - Construction specifications

#### Scenario: Timeline and status
- **WHEN** retrieving timeline
- **THEN** response includes:
  - `launch_date` - Project launch date
  - `expected_completion_date` - Estimated completion date
  - `possession_date` - Expected possession date
  - `rera_approved` - RERA approval status (true/false)

#### Scenario: Contact information
- **WHEN** retrieving contact details
- **THEN** response includes:
  - `sales_contact` - Sales team contact number
  - `email` - Project inquiry email
  - `website` - Project website URL

#### Scenario: Media and documents
- **WHEN** retrieving media
- **THEN** response includes:
  - `images` - List of project image URLs
  - `brochure_url` - Project brochure download link
  - `floor_plan_url` - Floor plan document link
  - `video_url` - Project video/walkthrough URL

---

### Requirement: Response Format

The API SHALL return project data in consistent JSON structure.

#### Scenario: Successful data retrieval
- **WHEN** project data is successfully retrieved
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "count": 1,
      "projects": [
        {
          "project_id": "PROJ001",
          "project_code": "GV2024",
          "project_name": "Green Valley Apartments",
          "status": "active",
          "city": "Bangalore",
          "total_units": 200,
          "available_units": 75,
          "rera_number": "RERA123456",
          "launch_date": "2024-01-15",
          "expected_completion_date": "2026-12-31",
          "amenities": ["Clubhouse", "Swimming Pool", "Gym", "Garden"],
          "sales_contact": "1800-XXX-XXXX",
          "images": ["url1", "url2"]
        }
      ]
    }
  }
  ```

#### Scenario: No projects found
- **WHEN** no projects match filter criteria
- **THEN** response includes:
  ```json
  {
    "result": {
      "status": "success",
      "count": 0,
      "projects": [],
      "message": "No projects found"
    }
  }
  ```

#### Scenario: Invalid project ID
- **WHEN** project ID does not exist
- **THEN** system returns 404 Not Found
- **AND** error message indicates project not found

---

### Requirement: Data Security

Project data SHALL respect visibility and access control rules.

#### Scenario: Public project data
- **WHEN** project is marked for public display
- **THEN** API returns full project information

#### Scenario: Internal project data
- **WHEN** project is marked internal/confidential
- **THEN** API returns only to authorized keys
- **AND** unauthorized requests receive access denied error

---

### Requirement: Performance

The API SHALL deliver project data efficiently.

#### Scenario: Response time
- **WHEN** fetching project list
- **THEN** API responds within 1 second for up to 100 projects

#### Scenario: Caching
- **WHEN** project data is requested
- **THEN** frequently accessed projects are served from cache
- **AND** cache invalidates when project data is updated

---

### Requirement: Audit Logging

All project fetch operations SHALL be logged.

#### Scenario: API access logging
- **WHEN** project API is called
- **THEN** system logs: timestamp, API user, project filter, result count

---

## Integration Example

```bash
# Fetch all active projects
curl -X POST https://odoo.example.com/project/fetch_record_details \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "login": "api_user",
      "password": "api_key_hash"
    }
  }'
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| MISSING_CREDENTIALS | 400 | Authentication credentials not provided |
| INVALID_CREDENTIALS | 401 | Authentication failed |
| INSUFFICIENT_SCOPE | 403 | API key lacks `project` scope |
| PROJECT_NOT_FOUND | 404 | Specified project does not exist |
| INTERNAL_ERROR | 500 | Server error during processing |

---

## Implementation Notes

- Project data sourced from project master models
- Images and documents served from Odoo filestore or CDN
- RERA compliance information prominently included
- Project status automatically updated based on timeline and inventory
- Media URLs use secure signed URLs with expiration
