"""
Bad Example: Lifecycle Method Violations

⚠️ ANTIPATTERN WARNING: This file demonstrates what NOT to do in PocketFlow.
These examples show violations of the prep/exec/post lifecycle pattern,
improper method responsibilities, and SharedStore access violations.

DO NOT COPY THESE PATTERNS - Use templates/examples/good/ instead.
"""

from typing import Dict, Any, Optional, List
from pocketflow import SharedStore, Node, AsyncNode, BatchNode
import requests
import json
import time
import logging
from datetime import datetime


class SharedStoreViolationNode(Node):
    """
    ❌ ANTIPATTERN: Direct SharedStore access in exec() method
    
    This node violates the lifecycle pattern by:
    - Accessing SharedStore directly in exec()
    - Bypassing the prep/exec/post data flow
    - Making testing and isolation impossible
    - Breaking the framework's retry mechanisms
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare should provide all data exec() needs."""
        # ❌ Only providing partial data, forcing exec() to access SharedStore
        return {
            'user_id': shared.get('user_id'),
            # Missing other required data that exec() will need
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Direct SharedStore access in exec()
        
        exec() should only use prep_result parameter, never self.shared
        """
        user_id = prep_result['user_id']
        
        # ❌ VIOLATION: Direct access to SharedStore in exec()
        user_profile = self.shared.get('user_profile', {})  # WRONG!
        user_preferences = self.shared['user_preferences']   # WRONG!
        
        # ❌ VIOLATION: Reading from SharedStore during execution
        if 'processing_config' in self.shared:
            config = self.shared['processing_config']        # WRONG!
        else:
            config = {}
        
        # ❌ VIOLATION: Writing to SharedStore during execution
        self.shared['processing_started_at'] = datetime.now().isoformat()  # WRONG!
        
        # Process user data
        processed_data = {
            'user_id': user_id,
            'profile': user_profile,
            'preferences': user_preferences,
            'config': config
        }
        
        # ❌ VIOLATION: More SharedStore access during processing
        if self.shared.get('enable_logging', True):          # WRONG!
            self.shared['processing_log'] = []               # WRONG!
            self.shared['processing_log'].append({           # WRONG!
                'step': 'data_processed',
                'timestamp': datetime.now().isoformat()
            })
        
        # ❌ VIOLATION: Conditional SharedStore updates in exec
        if processed_data['profile'].get('tier') == 'premium':
            self.shared['premium_processing_applied'] = True  # WRONG!
        
        return processed_data
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Post method becomes less useful when exec() violates lifecycle."""
        # exec() already wrote to SharedStore, making post() redundant
        shared['processed_user'] = exec_result
        return None


class ComputationInPrepNode(Node):
    """
    ❌ ANTIPATTERN: Complex computation in prep() method
    
    This node violates prep() responsibilities by:
    - Performing complex computations in prep()
    - Making LLM calls in prep()
    - Doing work that should be in exec()
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: prep() doing computation instead of data access
        
        prep() should only read from SharedStore and prepare data.
        All computation should happen in exec().
        """
        user_data = shared.get('user_data', {})
        business_rules = shared.get('business_rules', {})
        
        # ❌ VIOLATION: Complex computation in prep()
        risk_score = 0.0
        if user_data.get('age', 0) < 25:
            risk_score += 0.2
        if user_data.get('income', 0) < 30000:
            risk_score += 0.3
        if len(user_data.get('previous_addresses', [])) > 5:
            risk_score += 0.1
        
        # ❌ VIOLATION: Complex business logic in prep()
        credit_worthiness = 'good'
        if risk_score > 0.5:
            credit_worthiness = 'poor'
        elif risk_score > 0.3:
            credit_worthiness = 'fair'
        
        # ❌ VIOLATION: LLM call in prep() (should be in exec() for proper retry)
        user_summary = f"User {user_data.get('name')} has {credit_worthiness} creditworthiness"
        try:
            # This should be in exec()!
            enhanced_summary = self._call_llm_for_summary(user_summary)
        except Exception:
            enhanced_summary = user_summary
        
        # ❌ VIOLATION: File operations in prep() (should be in exec())
        try:
            with open(f"/tmp/user_{user_data.get('id', 'unknown')}.json", 'w') as f:
                json.dump(user_data, f)
        except Exception:
            pass
        
        # ❌ VIOLATION: External API call in prep() (should be in exec())
        try:
            external_data = requests.get(f"https://api.example.com/users/{user_data.get('id')}")
            external_info = external_data.json()
        except Exception:
            external_info = {}
        
        return {
            'user_data': user_data,
            'business_rules': business_rules,
            'computed_risk_score': risk_score,      # This computation should be in exec()
            'credit_worthiness': credit_worthiness,  # This logic should be in exec()
            'enhanced_summary': enhanced_summary,    # This LLM call should be in exec()
            'external_info': external_info           # This API call should be in exec()
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Exec becomes trivial when prep() does all the work."""
        # ❌ exec() now has nothing meaningful to do because prep() did everything
        return {
            'result': 'processed',
            'risk_score': prep_result['computed_risk_score'],
            'creditworthiness': prep_result['credit_worthiness']
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Store results."""
        shared['user_processed'] = exec_result
        return None
    
    def _call_llm_for_summary(self, summary: str) -> str:
        """❌ LLM call that should be in exec() method."""
        # This should be in exec() for proper framework retry handling
        return f"Enhanced: {summary}"


class PostMethodViolationNode(Node):
    """
    ❌ ANTIPATTERN: Complex computation and external calls in post() method
    
    This node violates post() responsibilities by:
    - Performing complex computations in post()
    - Making external API calls in post()
    - Doing work that should be in exec()
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare user processing data."""
        return {
            'user_data': shared.get('user_data'),
            'processing_config': shared.get('processing_config')
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Simple exec() that returns basic processing."""
        user_data = prep_result['user_data']
        return {
            'processed_user': {
                'id': user_data.get('id'),
                'name': user_data.get('name', '').title(),
                'processed_at': datetime.now().isoformat()
            }
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """
        ❌ ANTIPATTERN: Complex computation and external operations in post()
        
        post() should only update SharedStore and determine routing.
        All computation should be in exec().
        """
        processed_user = exec_result['processed_user']
        
        # Store the basic result
        shared['processed_user'] = processed_user
        
        # ❌ VIOLATION: Complex computation in post()
        config = prep_result['processing_config']
        if config.get('calculate_metrics', False):
            # This computation should be in exec()!
            metrics = {
                'processing_duration': time.time() - shared.get('start_time', time.time()),
                'data_quality_score': len([k for k, v in processed_user.items() if v]) / len(processed_user),
                'completeness_percentage': (len(processed_user.keys()) / 10) * 100  # Assuming 10 total fields
            }
            
            # ❌ More complex calculation
            if metrics['data_quality_score'] > 0.8:
                metrics['quality_tier'] = 'high'
            elif metrics['data_quality_score'] > 0.6:
                metrics['quality_tier'] = 'medium'
            else:
                metrics['quality_tier'] = 'low'
            
            shared['processing_metrics'] = metrics
        
        # ❌ VIOLATION: External API call in post()
        if config.get('notify_external_system', False):
            try:
                # This API call should be in exec() of a separate node!
                notification_response = requests.post(
                    'https://api.example.com/notifications',
                    json={
                        'event': 'user_processed',
                        'user_id': processed_user['id'],
                        'timestamp': processed_user['processed_at']
                    }
                )
                shared['notification_sent'] = notification_response.status_code == 200
            except Exception as e:
                shared['notification_error'] = str(e)
        
        # ❌ VIOLATION: File operations in post()
        if config.get('save_audit_log', False):
            try:
                # This file operation should be in exec() of a separate node!
                audit_entry = {
                    'user_id': processed_user['id'],
                    'processed_at': processed_user['processed_at'],
                    'node': self.__class__.__name__,
                    'success': True
                }
                
                audit_file = f"/tmp/audit_{datetime.now().strftime('%Y%m%d')}.json"
                try:
                    with open(audit_file, 'r') as f:
                        audit_data = json.load(f)
                except FileNotFoundError:
                    audit_data = []
                
                audit_data.append(audit_entry)
                
                with open(audit_file, 'w') as f:
                    json.dump(audit_data, f, indent=2)
                
                shared['audit_logged'] = True
            except Exception as e:
                shared['audit_error'] = str(e)
        
        # ❌ VIOLATION: LLM call in post()
        if config.get('generate_summary', False):
            try:
                # This LLM call should be in exec()!
                summary_prompt = f"Generate a summary for user processing: {processed_user}"
                processing_summary = self._call_llm(summary_prompt)
                shared['processing_summary'] = processing_summary
            except Exception as e:
                shared['summary_error'] = str(e)
        
        # ❌ Complex routing logic based on computations done in post()
        if shared.get('processing_metrics', {}).get('quality_tier') == 'low':
            return 'quality_review_needed'
        elif shared.get('notification_error'):
            return 'notification_failed'
        elif shared.get('audit_error'):
            return 'audit_failed'
        
        return None
    
    def _call_llm(self, prompt: str) -> str:
        """❌ LLM call in post() method."""
        # LLM calls should be in exec() for proper retry handling
        return f"Summary: {prompt}"


class AsyncLifecycleViolationNode(AsyncNode):
    """
    ❌ ANTIPATTERN: Mixing sync and async operations incorrectly
    
    This node violates async lifecycle patterns by:
    - Using sync operations in async methods
    - Using async operations in sync methods
    - Improper await handling
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Async operations in sync prep() method
        
        prep() is synchronous and should not contain async operations.
        """
        api_config = shared.get('api_config')
        
        # ❌ VIOLATION: Async operation in sync method
        # This will cause runtime errors!
        try:
            # This is wrong - can't await in sync method
            # api_data = await self._fetch_config_data(api_config['url'])  # WRONG!
            
            # Trying to work around with sync call to async function (also wrong)
            import asyncio
            api_data = asyncio.run(self._fetch_config_data(api_config['url']))  # WRONG!
        except Exception:
            api_data = {}
        
        return {
            'api_config': api_config,
            'api_data': api_data
        }
    
    async def exec_async(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Sync operations in async method without proper handling
        
        async exec should use await properly and not block with sync operations.
        """
        api_config = prep_result['api_config']
        
        # ❌ VIOLATION: Blocking sync operation in async method
        # This blocks the event loop!
        time.sleep(5)  # WRONG! Use await asyncio.sleep(5)
        
        # ❌ VIOLATION: Sync requests in async method
        # This blocks the event loop!
        response = requests.get(api_config['url'])  # WRONG! Use async http client
        
        # ❌ VIOLATION: Calling async function without await
        # This doesn't work as expected!
        data_result = self._process_async_data(response.text)  # WRONG! Missing await
        
        # ❌ VIOLATION: File operations without async
        # This blocks the event loop!
        with open('/tmp/data.json', 'w') as f:  # WRONG! Use async file operations
            json.dump(data_result, f)
        
        return {
            'processed_data': data_result,
            'success': True
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """
        ❌ ANTIPATTERN: Async operations in sync post() method
        """
        # ❌ VIOLATION: Async operation in sync post method
        # This will cause runtime errors!
        try:
            # Can't await in sync method
            # await self._send_async_notification(exec_result)  # WRONG!
            
            # Trying to work around (also wrong)
            import asyncio
            asyncio.run(self._send_async_notification(exec_result))  # WRONG!
        except Exception:
            pass
        
        shared['async_result'] = exec_result
        return None
    
    async def _fetch_config_data(self, url: str) -> Dict[str, Any]:
        """Async helper method."""
        # Should use async HTTP client
        return {'config': 'data'}
    
    async def _process_async_data(self, data: str) -> Dict[str, Any]:
        """Async data processing."""
        await asyncio.sleep(1)  # Simulate async work
        return {'processed': data}
    
    async def _send_async_notification(self, result: Dict[str, Any]) -> None:
        """Async notification sending."""
        await asyncio.sleep(0.5)  # Simulate async work


class BatchLifecycleViolationNode(BatchNode):
    """
    ❌ ANTIPATTERN: Batch node with lifecycle violations
    
    This node violates batch processing patterns by:
    - Processing single items instead of batches
    - Complex state management between items
    - Wrong item processing patterns
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Preparing for single-item processing in BatchNode
        
        BatchNode should process collections, not single items.
        """
        # ❌ VIOLATION: Getting single item instead of collection
        single_item = shared.get('single_item')  # Should be 'items' collection
        
        if single_item:
            # ❌ VIOLATION: Artificially creating batch from single item
            items = [single_item]  # This defeats the purpose of BatchNode
        else:
            items = []
        
        return {
            'items': items,
            'batch_size': 1  # ❌ Batch size of 1 indicates wrong node type
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Incorrect batch processing with state sharing
        
        Batch processing should be stateless between items.
        """
        items = prep_result['items']
        
        # ❌ VIOLATION: Complex state shared between items
        shared_state = {
            'running_total': 0,
            'previous_results': [],
            'error_count': 0,
            'cache': {}
        }
        
        results = []
        
        for i, item in enumerate(items):
            # ❌ VIOLATION: Each item processing depends on previous items
            if i > 0:
                # Using results from previous items
                item['prev_result'] = shared_state['previous_results'][-1]
                item['running_total'] = shared_state['running_total']
            
            # ❌ VIOLATION: Complex per-item processing that should be in separate node
            try:
                processed_item = self._complex_item_processing(item, shared_state)
                
                # ❌ VIOLATION: Updating shared state between items
                shared_state['running_total'] += processed_item.get('value', 0)
                shared_state['previous_results'].append(processed_item)
                shared_state['cache'][item.get('id')] = processed_item
                
                results.append(processed_item)
                
            except Exception as e:
                shared_state['error_count'] += 1
                results.append({'error': str(e), 'item_id': item.get('id')})
        
        return {
            'processed_items': results,
            'shared_state': shared_state,  # ❌ Returning stateful data
            'total_errors': shared_state['error_count']
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Post method handling stateful batch results."""
        shared['batch_results'] = exec_result['processed_items']
        shared['batch_state'] = exec_result['shared_state']
        
        # ❌ Routing based on complex state
        if exec_result['total_errors'] > 0:
            return 'batch_errors'
        
        return None
    
    def _complex_item_processing(self, item: Dict[str, Any], shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """❌ Complex processing that depends on shared state."""
        # This violates stateless batch processing principles
        processed = item.copy()
        processed['processed_with_state'] = True
        processed['state_dependency'] = len(shared_state['previous_results'])
        return processed


# ============================================================================
# How to Fix These Antipatterns
# ============================================================================

"""
✅ CORRECT APPROACH: Follow the lifecycle pattern properly

1. prep() method responsibilities:
   - Read from SharedStore only
   - Validate input data
   - Prepare parameters for exec()
   - NO computation, NO external calls, NO LLM calls

2. exec() method responsibilities:
   - Use ONLY prep_result parameter (never self.shared)
   - Perform ALL computations and processing
   - Make ALL external calls (API, LLM, file operations)
   - Return processed results
   - Let exceptions propagate naturally

3. post() method responsibilities:
   - Update SharedStore with exec() results
   - Determine next action/routing
   - NO computation, NO external calls, NO LLM calls

4. Async handling:
   - Use AsyncNode for I/O operations
   - Use proper async/await patterns
   - Don't mix sync/async incorrectly
   - Don't block the event loop

5. Batch processing:
   - Use BatchNode for homogeneous collections
   - Keep item processing stateless
   - Don't use BatchNode for single items
   - Process items independently

Example corrected structure:

class CorrectLifecycleNode(Node):
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        # Only data access and validation
        user_data = shared.get('user_data')
        if not user_data:
            raise ValueError("User data required")
        return {'user_data': user_data, 'config': shared.get('config', {})}
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        # All computation and external calls here
        user_data = prep_result['user_data']
        processed = self._process_user(user_data)  # Pure computation
        external_data = self._call_external_api(processed)  # External call
        return {'processed_user': processed, 'external_data': external_data}
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        # Only SharedStore updates and routing
        shared['processed_user'] = exec_result['processed_user']
        if exec_result['external_data'].get('error'):
            return 'external_api_failed'
        return None
"""

if __name__ == "__main__":
    print("⚠️  ANTIPATTERN EXAMPLES - DO NOT USE THESE PATTERNS")
    print("These examples show lifecycle violations in PocketFlow nodes.")
    print("See templates/examples/good/ for correct lifecycle patterns.")
    
    # These examples are intentionally broken and serve as educational material
    # about what NOT to do in PocketFlow applications.