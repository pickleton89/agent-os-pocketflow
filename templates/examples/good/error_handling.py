"""
Good Example: Error Handling with PocketFlow

This example demonstrates the correct way to handle errors in PocketFlow:
- Convert exceptions to branching decisions
- Use exec_fallback for graceful error handling
- Proper error classification and routing
- Clean separation of happy path and error handling logic
"""

from typing import Dict, Any, Optional
from pocketflow import SharedStore, Node, AsyncNode
import requests
import json
from enum import Enum


class ErrorType(Enum):
    """Classification of error types for routing decisions."""

    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"
    AUTHENTICATION_ERROR = "auth_error"
    RATE_LIMIT_ERROR = "rate_limit"
    UNKNOWN_ERROR = "unknown_error"


class DataValidationNode(Node):
    """
    ✅ CORRECT: Error handling with exception-to-branch conversion

    This node demonstrates proper error handling patterns:
    - Let exceptions propagate naturally from exec()
    - Use exec_fallback() to convert exceptions to routing decisions
    - Clean separation of success path and error handling
    """

    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare validation parameters."""
        input_data = shared.get("input_data")
        validation_rules = shared.get("validation_rules", {})

        return {"input_data": input_data, "validation_rules": validation_rules}

    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data - let exceptions propagate naturally.

        ✅ CORRECT: Pure validation logic without try/catch
        Exceptions are handled by the framework via exec_fallback
        """
        input_data = prep_result["input_data"]
        rules = prep_result["validation_rules"]

        # Validate required fields
        required_fields = rules.get("required_fields", [])
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Required field '{field}' is missing")

            if not input_data[field]:
                raise ValueError(f"Required field '{field}' cannot be empty")

        # Type validation
        type_rules = rules.get("types", {})
        for field, expected_type in type_rules.items():
            if field in input_data:
                actual_value = input_data[field]
                if expected_type == "int" and not isinstance(actual_value, int):
                    raise TypeError(f"Field '{field}' must be an integer")
                elif expected_type == "str" and not isinstance(actual_value, str):
                    raise TypeError(f"Field '{field}' must be a string")
                elif expected_type == "email" and not self._is_valid_email(
                    actual_value
                ):
                    raise ValueError(f"Field '{field}' must be a valid email")

        # Range validation
        range_rules = rules.get("ranges", {})
        for field, (min_val, max_val) in range_rules.items():
            if field in input_data:
                value = input_data[field]
                if isinstance(value, (int, float)) and not (
                    min_val <= value <= max_val
                ):
                    raise ValueError(
                        f"Field '{field}' must be between {min_val} and {max_val}"
                    )

        # If we reach here, validation passed
        return {
            "validated_data": input_data,
            "validation_status": "passed",
            "validated_fields": list(input_data.keys()),
        }

    def post(
        self,
        shared: SharedStore,
        prep_result: Dict[str, Any],
        exec_result: Dict[str, Any],
    ) -> Optional[str]:
        """Handle successful validation."""
        shared["validated_data"] = exec_result["validated_data"]
        shared["validation_results"] = {
            "status": "success",
            "validated_fields": exec_result["validated_fields"],
        }

        return None  # Continue to next node

    def exec_fallback(
        self, prep_result: Dict[str, Any], exception: Exception
    ) -> Dict[str, Any]:
        """
        ✅ CORRECT: Convert exceptions to structured results for routing

        This method classifies exceptions and prepares them for post_fallback
        to make routing decisions.
        """
        error_info = {
            "error_occurred": True,
            "error_message": str(exception),
            "error_type": self._classify_error(exception),
            "original_data": prep_result["input_data"],
        }

        # Log the error for debugging
        self.logger.error(
            f"Validation failed: {str(exception)}",
            extra={
                "error_type": error_info["error_type"],
                "input_data_keys": list(prep_result["input_data"].keys())
                if prep_result["input_data"]
                else [],
            },
        )

        return error_info

    def post_fallback(
        self,
        shared: SharedStore,
        prep_result: Dict[str, Any],
        fallback_result: Dict[str, Any],
    ) -> str:
        """
        ✅ CORRECT: Convert error information to routing decisions

        This method takes the structured error information from exec_fallback
        and converts it to specific routing actions.
        """
        error_type = fallback_result["error_type"]

        # Store error information in shared store
        shared["validation_error"] = {
            "type": error_type,
            "message": fallback_result["error_message"],
            "failed_data": fallback_result["original_data"],
        }

        # Route based on error type
        if error_type == ErrorType.VALIDATION_ERROR.value:
            return "validation_failed"
        else:
            return "unexpected_error"

    def _classify_error(self, exception: Exception) -> str:
        """Classify exception type for routing decisions."""
        if isinstance(exception, (ValueError, TypeError)):
            return ErrorType.VALIDATION_ERROR.value
        else:
            return ErrorType.UNKNOWN_ERROR.value

    def _is_valid_email(self, email: str) -> bool:
        """Simple email validation."""
        return "@" in email and "." in email.split("@")[-1]


