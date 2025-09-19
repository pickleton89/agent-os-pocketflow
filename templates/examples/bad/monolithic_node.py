"""
Bad Example: Monolithic Node Antipatterns

⚠️ ANTIPATTERN WARNING: This file demonstrates what NOT to do in PocketFlow.
These examples violate the single responsibility principle and create
monolithic nodes that are hard to test, debug, and maintain.

DO NOT COPY THESE PATTERNS - Use templates/examples/good/ instead.
"""

from typing import Dict, Any, Optional, List
from pocketflow import SharedStore, Node, BatchNode
import requests
import json
from datetime import datetime


class ProcessAndValidateAndSendNode(Node):
    """
    ❌ ANTIPATTERN: Monolithic node with multiple responsibilities
    
    This node violates the single responsibility principle by:
    - Processing user data
    - Validating multiple data types
    - Sending emails
    - Updating databases
    - Generating reports
    - Making API calls
    
    Problems:
    1. Too many responsibilities (violates SRP)
    2. Hard to test individual components
    3. Difficult to reuse parts of functionality
    4. Error handling becomes complex
    5. Method is too long (>50 lines)
    6. Multiple LLM calls for different purposes
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare data for monolithic processing."""
        return {
            'user_data': shared.get('user_data'),
            'email_config': shared.get('email_config'),
            'api_config': shared.get('api_config'),
            'database_config': shared.get('database_config')
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Monolithic exec method doing everything
        
        This method is too long and handles multiple responsibilities.
        It should be split into focused nodes.
        """
        user_data = prep_result['user_data']
        email_config = prep_result['email_config']
        api_config = prep_result['api_config']
        database_config = prep_result['database_config']
        
        results = {}
        
        # ❌ RESPONSIBILITY 1: Data validation (should be separate node)
        validation_errors = []
        if not user_data.get('name'):
            validation_errors.append('Name is required')
        if not user_data.get('email') or '@' not in user_data['email']:
            validation_errors.append('Valid email is required')
        if user_data.get('age', 0) < 0:
            validation_errors.append('Age must be positive')
        
        if validation_errors:
            results['validation_errors'] = validation_errors
        else:
            results['validation_status'] = 'passed'
        
        # ❌ RESPONSIBILITY 2: Data processing (should be separate node)
        processed_data = {
            'id': user_data.get('id'),
            'name': user_data.get('name', '').title(),
            'email': user_data.get('email', '').lower(),
            'age': user_data.get('age', 0),
            'processed_at': datetime.now().isoformat()
        }
        
        # ❌ RESPONSIBILITY 3: External API call (should be separate AsyncNode)
        try:
            api_response = requests.post(
                api_config['url'],
                json=processed_data,
                headers={'Authorization': f"Bearer {api_config['token']}"},
                timeout=30
            )
            api_data = api_response.json()
            processed_data['external_id'] = api_data.get('id')
        except Exception as e:
            results['api_error'] = str(e)
        
        # ❌ RESPONSIBILITY 4: Database operations (should be separate AsyncNode)
        try:
            # Simulated database operation
            database_result = self._save_to_database(processed_data, database_config)
            results['database_id'] = database_result.get('id')
        except Exception as e:
            results['database_error'] = str(e)
        
        # ❌ RESPONSIBILITY 5: Email sending (should be separate node)
        if not validation_errors:
            try:
                email_result = self._send_welcome_email(processed_data, email_config)
                results['email_sent'] = email_result
            except Exception as e:
                results['email_error'] = str(e)
        
        # ❌ RESPONSIBILITY 6: Report generation (should be separate node)
        report = self._generate_user_report(processed_data)
        results['report'] = report
        
        # ❌ RESPONSIBILITY 7: File operations (should be separate node)
        try:
            report_path = f"/tmp/user_report_{processed_data['id']}.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            results['report_path'] = report_path
        except Exception as e:
            results['file_error'] = str(e)
        
        # ❌ RESPONSIBILITY 8: Analytics tracking (should be separate node)
        try:
            analytics_data = {
                'event': 'user_processed',
                'user_id': processed_data['id'],
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'validation_errors': len(validation_errors),
                    'api_success': 'api_error' not in results,
                    'email_sent': results.get('email_sent', False)
                }
            }
            # Simulated analytics call
            self._track_analytics(analytics_data)
        except Exception as e:
            results['analytics_error'] = str(e)
        
        # ❌ MULTIPLE LLM CALLS: Should be in separate nodes
        try:
            # LLM call 1: Content generation
            content_prompt = f"Generate a welcome message for {processed_data['name']}"
            welcome_message = self._call_llm(content_prompt)
            results['welcome_message'] = welcome_message
            
            # LLM call 2: Data classification
            classification_prompt = f"Classify this user data: {json.dumps(processed_data)}"
            user_classification = self._call_llm(classification_prompt)
            results['user_classification'] = user_classification
            
            # LLM call 3: Risk assessment
            risk_prompt = f"Assess risk level for user: {processed_data}"
            risk_assessment = self._call_llm(risk_prompt)
            results['risk_assessment'] = risk_assessment
            
        except Exception as e:
            results['llm_error'] = str(e)
        
        results['processed_data'] = processed_data
        return results
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Post method also becomes complex due to monolithic design."""
        # ❌ Complex routing logic due to multiple responsibilities
        shared['processed_user'] = exec_result.get('processed_data')
        shared['processing_results'] = exec_result
        
        # Too many possible error conditions to handle
        if 'validation_errors' in exec_result:
            return 'validation_failed'
        elif 'api_error' in exec_result:
            return 'api_failed' 
        elif 'database_error' in exec_result:
            return 'database_failed'
        elif 'email_error' in exec_result:
            return 'email_failed'
        elif 'file_error' in exec_result:
            return 'file_failed'
        elif 'analytics_error' in exec_result:
            return 'analytics_failed'
        elif 'llm_error' in exec_result:
            return 'llm_failed'
        
        return None
    
    def _save_to_database(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Complex database logic embedded in node."""
        # This should be in a utility function or separate service
        pass
    
    def _send_welcome_email(self, user_data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """❌ Email logic embedded in node."""
        # This should be in a separate email service node
        pass
    
    def _generate_user_report(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Report generation logic embedded in node."""
        # This should be in a separate report generation node
        pass
    
    def _track_analytics(self, data: Dict[str, Any]) -> None:
        """❌ Analytics logic embedded in node."""
        # This should be in a separate analytics node
        pass
    
    def _call_llm(self, prompt: str) -> str:
        """❌ Multiple LLM calls in one node."""
        # Each LLM call should be in a separate node for proper retry handling
        pass


class MegaBatchProcessor(BatchNode):
    """
    ❌ ANTIPATTERN: Monolithic batch node trying to do everything
    
    This batch node violates separation of concerns by:
    - Processing multiple data types in one batch
    - Mixing file operations with API calls
    - Handling both synchronous and asynchronous operations
    - Complex state sharing between batch items
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare for monolithic batch processing."""
        return {
            'files': shared.get('files', []),
            'api_data': shared.get('api_data', []),
            'emails': shared.get('emails', []),
            'reports': shared.get('reports', [])
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Processing different data types in one batch
        
        This violates the principle that batch nodes should process
        homogeneous collections with the same operations.
        """
        files = prep_result['files']
        api_data = prep_result['api_data']
        emails = prep_result['emails']
        reports = prep_result['reports']
        
        # ❌ State shared between different types of processing
        shared_state = {
            'processed_count': 0,
            'error_count': 0,
            'file_cache': {}
        }
        
        results = {
            'file_results': [],
            'api_results': [],
            'email_results': [],
            'report_results': []
        }
        
        # ❌ Processing different data types with different logic
        for file_path in files:
            try:
                # File processing logic
                content = self._process_file(file_path, shared_state)
                results['file_results'].append({
                    'file': file_path,
                    'content': content,
                    'success': True
                })
                shared_state['processed_count'] += 1
            except Exception as e:
                results['file_results'].append({
                    'file': file_path,
                    'error': str(e),
                    'success': False
                })
                shared_state['error_count'] += 1
        
        # ❌ Mixing API calls in the same batch loop
        for api_item in api_data:
            try:
                # API processing logic (should be in AsyncNode)
                response = self._make_api_call(api_item, shared_state)
                results['api_results'].append({
                    'item': api_item,
                    'response': response,
                    'success': True
                })
                shared_state['processed_count'] += 1
            except Exception as e:
                results['api_results'].append({
                    'item': api_item,
                    'error': str(e),
                    'success': False
                })
                shared_state['error_count'] += 1
        
        # ❌ Email processing mixed with other operations
        for email_data in emails:
            try:
                # Email sending logic
                result = self._send_email(email_data, shared_state)
                results['email_results'].append({
                    'email': email_data,
                    'result': result,
                    'success': True
                })
                shared_state['processed_count'] += 1
            except Exception as e:
                results['email_results'].append({
                    'email': email_data,
                    'error': str(e),
                    'success': False
                })
                shared_state['error_count'] += 1
        
        # ❌ Report generation mixed with other operations
        for report_config in reports:
            try:
                # Report generation logic
                report = self._generate_report(report_config, shared_state)
                results['report_results'].append({
                    'config': report_config,
                    'report': report,
                    'success': True
                })
                shared_state['processed_count'] += 1
            except Exception as e:
                results['report_results'].append({
                    'config': report_config,
                    'error': str(e),
                    'success': False
                })
                shared_state['error_count'] += 1
        
        results['summary'] = shared_state
        return results
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Complex post method due to multiple operation types."""
        # ❌ Complex result handling for multiple data types
        shared['batch_results'] = exec_result
        
        summary = exec_result['summary']
        total_items = (
            len(prep_result['files']) + 
            len(prep_result['api_data']) + 
            len(prep_result['emails']) + 
            len(prep_result['reports'])
        )
        
        success_rate = (summary['processed_count'] - summary['error_count']) / total_items
        
        # ❌ Complex routing due to multiple operation types
        if success_rate < 0.5:
            return 'batch_failed'
        elif summary['error_count'] > 0:
            return 'partial_success'
        
        return None
    
    def _process_file(self, file_path: str, shared_state: Dict[str, Any]) -> str:
        """❌ File processing logic embedded in batch node."""
        # This should be a separate file processing node
        pass
    
    def _make_api_call(self, api_item: Dict[str, Any], shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """❌ API logic in batch node (should be AsyncNode)."""
        # This should be in a separate AsyncNode
        pass
    
    def _send_email(self, email_data: Dict[str, Any], shared_state: Dict[str, Any]) -> bool:
        """❌ Email logic in batch node."""
        # This should be in a separate email node
        pass
    
    def _generate_report(self, config: Dict[str, Any], shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Report generation in batch node."""
        # This should be in a separate report generation node
        pass


class GodClassProcessingNode(Node):
    """
    ❌ ANTIPATTERN: God class that knows about everything
    
    This node violates encapsulation by:
    - Having knowledge of multiple external systems
    - Implementing multiple business domains
    - Having too many dependencies
    - Being impossible to test in isolation
    """
    
    def __init__(self):
        """❌ Too many dependencies and configurations."""
        super().__init__()
        # This node "knows" about too many external systems
        self.database_manager = None  # Should be injected
        self.email_service = None     # Should be injected
        self.payment_processor = None # Should be injected
        self.inventory_system = None  # Should be injected
        self.analytics_tracker = None # Should be injected
        self.notification_service = None # Should be injected
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare for god-class processing."""
        # ❌ Reading from too many SharedStore keys
        return {
            'user_data': shared.get('user_data'),
            'order_data': shared.get('order_data'),
            'inventory_data': shared.get('inventory_data'),
            'payment_data': shared.get('payment_data'),
            'shipping_data': shared.get('shipping_data'),
            'analytics_data': shared.get('analytics_data'),
            'notification_preferences': shared.get('notification_preferences'),
            'business_rules': shared.get('business_rules'),
            'system_config': shared.get('system_config')
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: God method that handles multiple business domains
        
        This method violates the single responsibility principle by
        handling user management, order processing, inventory, payments,
        shipping, analytics, and notifications all in one place.
        """
        # ❌ DOMAIN 1: User management
        user_result = self._handle_user_operations(prep_result['user_data'])
        
        # ❌ DOMAIN 2: Order processing  
        order_result = self._handle_order_operations(
            prep_result['order_data'], 
            prep_result['business_rules']
        )
        
        # ❌ DOMAIN 3: Inventory management
        inventory_result = self._handle_inventory_operations(
            prep_result['inventory_data'],
            order_result
        )
        
        # ❌ DOMAIN 4: Payment processing
        payment_result = self._handle_payment_operations(
            prep_result['payment_data'],
            order_result
        )
        
        # ❌ DOMAIN 5: Shipping calculations
        shipping_result = self._handle_shipping_operations(
            prep_result['shipping_data'],
            order_result,
            user_result
        )
        
        # ❌ DOMAIN 6: Analytics tracking
        analytics_result = self._handle_analytics_operations(
            prep_result['analytics_data'],
            user_result,
            order_result,
            payment_result
        )
        
        # ❌ DOMAIN 7: Notification sending
        notification_result = self._handle_notification_operations(
            prep_result['notification_preferences'],
            user_result,
            order_result,
            payment_result,
            shipping_result
        )
        
        # ❌ Complex interdependencies between domains
        if payment_result['status'] == 'failed':
            # Rollback inventory
            self._rollback_inventory(inventory_result)
            # Cancel shipping
            self._cancel_shipping(shipping_result)
            # Send failure notifications
            self._send_failure_notifications(notification_result, payment_result)
        
        return {
            'user_result': user_result,
            'order_result': order_result,
            'inventory_result': inventory_result,
            'payment_result': payment_result,
            'shipping_result': shipping_result,
            'analytics_result': analytics_result,
            'notification_result': notification_result,
            'overall_success': self._determine_overall_success([
                user_result, order_result, inventory_result,
                payment_result, shipping_result, notification_result
            ])
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """❌ Complex post method handling multiple domains."""
        # ❌ Updating too many SharedStore keys
        shared['user_result'] = exec_result['user_result']
        shared['order_result'] = exec_result['order_result']
        shared['inventory_result'] = exec_result['inventory_result']
        shared['payment_result'] = exec_result['payment_result']
        shared['shipping_result'] = exec_result['shipping_result']
        shared['analytics_result'] = exec_result['analytics_result']
        shared['notification_result'] = exec_result['notification_result']
        
        # ❌ Complex routing logic due to multiple failure modes
        if not exec_result['overall_success']:
            if exec_result['payment_result']['status'] == 'failed':
                return 'payment_failed'
            elif exec_result['inventory_result']['status'] == 'insufficient':
                return 'inventory_insufficient'
            elif exec_result['shipping_result']['status'] == 'unavailable':
                return 'shipping_unavailable'
            else:
                return 'processing_failed'
        
        return None
    
    def _handle_user_operations(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """❌ User domain logic in god class."""
        # This entire method should be a separate UserProcessingNode
        pass
    
    def _handle_order_operations(self, order_data: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Order domain logic in god class."""  
        # This entire method should be a separate OrderProcessingNode
        pass
    
    def _handle_inventory_operations(self, inventory_data: Dict[str, Any], order_result: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Inventory domain logic in god class."""
        # This entire method should be a separate InventoryNode
        pass
    
    def _handle_payment_operations(self, payment_data: Dict[str, Any], order_result: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Payment domain logic in god class."""
        # This entire method should be a separate PaymentNode
        pass
    
    def _handle_shipping_operations(self, shipping_data: Dict[str, Any], order_result: Dict[str, Any], user_result: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Shipping domain logic in god class."""
        # This entire method should be a separate ShippingNode
        pass
    
    def _handle_analytics_operations(self, analytics_data: Dict[str, Any], *results) -> Dict[str, Any]:
        """❌ Analytics domain logic in god class."""
        # This entire method should be a separate AnalyticsNode
        pass
    
    def _handle_notification_operations(self, preferences: Dict[str, Any], *results) -> Dict[str, Any]:
        """❌ Notification domain logic in god class."""
        # This entire method should be a separate NotificationNode
        pass
    
    # ❌ Too many private helper methods indicate too many responsibilities
    def _rollback_inventory(self, inventory_result: Dict[str, Any]) -> None:
        pass
    
    def _cancel_shipping(self, shipping_result: Dict[str, Any]) -> None:
        pass
    
    def _send_failure_notifications(self, notification_result: Dict[str, Any], payment_result: Dict[str, Any]) -> None:
        pass
    
    def _determine_overall_success(self, results: List[Dict[str, Any]]) -> bool:
        pass


# ============================================================================
# How to Fix These Antipatterns
# ============================================================================

"""
✅ CORRECT APPROACH: Split monolithic nodes into focused nodes

Instead of ProcessAndValidateAndSendNode, create:
1. DataValidationNode - only handles validation
2. DataProcessingNode - only handles data transformation  
3. ExternalAPINode - only handles API calls
4. DatabaseNode - only handles database operations
5. EmailNode - only handles email sending
6. ReportGenerationNode - only handles reports
7. FileOperationNode - only handles file I/O
8. AnalyticsNode - only handles analytics
9. LLMContentNode - only handles content generation
10. LLMClassificationNode - only handles classification
11. LLMRiskAssessmentNode - only handles risk assessment

Each node would have:
- Single responsibility
- Clear input/output contracts
- Independent testability
- Focused error handling
- Proper node type selection (Node vs AsyncNode vs BatchNode)

Example flow structure:
DataValidationNode -> DataProcessingNode -> ExternalAPINode -> DatabaseNode
                                         -> EmailNode
                                         -> ReportGenerationNode -> FileOperationNode
                                         -> AnalyticsNode

Benefits:
- Each node can be tested independently
- Failures are isolated and easier to debug
- Nodes can be reused in different flows
- Parallel execution is possible where appropriate
- Error handling is focused and clear
- Easier to maintain and modify individual components
"""

if __name__ == "__main__":
    print("⚠️  ANTIPATTERN EXAMPLES - DO NOT USE THESE PATTERNS")
    print("These examples show common mistakes in PocketFlow design.")
    print("See templates/examples/good/ for correct implementations.")
    
    # These examples are intentionally broken and serve as educational material
    # about what NOT to do in PocketFlow applications.