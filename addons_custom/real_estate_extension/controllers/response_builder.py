# -*- coding: utf-8 -*-
"""
Standard API Response Builder

Provides consistent response format across all API endpoints with proper HTTP status codes.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class APIResponseBuilder:
    """
    Build standardized API responses with proper HTTP status codes.

    Response Format:
    {
        "status": "success|error",
        "code": 200|201|400|404|500,
        "message": "Human-readable message",
        "data": {...},  # For success responses
        "errors": [...],  # For error responses
        "timestamp": "2025-11-09T12:34:56"
    }
    """

    @staticmethod
    def success(data: Any = None, message: str = "Operation successful", code: int = 200) -> Dict:
        """
        Build success response.

        Args:
            data: Response data (dict, list, or any JSON-serializable type)
            message: Success message
            code: HTTP status code (200 for read/update, 201 for create)

        Returns:
            Standardized success response dict
        """
        response = {
            'status': 'success',
            'code': code,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }

        if data is not None:
            response['data'] = data

        return response

    @staticmethod
    def created(data: Any = None, message: str = "Resource created successfully", resource_id: Any = None) -> Dict:
        """
        Build success response for resource creation (HTTP 201).

        Args:
            data: Response data
            message: Success message
            resource_id: ID of created resource

        Returns:
            Standardized creation response dict with HTTP 201
        """
        response_data = data or {}

        # Include resource ID if provided
        if resource_id is not None and isinstance(response_data, dict):
            if 'id' not in response_data:
                response_data['id'] = resource_id

        return APIResponseBuilder.success(
            data=response_data,
            message=message,
            code=201
        )

    @staticmethod
    def error(message: str, code: int = 400, errors: Optional[List[str]] = None, data: Any = None) -> Dict:
        """
        Build error response.

        Args:
            message: Error message
            code: HTTP status code (400/404/500)
            errors: List of detailed error messages
            data: Additional error context data

        Returns:
            Standardized error response dict
        """
        response = {
            'status': 'error',
            'code': code,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }

        if errors:
            response['errors'] = errors

        if data is not None:
            response['data'] = data

        return response

    @staticmethod
    def bad_request(message: str = "Invalid request", errors: Optional[List[str]] = None, data: Any = None) -> Dict:
        """
        Build HTTP 400 Bad Request response.

        Use for:
        - Validation errors
        - Missing required fields
        - Invalid data format
        - Business rule violations

        Args:
            message: Error message
            errors: List of validation errors
            data: Additional context

        Returns:
            HTTP 400 error response
        """
        return APIResponseBuilder.error(
            message=message,
            code=400,
            errors=errors,
            data=data
        )

    @staticmethod
    def not_found(message: str = "Resource not found", resource_type: str = None, resource_id: Any = None) -> Dict:
        """
        Build HTTP 404 Not Found response.

        Use for:
        - Record not found by ID
        - Endpoint not found
        - Resource doesn't exist

        Args:
            message: Error message
            resource_type: Type of resource (e.g., "Customer", "Employee")
            resource_id: ID that was not found

        Returns:
            HTTP 404 error response
        """
        data = {}
        if resource_type:
            data['resource_type'] = resource_type
        if resource_id is not None:
            data['resource_id'] = resource_id

        return APIResponseBuilder.error(
            message=message,
            code=404,
            data=data if data else None
        )

    @staticmethod
    def server_error(message: str = "Internal server error", exception: Exception = None) -> Dict:
        """
        Build HTTP 500 Internal Server Error response.

        Use for:
        - Unexpected exceptions
        - Database errors
        - System errors

        Args:
            message: Error message
            exception: Exception object (for logging, not exposed to client)

        Returns:
            HTTP 500 error response
        """
        # Don't expose exception details to client for security
        # Log the exception separately
        return APIResponseBuilder.error(
            message=message,
            code=500
        )

    @staticmethod
    def unauthorized(message: str = "Authentication required") -> Dict:
        """
        Build HTTP 401 Unauthorized response.

        Use for:
        - Missing credentials
        - Invalid API key
        - Expired token

        Args:
            message: Error message

        Returns:
            HTTP 401 error response
        """
        return APIResponseBuilder.error(
            message=message,
            code=401
        )

    @staticmethod
    def forbidden(message: str = "Access denied") -> Dict:
        """
        Build HTTP 403 Forbidden response.

        Use for:
        - Insufficient permissions
        - Invalid login
        - Scope mismatch

        Args:
            message: Error message

        Returns:
            HTTP 403 error response
        """
        return APIResponseBuilder.error(
            message=message,
            code=403
        )

    @staticmethod
    def validation_error(field_errors: Dict[str, str], message: str = "Validation failed") -> Dict:
        """
        Build validation error response with field-specific errors.

        Args:
            field_errors: Dict of {field_name: error_message}
            message: Overall error message

        Returns:
            HTTP 400 error response with field errors

        Example:
            validation_error({
                'email': 'Invalid email format',
                'phone': 'Phone number too short'
            })
        """
        errors = [f"{field}: {error}" for field, error in field_errors.items()]

        return APIResponseBuilder.bad_request(
            message=message,
            errors=errors,
            data={'field_errors': field_errors}
        )


# Convenience functions for backwards compatibility with existing code

def build_success_response(data: Any = None, code: int = 200) -> Dict:
    """Build success response (backward compatible)"""
    return APIResponseBuilder.success(data=data, code=code)


def build_error_response(message: str, code: int = 400) -> Dict:
    """Build error response (backward compatible)"""
    return APIResponseBuilder.error(message=message, code=code)


def build_legacy_response(data: Any, status: str, code: int) -> Dict:
    """
    Build response in legacy format for compatibility.

    Legacy format:
    {
        'data': ...,
        'status': 'Success|Failed',
        'code': ...
    }

    Args:
        data: Response data
        status: 'Success' or 'Failed'
        code: HTTP status code

    Returns:
        Legacy format response
    """
    return {
        'data': data,
        'status': status,
        'code': code
    }