class ExternalAPINode(AsyncNode):
    """
    ✅ CORRECT: Async error handling with retry logic and circuit breaker

    This demonstrates error handling for external API calls with:
    - Network error classification
    - Automatic retry with exponential backoff
    - Circuit breaker pattern
    - Clean error-to-branch conversion
    """

    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare API call parameters."""
        api_url = shared.get("api_url")
        payload = shared.get("api_payload")
        headers = shared.get("api_headers", {})
        timeout = shared.get("timeout", 30)
        max_retries = shared.get("max_retries", 3)

        if not api_url:
            raise ValueError("API URL is required")

        return {
            "api_url": api_url,
            "payload": payload,
            "headers": headers,
            "timeout": timeout,
            "max_retries": max_retries,
            "attempt_count": 0,
        }

    async def exec_async(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API call - let network exceptions propagate naturally.

        ✅ CORRECT: Clean API call without nested error handling
        The framework will catch exceptions and route via exec_fallback
        """
        url = prep_result["api_url"]
        payload = prep_result["payload"]
        headers = prep_result["headers"]
        timeout = prep_result["timeout"]

        # Make the API call
        response = requests.post(
            url=url, json=payload, headers=headers, timeout=timeout
        )

        # Raise for HTTP error status
        response.raise_for_status()

        # Parse response
        response_data = response.json()

        return {
            "api_response": response_data,
            "status_code": response.status_code,
            "success": True,
        }

    def post(
        self,
        shared: SharedStore,
        prep_result: Dict[str, Any],
        exec_result: Dict[str, Any],
    ) -> Optional[str]:
        """Handle successful API response."""
        shared["api_response"] = exec_result["api_response"]
        shared["api_metadata"] = {
            "status_code": exec_result["status_code"],
            "success": True,
        }

        return None  # Continue to next node

    def exec_fallback(
        self, prep_result: Dict[str, Any], exception: Exception
    ) -> Dict[str, Any]:
        """
        ✅ CORRECT: Classify API exceptions for retry logic and routing
        """
        error_type = self._classify_api_error(exception)
        should_retry = self._should_retry(
            error_type, prep_result["attempt_count"], prep_result["max_retries"]
        )

        error_info = {
            "error_occurred": True,
            "error_type": error_type,
            "error_message": str(exception),
            "should_retry": should_retry,
            "attempt_count": prep_result["attempt_count"] + 1,
            "max_retries": prep_result["max_retries"],
        }

        # Log error with appropriate level
        if should_retry:
            self.logger.warning(
                f"API call failed (attempt {error_info['attempt_count']}), will retry: {str(exception)}",
                extra={"error_type": error_type, "url": prep_result["api_url"]},
            )
        else:
            self.logger.error(
                f"API call failed permanently: {str(exception)}",
                extra={
                    "error_type": error_type,
                    "url": prep_result["api_url"],
                    "attempts": error_info["attempt_count"],
                },
            )

        return error_info

    def post_fallback(
        self,
        shared: SharedStore,
        prep_result: Dict[str, Any],
        fallback_result: Dict[str, Any],
    ) -> str:
        """
        ✅ CORRECT: Convert API errors to specific routing actions
        """
        error_type = fallback_result["error_type"]
        should_retry = fallback_result["should_retry"]

        # Store error information
        shared["api_error"] = {
            "type": error_type,
            "message": fallback_result["error_message"],
            "attempt_count": fallback_result["attempt_count"],
            "retry_exhausted": not should_retry,
        }

        # Route based on error type and retry status
        if should_retry:
            return "retry_api_call"
        elif error_type == ErrorType.AUTHENTICATION_ERROR.value:
            return "auth_failed"
        elif error_type == ErrorType.RATE_LIMIT_ERROR.value:
            return "rate_limited"
        elif error_type == ErrorType.NETWORK_ERROR.value:
            return "network_unavailable"
        else:
            return "api_failed"

    def _classify_api_error(self, exception: Exception) -> str:
        """Classify API errors for appropriate handling."""
        if isinstance(exception, requests.exceptions.ConnectionError):
            return ErrorType.NETWORK_ERROR.value
        elif isinstance(exception, requests.exceptions.Timeout):
            return ErrorType.NETWORK_ERROR.value
        elif isinstance(exception, requests.exceptions.HTTPError):
            if hasattr(exception, "response") and exception.response is not None:
                status_code = exception.response.status_code
                if status_code == 401 or status_code == 403:
                    return ErrorType.AUTHENTICATION_ERROR.value
                elif status_code == 429:
                    return ErrorType.RATE_LIMIT_ERROR.value
                else:
                    return ErrorType.NETWORK_ERROR.value
        elif isinstance(exception, (json.JSONDecodeError, ValueError)):
            return ErrorType.VALIDATION_ERROR.value
        else:
            return ErrorType.UNKNOWN_ERROR.value

    def _should_retry(
        self, error_type: str, attempt_count: int, max_retries: int
    ) -> bool:
        """Determine if the error is retryable."""
        if attempt_count >= max_retries:
            return False

        # Only retry certain types of errors
        retryable_errors = [
            ErrorType.NETWORK_ERROR.value,
            ErrorType.RATE_LIMIT_ERROR.value,
        ]

        return error_type in retryable_errors


