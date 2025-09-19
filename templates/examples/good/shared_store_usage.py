"""
Good Example: SharedStore Usage Patterns

This example demonstrates the correct way to use SharedStore in PocketFlow:
- Clear data schemas and access patterns
- Proper isolation of data access in prep() and post()
- No SharedStore access in exec() methods
- Clean data flow and state management
"""

from typing import Dict, Any, Optional
from pocketflow import SharedStore, Node
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessingMetadata:
    """Structured metadata for processing operations."""
    node_name: str
    timestamp: datetime
    processing_time: float
    success: bool


class SharedStoreSchemaNode(Node):
    """
    ✅ CORRECT: Well-defined SharedStore schema and access patterns
    
    This node demonstrates:
    - Clear documentation of SharedStore schema
    - Data access only in prep() and post()
    - Structured data with clear naming conventions
    - No direct SharedStore access in exec()
    """
    
    # Define the SharedStore schema this node expects/produces
    REQUIRED_KEYS = ['user_data', 'processing_config']
    PRODUCES_KEYS = ['processed_user', 'processing_metadata']
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """
        ✅ CORRECT: All SharedStore access in prep()
        
        This method reads from SharedStore and prepares data for exec().
        It validates the schema and extracts only what exec() needs.
        """
        # Validate required keys exist
        for key in self.REQUIRED_KEYS:
            if key not in shared:
                raise ValueError(f"Required SharedStore key '{key}' is missing")
        
        user_data = shared['user_data']
        config = shared['processing_config']
        
        # Extract and validate user data
        if not isinstance(user_data, dict):
            raise TypeError("user_data must be a dictionary")
        
        required_user_fields = ['id', 'name', 'email']
        for field in required_user_fields:
            if field not in user_data:
                raise ValueError(f"Required user field '{field}' is missing")
        
        # Prepare processing configuration
        processing_options = {
            'normalize_name': config.get('normalize_name', True),
            'validate_email': config.get('validate_email', True),
            'add_metadata': config.get('add_metadata', True),
            'timestamp_format': config.get('timestamp_format', '%Y-%m-%d %H:%M:%S')
        }
        
        # Return only what exec() needs - no SharedStore reference
        return {
            'user_data': user_data,
            'processing_options': processing_options,
            'start_time': datetime.now()
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ✅ CORRECT: Pure processing with no SharedStore access
        
        This method only uses data from prep_result and returns
        processed data. No SharedStore access allowed here.
        """
        user_data = prep_result['user_data']
        options = prep_result['processing_options']
        start_time = prep_result['start_time']
        
        # Process user data based on options
        processed_user = {
            'id': user_data['id'],
            'original_name': user_data['name'],
            'email': user_data['email']
        }
        
        # Apply processing options
        if options['normalize_name']:
            processed_user['normalized_name'] = self._normalize_name(user_data['name'])
        
        if options['validate_email']:
            processed_user['email_valid'] = self._validate_email(user_data['email'])
            processed_user['email_domain'] = user_data['email'].split('@')[-1] if '@' in user_data['email'] else None
        
        # Create processing metadata
        processing_time = (datetime.now() - start_time).total_seconds()
        metadata = ProcessingMetadata(
            node_name=self.__class__.__name__,
            timestamp=datetime.now(),
            processing_time=processing_time,
            success=True
        )
        
        return {
            'processed_user': processed_user,
            'processing_metadata': metadata,
            'execution_stats': {
                'processing_time': processing_time,
                'fields_processed': len(processed_user),
                'normalization_applied': options['normalize_name'],
                'validation_applied': options['validate_email']
            }
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """
        ✅ CORRECT: All SharedStore updates in post()
        
        This method takes the results from exec() and updates SharedStore.
        It follows clear naming conventions and structured data storage.
        """
        # Store processed user data
        shared['processed_user'] = exec_result['processed_user']
        
        # Store processing metadata using structured format
        metadata = exec_result['processing_metadata']
        shared['processing_metadata'] = {
            'node_name': metadata.node_name,
            'timestamp': metadata.timestamp.isoformat(),
            'processing_time': metadata.processing_time,
            'success': metadata.success
        }
        
        # Store execution statistics for monitoring
        shared['execution_stats'] = exec_result['execution_stats']
        
        # Add to processing history (append to list)
        if 'processing_history' not in shared:
            shared['processing_history'] = []
        
        shared['processing_history'].append({
            'node': self.__class__.__name__,
            'timestamp': metadata.timestamp.isoformat(),
            'duration': metadata.processing_time,
            'user_id': exec_result['processed_user']['id']
        })
        
        # Route based on processing results
        if not exec_result['processed_user'].get('email_valid', True):
            return "email_invalid"
        
        return None  # Continue to next node
    
    def _normalize_name(self, name: str) -> str:
        """Normalize user name."""
        return ' '.join(word.capitalize() for word in name.strip().split())
    
    def _validate_email(self, email: str) -> bool:
        """Simple email validation."""
        return '@' in email and '.' in email.split('@')[-1]


class DataAggregatorNode(Node):
    """
    ✅ CORRECT: Aggregating data from multiple SharedStore keys
    
    This demonstrates how to properly aggregate data from different
    sources in SharedStore while maintaining clean access patterns.
    """
    
    REQUIRED_KEYS = ['processed_user', 'processing_history', 'external_data']
    PRODUCES_KEYS = ['user_profile', 'aggregation_summary']
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare data aggregation by reading from multiple SharedStore sources."""
        # Get processed user data
        processed_user = shared.get('processed_user', {})
        if not processed_user:
            raise ValueError("No processed user data available for aggregation")
        
        # Get processing history
        processing_history = shared.get('processing_history', [])
        
        # Get external data (could be from previous API calls)
        external_data = shared.get('external_data', {})
        
        # Get any additional context
        user_preferences = shared.get('user_preferences', {})
        system_config = shared.get('system_config', {})
        
        return {
            'processed_user': processed_user,
            'processing_history': processing_history,
            'external_data': external_data,
            'user_preferences': user_preferences,
            'system_config': system_config,
            'aggregation_timestamp': datetime.now()
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate data from multiple sources into a comprehensive user profile."""
        processed_user = prep_result['processed_user']
        history = prep_result['processing_history']
        external_data = prep_result['external_data']
        preferences = prep_result['user_preferences']
        
        # Create comprehensive user profile
        user_profile = {
            'basic_info': {
                'id': processed_user.get('id'),
                'name': processed_user.get('normalized_name', processed_user.get('original_name')),
                'email': processed_user.get('email'),
                'email_domain': processed_user.get('email_domain'),
                'email_valid': processed_user.get('email_valid', True)
            },
            'processing_info': {
                'total_processing_events': len(history),
                'last_processed': max((h['timestamp'] for h in history), default=None),
                'processing_nodes_used': list(set(h['node'] for h in history))
            },
            'external_info': external_data,
            'preferences': preferences
        }
        
        # Calculate aggregation statistics
        aggregation_summary = {
            'profile_completeness': self._calculate_completeness(user_profile),
            'data_sources': {
                'processed_user': bool(processed_user),
                'processing_history': len(history) > 0,
                'external_data': bool(external_data),
                'user_preferences': bool(preferences)
            },
            'aggregation_timestamp': prep_result['aggregation_timestamp'].isoformat(),
            'total_fields_aggregated': self._count_profile_fields(user_profile)
        }
        
        return {
            'user_profile': user_profile,
            'aggregation_summary': aggregation_summary
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Store aggregated user profile and summary."""
        # Store the comprehensive user profile
        shared['user_profile'] = exec_result['user_profile']
        shared['aggregation_summary'] = exec_result['aggregation_summary']
        
        # Update system-wide statistics
        if 'system_stats' not in shared:
            shared['system_stats'] = {
                'total_profiles_created': 0,
                'avg_profile_completeness': 0,
                'profiles_by_domain': {}
            }
        
        stats = shared['system_stats']
        stats['total_profiles_created'] += 1
        
        # Update average completeness
        completeness = exec_result['aggregation_summary']['profile_completeness']
        current_avg = stats['avg_profile_completeness']
        total_profiles = stats['total_profiles_created']
        stats['avg_profile_completeness'] = ((current_avg * (total_profiles - 1)) + completeness) / total_profiles
        
        # Track by email domain
        email_domain = exec_result['user_profile']['basic_info'].get('email_domain')
        if email_domain:
            domain_count = stats['profiles_by_domain'].get(email_domain, 0)
            stats['profiles_by_domain'][email_domain] = domain_count + 1
        
        # Route based on profile completeness
        if completeness < 0.5:
            return "incomplete_profile"
        elif completeness < 0.8:
            return "partial_profile"
        
        return None  # Complete profile, continue
    
    def _calculate_completeness(self, profile: Dict[str, Any]) -> float:
        """Calculate profile completeness percentage."""
        total_fields = 0
        filled_fields = 0
        
        def count_fields(obj, parent_key=''):
            nonlocal total_fields, filled_fields
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, dict):
                        count_fields(value, f"{parent_key}.{key}")
                    else:
                        total_fields += 1
                        if value and value != '':
                            filled_fields += 1
            elif isinstance(obj, list):
                total_fields += 1
                if obj:
                    filled_fields += 1
        
        count_fields(profile)
        return filled_fields / total_fields if total_fields > 0 else 0.0
    
    def _count_profile_fields(self, profile: Dict[str, Any]) -> int:
        """Count total fields in profile."""
        count = 0
        
        def count_recursive(obj):
            nonlocal count
            if isinstance(obj, dict):
                count += len(obj)
                for value in obj.values():
                    if isinstance(value, (dict, list)):
                        count_recursive(value)
            elif isinstance(obj, list):
                count += len(obj)
                for item in obj:
                    if isinstance(item, (dict, list)):
                        count_recursive(item)
        
        count_recursive(profile)
        return count


class SharedStoreValidatorNode(Node):
    """
    ✅ CORRECT: SharedStore validation and cleanup
    
    This demonstrates how to validate SharedStore state and perform cleanup
    while following proper access patterns.
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Validate SharedStore state and prepare cleanup operations."""
        # Define expected schema
        expected_schema = {
            'user_profile': dict,
            'processing_metadata': dict,
            'system_stats': dict
        }
        
        validation_results = {}
        cleanup_tasks = []
        
        # Validate schema compliance
        for key, expected_type in expected_schema.items():
            if key in shared:
                if not isinstance(shared[key], expected_type):
                    validation_results[key] = f"Type mismatch: expected {expected_type.__name__}, got {type(shared[key]).__name__}"
                else:
                    validation_results[key] = "valid"
            else:
                validation_results[key] = "missing"
                cleanup_tasks.append(f"create_default_{key}")
        
        # Check for orphaned data
        expected_keys = set(expected_schema.keys())
        actual_keys = set(shared.keys())
        orphaned_keys = actual_keys - expected_keys
        
        if orphaned_keys:
            cleanup_tasks.append(f"remove_orphaned_keys: {list(orphaned_keys)}")
        
        return {
            'validation_results': validation_results,
            'cleanup_tasks': cleanup_tasks,
            'schema_compliance': all(result == "valid" for result in validation_results.values()),
            'orphaned_keys': list(orphaned_keys)
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process validation results and prepare cleanup actions."""
        validation_results = prep_result['validation_results']
        cleanup_tasks = prep_result['cleanup_tasks']
        
        # Determine validation status
        validation_status = "passed" if prep_result['schema_compliance'] else "failed"
        
        # Prepare default values for missing keys
        default_values = {}
        if 'user_profile' in validation_results and validation_results['user_profile'] in ["missing", "type_mismatch"]:
            default_values['user_profile'] = {
                'basic_info': {},
                'processing_info': {},
                'external_info': {},
                'preferences': {}
            }
        
        if 'processing_metadata' in validation_results and validation_results['processing_metadata'] in ["missing", "type_mismatch"]:
            default_values['processing_metadata'] = {
                'node_name': 'unknown',
                'timestamp': datetime.now().isoformat(),
                'processing_time': 0.0,
                'success': False
            }
        
        if 'system_stats' in validation_results and validation_results['system_stats'] in ["missing", "type_mismatch"]:
            default_values['system_stats'] = {
                'total_profiles_created': 0,
                'avg_profile_completeness': 0.0,
                'profiles_by_domain': {}
            }
        
        return {
            'validation_status': validation_status,
            'validation_details': validation_results,
            'cleanup_required': len(cleanup_tasks) > 0,
            'cleanup_tasks': cleanup_tasks,
            'default_values': default_values,
            'orphaned_keys': prep_result['orphaned_keys']
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Apply cleanup operations and update SharedStore state."""
        # Apply default values for missing/invalid keys
        for key, default_value in exec_result['default_values'].items():
            shared[key] = default_value
        
        # Remove orphaned keys (with caution)
        orphaned_keys = exec_result['orphaned_keys']
        for key in orphaned_keys:
            if key.startswith('temp_') or key.startswith('debug_'):
                # Only remove temporary or debug keys automatically
                del shared[key]
        
        # Store validation results
        shared['validation_report'] = {
            'status': exec_result['validation_status'],
            'details': exec_result['validation_details'],
            'cleanup_applied': exec_result['cleanup_required'],
            'cleanup_tasks': exec_result['cleanup_tasks'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Route based on validation results
        if exec_result['validation_status'] == "failed":
            return "schema_validation_failed"
        elif exec_result['cleanup_required']:
            return "cleanup_applied"
        
        return None  # All good, continue


# Example usage and testing
if __name__ == "__main__":
    print("=== SharedStore Usage Patterns Example ===")
    
    # Initialize SharedStore with sample data
    shared = SharedStore({
        'user_data': {
            'id': 'user123',
            'name': 'john doe',
            'email': 'john.doe@example.com'
        },
        'processing_config': {
            'normalize_name': True,
            'validate_email': True,
            'add_metadata': True
        },
        'external_data': {
            'account_type': 'premium',
            'signup_date': '2024-01-15'
        },
        'user_preferences': {
            'theme': 'dark',
            'notifications': True
        }
    })
    
    print(f"Initial SharedStore keys: {list(shared.keys())}")
    
    # Test schema node
    schema_node = SharedStoreSchemaNode()
    prep_result = schema_node.prep(shared)
    exec_result = schema_node.exec(prep_result)
    action = schema_node.post(shared, prep_result, exec_result)
    
    print("\nAfter schema processing:")
    print(f"  Action: {action}")
    print(f"  SharedStore keys: {list(shared.keys())}")
    print(f"  Processed user: {shared.get('processed_user', {}).get('normalized_name')}")
    
    # Test aggregation node
    aggregator = DataAggregatorNode()
    prep_result = aggregator.prep(shared)
    exec_result = aggregator.exec(prep_result)
    action = aggregator.post(shared, prep_result, exec_result)
    
    print("\nAfter aggregation:")
    print(f"  Action: {action}")
    print(f"  Profile completeness: {shared.get('aggregation_summary', {}).get('profile_completeness', 0):.2%}")
    print(f"  System stats: {shared.get('system_stats', {})}")
    
    # Test validation node
    validator = SharedStoreValidatorNode()
    prep_result = validator.prep(shared)
    exec_result = validator.exec(prep_result)
    action = validator.post(shared, prep_result, exec_result)
    
    print("\nAfter validation:")
    print(f"  Action: {action}")
    print(f"  Validation status: {shared.get('validation_report', {}).get('status')}")
    print(f"  Final SharedStore keys: {list(shared.keys())}")