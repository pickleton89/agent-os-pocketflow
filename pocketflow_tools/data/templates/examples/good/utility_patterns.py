"""
Good Example: Utility Function Patterns

This example demonstrates the correct way to design utility functions in PocketFlow:
- Simple, focused functions with single responsibilities
- Pure functions without side effects
- Clear separation from business logic
- Proper error handling and testability
- External service abstraction
"""

from typing import Dict, Any, List, Optional, Union
import requests
import json
import re
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
import logging


# ============================================================================
# File Operation Utilities
# ============================================================================

def read_file_safe(file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
    """
    ✅ CORRECT: Simple file reading utility with error handling
    
    This function handles one specific task (reading files) and returns
    None on errors rather than raising exceptions, letting the calling
    node handle the decision logic.
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError):
        return None


def write_file_safe(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
    """
    ✅ CORRECT: Simple file writing utility with boolean success indicator
    
    Returns success/failure as a boolean, letting the calling node
    decide how to handle failures through branching.
    """
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except (PermissionError, OSError):
        return False


def list_files_with_extension(directory: Union[str, Path], extension: str) -> List[Path]:
    """
    ✅ CORRECT: Simple directory traversal utility
    
    Pure function that returns a list of files. No business logic,
    no complex error handling - just does one thing well.
    """
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return []
    
    return list(directory.glob(f"*.{extension.lstrip('.')}"))


def calculate_file_hash(file_path: Union[str, Path], algorithm: str = 'sha256') -> Optional[str]:
    """
    ✅ CORRECT: File hashing utility with configurable algorithm
    
    Single purpose function that calculates file hashes. Returns None
    on error rather than raising exceptions.
    """
    try:
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (FileNotFoundError, ValueError, OSError):
        return None


# ============================================================================
# Data Transformation Utilities
# ============================================================================

def normalize_text(text: str, options: Optional[Dict[str, bool]] = None) -> str:
    """
    ✅ CORRECT: Pure text transformation function
    
    No side effects, no business logic - just transforms input to output
    based on clear configuration options.
    """
    if not text or not isinstance(text, str):
        return ""
    
    options = options or {}
    result = text
    
    # Apply transformations based on options
    if options.get('strip_whitespace', True):
        result = result.strip()
    
    if options.get('normalize_whitespace', True):
        result = re.sub(r'\s+', ' ', result)
    
    if options.get('lower_case', False):
        result = result.lower()
    
    if options.get('remove_special_chars', False):
        result = re.sub(r'[^\w\s]', '', result)
    
    return result


def extract_email_domain(email: str) -> Optional[str]:
    """
    ✅ CORRECT: Simple extraction utility
    
    Single purpose function that extracts email domain.
    Returns None for invalid emails.
    """
    if not email or not isinstance(email, str):
        return None
    
    if '@' not in email:
        return None
    
    domain = email.split('@')[-1].strip().lower()
    return domain if domain else None


def validate_data_types(data: Dict[str, Any], schema: Dict[str, type]) -> Dict[str, bool]:
    """
    ✅ CORRECT: Data validation utility
    
    Pure function that validates data against a schema. Returns
    a clear result structure that nodes can use for decision making.
    """
    results = {}
    
    for field, expected_type in schema.items():
        if field in data:
            value = data[field]
            if expected_type == 'email':
                # Special case for email validation
                results[field] = bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(value)))
            else:
                results[field] = isinstance(value, expected_type)
        else:
            results[field] = False  # Missing field
    
    return results


def convert_timestamps(data: Dict[str, Any], timestamp_fields: List[str]) -> Dict[str, Any]:
    """
    ✅ CORRECT: Timestamp conversion utility
    
    Converts various timestamp formats to ISO format. Pure function
    that returns a new dictionary without modifying the input.
    """
    result = data.copy()
    
    for field in timestamp_fields:
        if field in result:
            timestamp_value = result[field]
            iso_timestamp = convert_to_iso_timestamp(timestamp_value)
            if iso_timestamp:
                result[field] = iso_timestamp
    
    return result


def convert_to_iso_timestamp(timestamp: Union[str, int, float, datetime]) -> Optional[str]:
    """
    ✅ CORRECT: Flexible timestamp conversion
    
    Handles multiple timestamp formats and converts to ISO format.
    Returns None if conversion fails.
    """
    try:
        if isinstance(timestamp, datetime):
            return timestamp.isoformat()
        elif isinstance(timestamp, (int, float)):
            # Unix timestamp
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            return dt.isoformat()
        elif isinstance(timestamp, str):
            # Try common string formats
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%d'
            ]
            for fmt in formats:
                try:
                    dt = datetime.strptime(timestamp, fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
        
        return None
    except (ValueError, TypeError, OSError):
        return None


# ============================================================================
# External Service Utilities
# ============================================================================

def make_http_request(url: str, method: str = 'GET', headers: Optional[Dict[str, str]] = None, 
                     data: Optional[Dict[str, Any]] = None, timeout: int = 30) -> Optional[Dict[str, Any]]:
    """
    ✅ CORRECT: HTTP request utility with clean interface
    
    Simple wrapper around HTTP requests. Returns structured result
    or None on failure. No business logic, just technical operation.
    """
    try:
        headers = headers or {}
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=timeout)
        else:
            return None  # Unsupported method
        
        return {
            'status_code': response.status_code,
            'success': response.status_code < 400,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            'headers': dict(response.headers)
        }
    except (requests.RequestException, json.JSONDecodeError, ValueError):
        return None


def call_external_api(endpoint: str, payload: Dict[str, Any], api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    ✅ CORRECT: External API wrapper
    
    Abstracts external API calls with authentication. Returns None on failure,
    letting the calling node handle error logic through branching.
    """
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    return make_http_request(endpoint, method='POST', headers=headers, data=payload)


def validate_api_response(response: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    ✅ CORRECT: API response validation
    
    Validates that an API response contains required fields.
    Simple boolean return for clear decision making.
    """
    if not response or not isinstance(response, dict):
        return False
    
    data = response.get('data', {})
    if not isinstance(data, dict):
        return False
    
    return all(field in data for field in required_fields)


# ============================================================================
# Configuration and Environment Utilities
# ============================================================================

def load_config_from_env(prefix: str = '') -> Dict[str, str]:
    """
    ✅ CORRECT: Environment configuration loader
    
    Loads configuration from environment variables with optional prefix.
    Pure function that reads environment state.
    """
    config = {}
    prefix = prefix.upper() + '_' if prefix else ''
    
    for key, value in os.environ.items():
        if key.startswith(prefix):
            config_key = key[len(prefix):].lower()
            config[config_key] = value
    
    return config


def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    ✅ CORRECT: Configuration merging utility
    
    Merges two configuration dictionaries with override precedence.
    Pure function that doesn't modify inputs.
    """
    result = base_config.copy()
    
    for key, value in override_config.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            # Recursive merge for nested dictionaries
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    
    return result


def validate_required_config(config: Dict[str, Any], required_keys: List[str]) -> Dict[str, bool]:
    """
    ✅ CORRECT: Configuration validation
    
    Checks that required configuration keys are present and non-empty.
    Returns validation results for node decision making.
    """
    results = {}
    
    for key in required_keys:
        if key in config:
            value = config[key]
            # Check if value is not None and not empty string
            results[key] = value is not None and value != ''
        else:
            results[key] = False
    
    return results


# ============================================================================
# Logging and Monitoring Utilities
# ============================================================================

def setup_structured_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """
    ✅ CORRECT: Logger setup utility
    
    Creates a structured logger with consistent formatting.
    Side effect is isolated and predictable.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def create_monitoring_payload(node_name: str, execution_time: float, success: bool, 
                            metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    ✅ CORRECT: Monitoring data creation
    
    Creates structured monitoring/telemetry payload. Pure function
    that formats data for external monitoring systems.
    """
    payload = {
        'node_name': node_name,
        'timestamp': datetime.utcnow().isoformat(),
        'execution_time': execution_time,
        'success': success,
        'metadata': metadata or {}
    }
    
    return payload


# ============================================================================
# Testing and Example Usage
# ============================================================================

def main():
    """
    ✅ CORRECT: Main function for testing utilities
    
    This demonstrates how utility functions should be testable
    independently of the PocketFlow framework.
    """
    print("=== Utility Functions Testing ===")
    
    # Test text normalization
    sample_text = "  Hello    World!  \n\n  Extra   spaces  "
    normalized = normalize_text(sample_text, {
        'strip_whitespace': True,
        'normalize_whitespace': True
    })
    print(f"Normalized text: '{normalized}'")
    
    # Test email domain extraction
    emails = ['user@example.com', 'invalid-email', 'admin@test.org']
    for email in emails:
        domain = extract_email_domain(email)
        print(f"Email: {email} -> Domain: {domain}")
    
    # Test data type validation
    test_data = {
        'name': 'John Doe',
        'age': 30,
        'email': 'john@example.com',
        'score': 'not-a-number'
    }
    schema = {
        'name': str,
        'age': int,
        'email': 'email',
        'score': int
    }
    validation_results = validate_data_types(test_data, schema)
    print(f"Validation results: {validation_results}")
    
    # Test timestamp conversion
    timestamp_data = {
        'created_at': '2024-01-15 10:30:00',
        'updated_at': 1705312200,  # Unix timestamp
        'other_field': 'not a timestamp'
    }
    converted = convert_timestamps(timestamp_data, ['created_at', 'updated_at'])
    print(f"Converted timestamps: {converted}")
    
    # Test configuration loading and merging
    base_config = {
        'host': 'localhost',
        'port': 8080,
        'database': {
            'name': 'testdb',
            'timeout': 30
        }
    }
    override_config = {
        'port': 9090,
        'database': {
            'timeout': 60,
            'pool_size': 10
        },
        'debug': True
    }
    merged = merge_configs(base_config, override_config)
    print(f"Merged config: {json.dumps(merged, indent=2)}")
    
    # Test monitoring payload creation
    monitoring_data = create_monitoring_payload(
        node_name='TestUtilityNode',
        execution_time=0.25,
        success=True,
        metadata={'items_processed': 10, 'cache_hits': 7}
    )
    print(f"Monitoring payload: {json.dumps(monitoring_data, indent=2)}")


if __name__ == "__main__":
    main()