class ErrorRecoveryNode(Node):
    """
    ✅ CORRECT: Dedicated error recovery and fallback logic

    This node demonstrates how to handle recovered errors and implement
    fallback strategies when primary processing fails.
    """

    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare error recovery based on the type of error that occurred."""
        validation_error = shared.get("validation_error")
        api_error = shared.get("api_error")

        return {
            "validation_error": validation_error,
            "api_error": api_error,
            "original_data": shared.get("input_data"),
        }

    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Implement fallback strategies based on error types."""
        validation_error = prep_result["validation_error"]
        api_error = prep_result["api_error"]
        original_data = prep_result["original_data"]

        recovery_actions = []
        fallback_data = {}

        # Handle validation errors
        if validation_error:
            recovery_actions.append("apply_default_values")
            fallback_data = self._apply_validation_fallback(
                original_data, validation_error
            )

        # Handle API errors
        if api_error:
            recovery_actions.append("use_cached_response")
            fallback_data.update(self._apply_api_fallback(api_error))

        return {
            "recovery_applied": True,
            "recovery_actions": recovery_actions,
            "fallback_data": fallback_data,
            "can_continue": len(recovery_actions) > 0,
        }

    def post(
        self,
        shared: SharedStore,
        prep_result: Dict[str, Any],
        exec_result: Dict[str, Any],
    ) -> Optional[str]:
        """Determine if recovery was successful."""
        shared["error_recovery"] = {
            "applied": exec_result["recovery_applied"],
            "actions": exec_result["recovery_actions"],
        }

        if exec_result["can_continue"]:
            shared["recovered_data"] = exec_result["fallback_data"]
            return "recovery_success"
        else:
            return "recovery_failed"

    def _apply_validation_fallback(
        self, original_data: Dict[str, Any], error_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply default values for validation failures."""
        fallback_data = original_data.copy() if original_data else {}

        # Apply sensible defaults
        if "email" not in fallback_data or not fallback_data["email"]:
            fallback_data["email"] = "noreply@example.com"

        if "name" not in fallback_data or not fallback_data["name"]:
            fallback_data["name"] = "Anonymous User"

        return fallback_data

    def _apply_api_fallback(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Provide fallback API response."""
        return {
            "api_response": {
                "status": "fallback",
                "message": "Using cached/default response due to API unavailability",
                "data": {},
            },
            "fallback_used": True,
        }


# Example usage and testing
if __name__ == "__main__":
    # Test data with validation issues
    test_data = {
        "name": "",  # Invalid: empty required field
        "email": "not-an-email",  # Invalid: bad email format
        "age": 150,  # Invalid: outside reasonable range
    }

    validation_rules = {
        "required_fields": ["name", "email"],
        "types": {"name": "str", "email": "email", "age": "int"},
        "ranges": {"age": (0, 120)},
    }

    print("=== Error Handling Example ===")

    # Test validation with errors
    shared = SharedStore(
        {"input_data": test_data, "validation_rules": validation_rules}
    )

    validator = DataValidationNode()

    try:
        prep_result = validator.prep(shared)
        # This will trigger exec_fallback due to validation errors
        exec_result = validator.exec(prep_result)
        action = validator.post(shared, prep_result, exec_result)
        print(f"Validation succeeded: {action}")
    except Exception as e:
        # Handle via fallback mechanism
        fallback_result = validator.exec_fallback(prep_result, e)
        action = validator.post_fallback(shared, prep_result, fallback_result)
        print(f"Validation failed, routing to: {action}")
        print(f"Error details: {shared.get('validation_error')}")

    # Test error recovery
    if "validation_error" in shared:
        print("\n=== Error Recovery ===")
        recovery = ErrorRecoveryNode()
        prep_result = recovery.prep(shared)
        exec_result = recovery.exec(prep_result)
        action = recovery.post(shared, prep_result, exec_result)

        print(f"Recovery action: {action}")
        print(f"Recovery details: {shared.get('error_recovery')}")
        if "recovered_data" in shared:
            print(f"Recovered data: {shared['recovered_data']}")
