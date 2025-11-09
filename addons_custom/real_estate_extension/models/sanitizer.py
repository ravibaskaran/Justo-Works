# -*- coding: utf-8 -*-
"""
Data Sanitization Utility for API Logging

This module provides utilities to sanitize sensitive data before logging.
Prevents exposure of passwords, API keys, PII, and other sensitive information.
"""

import re
import json
from typing import Any, Dict, List, Set, Tuple


class DataSanitizer:
    """
    Sanitizes sensitive data in dictionaries, lists, and strings.

    Handles:
    - Passwords and API keys
    - PII (Aadhar, PAN, bank accounts, DOB, phone numbers)
    - Configurable field patterns
    """

    # Sensitive field patterns (case-insensitive)
    SENSITIVE_PATTERNS = {
        # Authentication & Secrets
        'password': r'(password|passwd|pwd)',
        'api_key': r'(api[-_]?key|apikey|access[-_]?key)',
        'token': r'(token|bearer|auth[-_]?token)',
        'secret': r'(secret|private[-_]?key)',

        # Personal Identifiable Information (India-specific)
        'aadhar': r'(aadhar|aadhaar|uid)',
        'pan': r'(pan|pan[-_]?number|pan[-_]?card)',
        'bank_account': r'(account[-_]?number|acc[-_]?no|bank[-_]?acc)',
        'dob': r'(dob|date[-_]?of[-_]?birth|birth[-_]?date)',

        # Contact Information
        'phone': r'(phone|mobile|contact[-_]?number|cell)',
        'email': r'(email|e[-_]?mail)',
    }

    # Fields that should NEVER be sanitized
    WHITELIST_PATTERNS = {
        'name', 'title', 'description', 'notes', 'remarks',
        'status', 'type', 'category', 'code', 'reference'
    }

    def __init__(self):
        """Initialize sanitizer with compiled regex patterns"""
        self.compiled_patterns = {
            key: re.compile(pattern, re.IGNORECASE)
            for key, pattern in self.SENSITIVE_PATTERNS.items()
        }
        self.whitelist_set = set(self.WHITELIST_PATTERNS)
        self.found_sensitive = False

    def sanitize(self, data: Any) -> Tuple[Any, bool]:
        """
        Sanitize data recursively.

        Args:
            data: Data to sanitize (dict, list, string, or other)

        Returns:
            Tuple of (sanitized_data, contains_sensitive)
        """
        self.found_sensitive = False
        sanitized = self._sanitize_recursive(data)
        return sanitized, self.found_sensitive

    def _sanitize_recursive(self, data: Any, depth: int = 0) -> Any:
        """
        Recursively sanitize data structures.

        Args:
            data: Data to sanitize
            depth: Current recursion depth (max 10 to prevent infinite loops)

        Returns:
            Sanitized data
        """
        if depth > 10:
            return "[MAX_DEPTH_EXCEEDED]"

        if isinstance(data, dict):
            return self._sanitize_dict(data, depth)
        elif isinstance(data, (list, tuple)):
            return self._sanitize_list(data, depth)
        elif isinstance(data, str):
            return data  # Individual strings are sanitized based on context
        else:
            return data

    def _sanitize_dict(self, data: Dict, depth: int) -> Dict:
        """Sanitize dictionary by checking field names and values"""
        sanitized = {}
        for key, value in data.items():
            if self._is_whitelisted(key):
                # Whitelisted field - don't sanitize
                sanitized[key] = self._sanitize_recursive(value, depth + 1)
            elif self._is_sensitive_field(key):
                # Sensitive field - mask the value
                self.found_sensitive = True
                sanitized[key] = self._mask_value(key, value)
            else:
                # Regular field - continue recursion
                sanitized[key] = self._sanitize_recursive(value, depth + 1)
        return sanitized

    def _sanitize_list(self, data: List, depth: int) -> List:
        """Sanitize list by processing each element"""
        return [self._sanitize_recursive(item, depth + 1) for item in data]

    def _is_whitelisted(self, field_name: str) -> bool:
        """Check if field is whitelisted (never sanitize)"""
        return field_name.lower() in self.whitelist_set

    def _is_sensitive_field(self, field_name: str) -> bool:
        """Check if field name matches sensitive patterns"""
        for pattern_type, compiled_pattern in self.compiled_patterns.items():
            if compiled_pattern.search(field_name):
                return True
        return False

    def _mask_value(self, field_name: str, value: Any) -> str:
        """
        Mask sensitive value based on field type.

        Args:
            field_name: Name of the field
            value: Value to mask

        Returns:
            Masked value as string
        """
        if value is None or value == '':
            return ''

        value_str = str(value)

        # Determine masking strategy based on field pattern
        for pattern_type, compiled_pattern in self.compiled_patterns.items():
            if compiled_pattern.search(field_name):
                return self._apply_mask_pattern(pattern_type, value_str)

        # Default masking if no specific pattern matched
        return self._mask_default(value_str)

    def _apply_mask_pattern(self, pattern_type: str, value: str) -> str:
        """Apply specific masking pattern based on data type"""

        if pattern_type in ['password', 'api_key', 'token', 'secret']:
            # Show first 4 + last 4 chars, mask middle
            return self._mask_credential(value)

        elif pattern_type == 'aadhar':
            # Aadhar: XXXX XXXX XX34 (show last 4 digits)
            return self._mask_aadhar(value)

        elif pattern_type == 'pan':
            # PAN: XXXXXX5678 (show last 4 chars)
            return self._mask_pan(value)

        elif pattern_type == 'bank_account':
            # Bank Account: XXXXXXXXX1234 (show last 4 digits)
            return self._mask_bank_account(value)

        elif pattern_type == 'dob':
            # DOB: 1990-XX-XX (show only year)
            return self._mask_dob(value)

        elif pattern_type == 'phone':
            # Phone: +91 98XXX XXX45 (mask middle digits)
            return self._mask_phone(value)

        elif pattern_type == 'email':
            # Email: a***@example.com (mask local part)
            return self._mask_email(value)

        else:
            return self._mask_default(value)

    def _mask_credential(self, value: str) -> str:
        """Mask credentials: show first 4 + last 4 chars"""
        if len(value) <= 8:
            return '*' * len(value)
        return value[:4] + ('*' * (len(value) - 8)) + value[-4:]

    def _mask_aadhar(self, value: str) -> str:
        """Mask Aadhar: show only last 4 digits"""
        # Remove spaces and non-digits
        digits = re.sub(r'\D', '', value)
        if len(digits) >= 12:
            return 'XXXX XXXX ' + digits[-4:]
        elif len(digits) >= 4:
            return 'X' * (len(digits) - 4) + digits[-4:]
        else:
            return 'X' * len(digits)

    def _mask_pan(self, value: str) -> str:
        """Mask PAN: show only last 4 chars"""
        clean_value = value.strip().upper()
        if len(clean_value) >= 10:
            return 'X' * 6 + clean_value[-4:]
        elif len(clean_value) >= 4:
            return 'X' * (len(clean_value) - 4) + clean_value[-4:]
        else:
            return 'X' * len(clean_value)

    def _mask_bank_account(self, value: str) -> str:
        """Mask bank account: show only last 4 digits"""
        digits = re.sub(r'\D', '', value)
        if len(digits) >= 4:
            return 'X' * (len(digits) - 4) + digits[-4:]
        else:
            return 'X' * len(digits)

    def _mask_dob(self, value: str) -> str:
        """Mask DOB: show only year"""
        # Try to parse various date formats
        date_patterns = [
            r'(\d{4})-\d{2}-\d{2}',  # YYYY-MM-DD
            r'(\d{4})/\d{2}/\d{2}',  # YYYY/MM/DD
            r'\d{2}-\d{2}-(\d{4})',  # DD-MM-YYYY
            r'\d{2}/\d{2}/(\d{4})',  # DD/MM/YYYY
        ]

        for pattern in date_patterns:
            match = re.search(pattern, value)
            if match:
                year = match.group(1)
                return f'{year}-XX-XX'

        # If no pattern matched, mask everything
        return 'XXXX-XX-XX'

    def _mask_phone(self, value: str) -> str:
        """Mask phone: show country code and last 2 digits"""
        # Remove all non-digits except + at start
        clean = value.strip()

        # Check if has country code
        if clean.startswith('+'):
            country_match = re.match(r'(\+\d{1,3})\s*', clean)
            if country_match:
                country_code = country_match.group(1)
                digits = re.sub(r'\D', '', clean[len(country_code):])
                if len(digits) >= 2:
                    return f'{country_code} {"X" * (len(digits) - 2)}{digits[-2:]}'
                else:
                    return f'{country_code} {"X" * len(digits)}'

        # No country code
        digits = re.sub(r'\D', '', clean)
        if len(digits) >= 2:
            return 'X' * (len(digits) - 2) + digits[-2:]
        else:
            return 'X' * len(digits)

    def _mask_email(self, value: str) -> str:
        """Mask email: show first char + domain"""
        email_pattern = r'^([a-zA-Z0-9])[a-zA-Z0-9._-]*@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$'
        match = re.match(email_pattern, value.strip())

        if match:
            first_char = match.group(1)
            domain = match.group(2)
            return f'{first_char}***@{domain}'
        else:
            # Invalid email format - mask completely
            return 'X' * len(value)

    def _mask_default(self, value: str) -> str:
        """Default masking: show first 2 + last 2 chars"""
        if len(value) <= 4:
            return '*' * len(value)
        return value[:2] + ('*' * (len(value) - 4)) + value[-2:]


def sanitize_for_logging(data: Any) -> Tuple[str, bool]:
    """
    Convenience function to sanitize data and convert to JSON string.

    Args:
        data: Data to sanitize (dict, list, or other)

    Returns:
        Tuple of (json_string, contains_sensitive)
    """
    sanitizer = DataSanitizer()
    sanitized_data, contains_sensitive = sanitizer.sanitize(data)

    try:
        json_string = json.dumps(sanitized_data, indent=2, ensure_ascii=False)
    except (TypeError, ValueError):
        # If JSON serialization fails, convert to string
        json_string = str(sanitized_data)

    return json_string, contains_sensitive
