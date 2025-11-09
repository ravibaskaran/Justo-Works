# -*- coding: utf-8 -*-
"""
Data Validation Utilities for API Endpoints

This module provides reusable validators for API input validation.
Ensures data quality and prevents invalid data from entering the system.
"""

import re
from typing import Tuple, List, Any, Optional
from odoo import http
from odoo.http import request


class DataValidator:
    """
    Comprehensive data validation utilities.

    Provides validators for:
    - Email addresses
    - Phone numbers
    - State and country codes
    - Date formats
    - Required fields
    """

    # Email regex pattern (RFC 5322 simplified)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    # Phone patterns (India-specific, extensible)
    PHONE_PATTERNS = {
        'india': re.compile(r'^\+?91[-\s]?[6-9]\d{9}$|^[6-9]\d{9}$'),
        'international': re.compile(r'^\+?[1-9]\d{1,14}$'),  # E.164 format
    }

    # Date format patterns
    DATE_FORMATS = [
        (r'^\d{2}/\d{2}/\d{4}$', '%d/%m/%Y'),  # DD/MM/YYYY
        (r'^\d{2}-\d{2}-\d{4}$', '%d-%m-%Y'),  # DD-MM-YYYY
        (r'^\d{4}-\d{2}-\d{2}$', '%Y-%m-%d'),  # YYYY-MM-DD (ISO)
    ]

    def __init__(self, env=None):
        """
        Initialize validator.

        Args:
            env: Odoo environment (optional, defaults to request.env)
        """
        self.env = env or (request.env if request else None)

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not email or not email.strip():
            return True, ''  # Empty email is valid (optional field)

        email = email.strip()

        if not self.EMAIL_PATTERN.match(email):
            return False, f"Invalid email format: '{email}'. Expected format: user@example.com"

        # Additional checks
        if len(email) > 254:  # RFC 5321 max length
            return False, f"Email too long (max 254 characters): '{email}'"

        local_part = email.split('@')[0]
        if len(local_part) > 64:  # RFC 5321 local part max
            return False, f"Email local part too long (max 64 characters): '{email}'"

        return True, ''

    def validate_phone(self, phone: str, country: str = 'india') -> Tuple[bool, str]:
        """
        Validate phone number format.

        Args:
            phone: Phone number to validate
            country: Country code for validation rules (default: 'india')

        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not phone or not phone.strip():
            return True, ''  # Empty phone is valid (optional field)

        phone = phone.strip()

        # Get pattern for country
        pattern = self.PHONE_PATTERNS.get(country.lower(), self.PHONE_PATTERNS['international'])

        if not pattern.match(phone):
            if country.lower() == 'india':
                return False, f"Invalid Indian phone number: '{phone}'. Expected format: +91-9876543210 or 9876543210 (10 digits starting with 6-9)"
            else:
                return False, f"Invalid phone number: '{phone}'. Expected E.164 format (e.g., +1234567890)"

        return True, ''

    def validate_state_country(self, state_code: Optional[str], country_code: Optional[str]) -> Tuple[bool, str, Any, Any]:
        """
        Validate state and country codes against Odoo database.

        Args:
            state_code: State code to validate (can be None)
            country_code: Country code to validate (can be None)

        Returns:
            Tuple of (is_valid: bool, error_message: str, country_record, state_record)
        """
        if not self.env:
            return False, "Environment not available for validation", None, None

        country_record = None
        state_record = None

        # Validate country code
        if country_code:
            country_record = self.env['res.country'].sudo().search(
                [('code', '=', country_code.upper())],
                limit=1
            )
            if not country_record:
                return False, f"Invalid country code: '{country_code}'. Country not found in system.", None, None

        # Validate state code (requires valid country)
        if state_code:
            if not country_record:
                return False, "State code provided but country code is missing or invalid.", None, None

            state_record = self.env['res.country.state'].sudo().search(
                [('code', '=', state_code.upper()), ('country_id', '=', country_record.id)],
                limit=1
            )
            if not state_record:
                return False, f"Invalid state code: '{state_code}' for country '{country_code}'. State not found in system.", country_record, None

        return True, '', country_record, state_record

    def validate_date_format(self, date_string: str) -> Tuple[bool, str, Optional[str]]:
        """
        Validate date format and convert to ISO format (YYYY-MM-DD).

        Args:
            date_string: Date string to validate

        Returns:
            Tuple of (is_valid: bool, error_message: str, iso_date: str or None)
        """
        if not date_string or not date_string.strip():
            return True, '', None  # Empty date is valid (optional field)

        date_string = date_string.strip()

        from datetime import datetime

        for pattern, date_format in self.DATE_FORMATS:
            if re.match(pattern, date_string):
                try:
                    parsed_date = datetime.strptime(date_string, date_format)
                    iso_date = parsed_date.strftime('%Y-%m-%d')
                    return True, '', iso_date
                except ValueError as e:
                    return False, f"Invalid date value: '{date_string}'. {str(e)}", None

        # No pattern matched
        return False, f"Invalid date format: '{date_string}'. Expected formats: DD/MM/YYYY, DD-MM-YYYY, or YYYY-MM-DD", None

    def validate_required_fields(self, data: dict, required_fields: List[str]) -> Tuple[bool, str, List[str]]:
        """
        Validate that all required fields are present and not empty.

        Args:
            data: Dictionary of data to validate
            required_fields: List of required field names

        Returns:
            Tuple of (is_valid: bool, error_message: str, missing_fields: List[str])
        """
        missing_fields = []

        for field in required_fields:
            value = data.get(field)

            # Check if field is missing or empty
            if value is None or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)

        if missing_fields:
            fields_str = ', '.join(missing_fields)
            return False, f"Missing required fields: {fields_str}", missing_fields

        return True, '', []

    def validate_gender(self, gender: str) -> Tuple[bool, str, Optional[str]]:
        """
        Validate and normalize gender value.

        Args:
            gender: Gender code (F, M, O or full names)

        Returns:
            Tuple of (is_valid: bool, error_message: str, normalized_value: str or None)
        """
        if not gender or not gender.strip():
            return True, '', None  # Empty gender is valid (optional field)

        gender_upper = gender.strip().upper()

        # Map codes to Odoo values
        gender_map = {
            'M': 'male',
            'MALE': 'male',
            'F': 'female',
            'FEMALE': 'female',
            'O': 'other',
            'OTHER': 'other',
        }

        normalized = gender_map.get(gender_upper)

        if not normalized:
            return False, f"Invalid gender: '{gender}'. Valid values: M/Male, F/Female, O/Other", None

        return True, '', normalized

    def validate_marital_status(self, status: str) -> Tuple[bool, str, Optional[str]]:
        """
        Validate marital status value.

        Args:
            status: Marital status

        Returns:
            Tuple of (is_valid: bool, error_message: str, normalized_value: str or None)
        """
        if not status or not status.strip():
            return True, '', None  # Empty is valid (optional field)

        status_lower = status.strip().lower()

        valid_statuses = ['single', 'married', 'cohabitant', 'widower', 'divorced']

        if status_lower not in valid_statuses:
            return False, f"Invalid marital status: '{status}'. Valid values: {', '.join(valid_statuses)}", None

        return True, '', status_lower

    def validate_boolean_flag(self, value: Any, field_name: str = 'field') -> Tuple[bool, str, Optional[bool]]:
        """
        Validate and normalize boolean flag (T/F, True/False, 1/0).

        Args:
            value: Value to validate
            field_name: Name of the field (for error messages)

        Returns:
            Tuple of (is_valid: bool, error_message: str, boolean_value: bool or None)
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            return True, '', None  # Empty is valid (optional field)

        # Handle boolean type
        if isinstance(value, bool):
            return True, '', value

        # Handle string type
        if isinstance(value, str):
            value_upper = value.strip().upper()
            if value_upper in ('T', 'TRUE', '1', 'YES', 'Y'):
                return True, '', True
            elif value_upper in ('F', 'FALSE', '0', 'NO', 'N'):
                return True, '', False
            else:
                return False, f"Invalid {field_name}: '{value}'. Valid values: T/True/1, F/False/0", None

        # Handle numeric type
        if isinstance(value, (int, float)):
            return True, '', bool(value)

        return False, f"Invalid {field_name}: '{value}'. Expected boolean value.", None


# Convenience functions for direct use

def validate_email(email: str) -> Tuple[bool, str]:
    """Convenience function for email validation"""
    validator = DataValidator()
    return validator.validate_email(email)


def validate_phone(phone: str, country: str = 'india') -> Tuple[bool, str]:
    """Convenience function for phone validation"""
    validator = DataValidator()
    return validator.validate_phone(phone, country)


def validate_required_fields(data: dict, required_fields: List[str]) -> Tuple[bool, str, List[str]]:
    """Convenience function for required fields validation"""
    validator = DataValidator()
    return validator.validate_required_fields(data, required_fields)


def validate_date_format(date_string: str) -> Tuple[bool, str, Optional[str]]:
    """Convenience function for date validation"""
    validator = DataValidator()
    return validator.validate_date_format(date_string)
