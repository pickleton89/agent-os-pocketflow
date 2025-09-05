"""
Bad Example: Hidden Logic and Business Logic in Utilities

⚠️ ANTIPATTERN WARNING: This file demonstrates what NOT to do in PocketFlow.
These examples show hidden business logic, complex utilities, and
violations of the separation between utilities and business logic.

DO NOT COPY THESE PATTERNS - Use templates/examples/good/ instead.
"""

from typing import Dict, Any, Optional, List, Union
from pocketflow import SharedStore, Node, AsyncNode
import requests
import json
import re
import logging
from datetime import datetime
from dataclasses import dataclass
import openai


# ============================================================================
# ANTIPATTERN: Complex Business Logic Hidden in Utilities  
# ============================================================================

def process_customer_data_completely(customer_data: Dict[str, Any], business_rules: Dict[str, Any]) -> Dict[str, Any]:
    """
    ❌ ANTIPATTERN: Hidden business logic in utility function
    
    This function violates utility function principles by:
    - Containing complex business logic that should be in nodes
    - Making LLM calls (should be in exec methods)
    - Having multiple responsibilities
    - Making decisions that affect flow control
    - Being untestable without external dependencies
    """
    
    # ❌ Complex business validation logic hidden in utility
    if customer_data.get('tier') == 'premium':
        # Business rule: Premium customers get different processing
        if customer_data.get('account_balance', 0) < business_rules.get('premium_min_balance', 1000):
            # ❌ Business decision making in utility
            customer_data['tier_downgrade_required'] = True
            customer_data['tier'] = 'standard'
            
            # ❌ LLM call in utility function - should be in node exec()
            downgrade_message = call_llm_for_downgrade_message(
                customer_data['name'], 
                business_rules['premium_min_balance']
            )
            customer_data['downgrade_notification'] = downgrade_message
    
    # ❌ Complex scoring algorithm hidden in utility
    risk_score = calculate_customer_risk_with_llm(customer_data, business_rules)
    if risk_score > business_rules.get('risk_threshold', 0.7):
        # ❌ Business decision: flag for review
        customer_data['requires_manual_review'] = True
        
        # ❌ Another LLM call for risk assessment
        risk_explanation = call_llm_for_risk_explanation(customer_data, risk_score)
        customer_data['risk_explanation'] = risk_explanation
    
    # ❌ Complex workflow decisions hidden in utility
    if customer_data.get('country') in business_rules.get('restricted_countries', []):
        # ❌ Business logic: compliance checking
        compliance_status = check_compliance_with_llm(customer_data)
        customer_data['compliance_status'] = compliance_status
        
        if compliance_status == 'non_compliant':
            # ❌ Workflow control decision in utility
            customer_data['processing_blocked'] = True
            customer_data['block_reason'] = 'compliance_violation'
    
    # ❌ External API calls in utility (should be in AsyncNode)
    try:
        credit_report = fetch_credit_report(customer_data['ssn'])
        customer_data['credit_score'] = credit_report['score']
        
        # ❌ More business logic based on external data
        if credit_report['score'] < business_rules.get('min_credit_score', 600):
            customer_data['credit_approved'] = False
            
            # ❌ Yet another LLM call for rejection message
            rejection_message = call_llm_for_credit_rejection(
                customer_data['name'], 
                credit_report['score']
            )
            customer_data['rejection_message'] = rejection_message
    except Exception as e:
        # ❌ Business decision on how to handle failures
        customer_data['credit_check_failed'] = True
        customer_data['requires_manual_review'] = True
    
    return customer_data


def call_llm_for_downgrade_message(customer_name: str, min_balance: float) -> str:
    """
    ❌ ANTIPATTERN: LLM calls hidden in utility functions
    
    LLM calls should always be in node exec() methods for proper:
    - Retry handling by the framework
    - Error classification and routing
    - Testability and mocking
    - Flow control and branching
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Write a polite message to {customer_name} explaining their account will be downgraded because they don't meet the minimum balance of ${min_balance}"}
            ]
        )
        return response.choices[0].message.content
    except Exception:
        return f"Dear {customer_name}, your account will be downgraded due to insufficient balance."


def calculate_customer_risk_with_llm(customer_data: Dict[str, Any], business_rules: Dict[str, Any]) -> float:
    """
    ❌ ANTIPATTERN: Complex risk calculation with LLM in utility
    
    This combines business logic with LLM calls in a utility function.
    Should be split into separate nodes for risk calculation and LLM analysis.
    """
    # ❌ Complex business logic for risk factors
    risk_factors = []
    
    if customer_data.get('age', 0) < 25:
        risk_factors.append("young_age")
    if customer_data.get('income', 0) < business_rules.get('min_income', 30000):
        risk_factors.append("low_income")
    if len(customer_data.get('address_history', [])) > 5:
        risk_factors.append("frequent_moves")
    if customer_data.get('previous_defaults', 0) > 0:
        risk_factors.append("previous_defaults")
    
    # ❌ LLM call to assess risk (should be in exec method)
    try:
        prompt = f"""
        Assess the risk level for this customer profile:
        Age: {customer_data.get('age')}
        Income: {customer_data.get('income')}
        Risk factors: {', '.join(risk_factors)}
        Credit history length: {customer_data.get('credit_history_months', 0)} months
        
        Return a risk score between 0.0 and 1.0.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # ❌ Complex parsing logic in utility
        risk_text = response.choices[0].message.content
        risk_score = extract_risk_score_from_text(risk_text)
        return risk_score
    except Exception:
        # ❌ Business decision on fallback risk calculation
        return len(risk_factors) * 0.2  # Fallback calculation


def intelligent_data_processor(data: Dict[str, Any], processing_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    ❌ ANTIPATTERN: "Intelligent" utility function with hidden LLM logic
    
    This function appears to be a simple data processor but actually
    contains hidden AI logic that makes business decisions.
    """
    processed_data = data.copy()
    
    # ❌ Hidden data enhancement with LLM
    if processing_config.get('enhance_descriptions', False):
        for field in ['description', 'summary', 'notes']:
            if field in processed_data and processed_data[field]:
                # ❌ LLM call hidden in what appears to be simple processing
                enhanced = enhance_text_with_llm(processed_data[field])
                processed_data[f'{field}_enhanced'] = enhanced
    
    # ❌ Hidden sentiment analysis
    if 'feedback' in processed_data:
        # ❌ LLM call for sentiment without being obvious
        sentiment = analyze_sentiment_with_llm(processed_data['feedback'])
        processed_data['sentiment_score'] = sentiment
        
        # ❌ Business logic based on sentiment
        if sentiment < -0.5:
            processed_data['priority'] = 'high'
            processed_data['escalate_to_manager'] = True
    
    # ❌ Hidden categorization logic
    if processing_config.get('auto_categorize', False):
        # ❌ LLM call for categorization
        category = categorize_data_with_llm(processed_data)
        processed_data['auto_category'] = category
        
        # ❌ Business routing decision based on category
        if category in ['urgent', 'complaint', 'legal']:
            processed_data['requires_immediate_attention'] = True
    
    return processed_data


# ============================================================================
# ANTIPATTERN: Utilities Making External Calls with Business Logic
# ============================================================================

def smart_api_caller(endpoint: str, data: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    ❌ ANTIPATTERN: Utility function with complex retry logic and business decisions
    
    This function violates utility principles by:
    - Making business decisions about retry strategies  
    - Containing complex fallback logic
    - Making multiple different API calls based on business rules
    - Handling business-specific error conditions
    """
    
    # ❌ Business logic: choose API endpoint based on data
    if data.get('customer_tier') == 'premium':
        endpoint = config.get('premium_api_endpoint', endpoint)
        timeout = config.get('premium_timeout', 60)
    else:
        timeout = config.get('standard_timeout', 30)
    
    # ❌ Business-specific retry logic
    max_retries = 3
    if data.get('priority') == 'urgent':
        max_retries = 5  # Business decision: urgent requests get more retries
    
    for attempt in range(max_retries):
        try:
            response = requests.post(endpoint, json=data, timeout=timeout)
            
            if response.status_code == 200:
                result = response.json()
                
                # ❌ Business logic: enhance response based on customer tier
                if data.get('customer_tier') == 'premium':
                    # ❌ Additional API call for premium customers
                    enhanced_data = call_premium_enhancement_api(result)
                    if enhanced_data:
                        result.update(enhanced_data)
                
                return result
            
            elif response.status_code == 429:  # Rate limited
                # ❌ Business decision: how to handle rate limits
                if data.get('customer_tier') == 'premium':
                    # Premium customers: wait longer and retry
                    time.sleep(2 ** attempt * 2)  # Exponential backoff
                else:
                    # Standard customers: fail faster
                    time.sleep(2 ** attempt)
            
            elif response.status_code == 402:  # Payment required
                # ❌ Business logic: payment handling
                if data.get('auto_pay_enabled', False):
                    payment_result = process_automatic_payment(data['customer_id'])
                    if payment_result['success']:
                        continue  # Retry after payment
                
                # ❌ Business decision: how to handle payment failures
                return {
                    'error': 'payment_required',
                    'payment_url': generate_payment_url(data['customer_id']),
                    'amount_due': get_customer_balance(data['customer_id'])
                }
        
        except requests.exceptions.Timeout:
            # ❌ Business logic: timeout handling strategy
            if data.get('allow_fallback', True):
                # ❌ Business decision: use fallback service
                fallback_result = call_fallback_api(data)
                if fallback_result:
                    fallback_result['_used_fallback'] = True
                    return fallback_result
        
        except requests.exceptions.ConnectionError:
            # ❌ Business logic: connection error handling
            if attempt == max_retries - 1:
                # ❌ Business decision: use cached data on final failure
                cached_result = get_cached_api_result(data)
                if cached_result:
                    cached_result['_used_cache'] = True
                    return cached_result
    
    # ❌ Business decision: how to handle total failure
    if data.get('customer_tier') == 'premium':
        # Premium customers get manual processing
        create_manual_processing_ticket(data)
        return {'status': 'manual_processing_scheduled'}
    
    return None


def dynamic_validator(data: Dict[str, Any], validation_rules: Dict[str, Any]) -> Dict[str, Any]:
    """
    ❌ ANTIPATTERN: Validation utility with hidden business logic and LLM calls
    
    This appears to be a simple validator but contains complex business
    logic and LLM calls that should be in nodes.
    """
    validation_results = {'is_valid': True, 'errors': [], 'warnings': []}
    
    # ❌ Basic validation (this part is OK for utilities)
    for field, rules in validation_rules.get('basic_rules', {}).items():
        if field in data:
            value = data[field]
            if 'required' in rules and not value:
                validation_results['errors'].append(f'{field} is required')
                validation_results['is_valid'] = False
    
    # ❌ PROBLEM: Complex business validation with LLM
    if validation_rules.get('use_ai_validation', False):
        # ❌ LLM call for content validation
        content_fields = ['description', 'comments', 'feedback']
        for field in content_fields:
            if field in data and data[field]:
                # ❌ Hidden LLM call in validator
                ai_validation = validate_content_with_llm(data[field])
                
                if ai_validation.get('inappropriate', False):
                    validation_results['errors'].append(f'{field} contains inappropriate content')
                    validation_results['is_valid'] = False
                
                if ai_validation.get('spam_likelihood', 0) > 0.8:
                    validation_results['errors'].append(f'{field} appears to be spam')
                    validation_results['is_valid'] = False
                
                # ❌ Business logic: auto-correct based on LLM suggestions
                if ai_validation.get('suggested_correction'):
                    data[f'{field}_corrected'] = ai_validation['suggested_correction']
    
    # ❌ Business rule validation with external calls
    if validation_rules.get('check_external_blacklist', False):
        if 'email' in data:
            # ❌ External API call in validator
            blacklist_result = check_email_blacklist(data['email'])
            if blacklist_result.get('is_blacklisted', False):
                validation_results['errors'].append('Email is on blacklist')
                validation_results['is_valid'] = False
                
                # ❌ Business logic: auto-suggest alternative
                if blacklist_result.get('suggested_domains'):
                    validation_results['suggestions'] = {
                        'alternative_emails': [
                            data['email'].replace(data['email'].split('@')[1], domain)
                            for domain in blacklist_result['suggested_domains']
                        ]
                    }
    
    return validation_results


# ============================================================================
# ANTIPATTERN: Nodes That Rely on Hidden Logic Utilities
# ============================================================================

class CustomerProcessingNodeWithHiddenLogic(Node):
    """
    ❌ ANTIPATTERN: Node that delegates business logic to utilities
    
    This node appears simple but actually delegates complex business
    logic to utilities, making the true complexity invisible.
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare customer processing."""
        return {
            'customer_data': shared.get('customer_data'),
            'business_rules': shared.get('business_rules'),
            'processing_config': shared.get('processing_config')
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Exec method that hides complexity in utilities
        
        This method looks simple but actually performs complex operations
        including LLM calls, external API calls, and business decisions
        through utility functions.
        """
        customer_data = prep_result['customer_data']
        business_rules = prep_result['business_rules']
        processing_config = prep_result['processing_config']
        
        # ❌ This innocent-looking call actually contains multiple LLM calls
        # and complex business logic
        processed_customer = process_customer_data_completely(customer_data, business_rules)
        
        # ❌ This "validation" actually makes LLM calls and external API calls
        validation_result = dynamic_validator(processed_customer, processing_config.get('validation'))
        
        # ❌ This "API call" actually makes business decisions and multiple API calls
        external_data = smart_api_caller(
            processing_config['api_endpoint'],
            processed_customer,
            processing_config
        )
        
        # ❌ This "data processing" actually contains hidden LLM logic
        enhanced_data = intelligent_data_processor(
            processed_customer,
            processing_config.get('enhancement')
        )
        
        return {
            'processed_customer': enhanced_data,
            'validation_result': validation_result,
            'external_data': external_data,
            'processing_successful': validation_result.get('is_valid', False)
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Post method that doesn't reveal the complexity of what happened."""
        shared['customer_result'] = exec_result['processed_customer']
        shared['validation_result'] = exec_result['validation_result']
        
        # ❌ Routing decisions based on hidden business logic results
        if not exec_result['processing_successful']:
            return 'validation_failed'
        
        # ❌ These conditions are set by hidden business logic in utilities
        if exec_result['processed_customer'].get('requires_manual_review'):
            return 'manual_review_required'
        
        if exec_result['processed_customer'].get('processing_blocked'):
            return 'processing_blocked'
        
        return None


class DataEnhancementNodeWithHiddenAI(Node):
    """
    ❌ ANTIPATTERN: Node that uses utilities with hidden AI/LLM logic
    
    This node appears to be doing simple data enhancement but actually
    contains multiple AI/LLM calls hidden in utility functions.
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare for data enhancement."""
        return {
            'raw_data': shared.get('raw_data'),
            'enhancement_config': shared.get('enhancement_config')
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        ❌ ANTIPATTERN: Hidden AI/LLM calls through utilities
        
        This method appears to be doing simple data processing but
        actually makes multiple LLM calls through utility functions.
        """
        raw_data = prep_result['raw_data']
        config = prep_result['enhancement_config']
        
        enhanced_items = []
        
        for item in raw_data:
            # ❌ This innocent call actually makes LLM calls for:
            # - text enhancement
            # - sentiment analysis  
            # - categorization
            enhanced_item = intelligent_data_processor(item, config)
            enhanced_items.append(enhanced_item)
        
        return {
            'enhanced_data': enhanced_items,
            'total_processed': len(enhanced_items)
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Post method that doesn't reveal AI operations occurred."""
        shared['enhanced_data'] = exec_result['enhanced_data']
        
        # ❌ Routing based on AI decisions made in utilities
        urgent_items = [
            item for item in exec_result['enhanced_data']
            if item.get('requires_immediate_attention')
        ]
        
        if urgent_items:
            shared['urgent_items'] = urgent_items
            return 'urgent_items_found'
        
        return None


# ============================================================================
# How to Fix These Antipatterns
# ============================================================================

"""
✅ CORRECT APPROACH: Keep business logic in nodes, utilities simple

Instead of complex utilities with hidden business logic:

1. Make LLM calls explicit in node exec() methods:
   - LLMContentEnhancementNode
   - LLMSentimentAnalysisNode  
   - LLMCategorizationNode
   - LLMRiskAssessmentNode

2. Move business logic to dedicated nodes:
   - CustomerTierEvaluationNode
   - RiskCalculationNode
   - ComplianceCheckNode
   - PaymentProcessingNode

3. Keep utilities simple and pure:
   - read_file(path) -> str | None
   - validate_email(email) -> bool
   - normalize_text(text) -> str
   - make_http_request(url, data) -> dict | None

4. Make external dependencies explicit:
   - ExternalAPINode for each external service
   - DatabaseNode for database operations
   - EmailServiceNode for email operations

Benefits:
- Business logic is visible in the flow diagram
- LLM calls are explicit and properly handled
- Utilities can be tested in isolation
- Business decisions are trackable
- Error handling is clear and focused
- Flow control is transparent
"""

if __name__ == "__main__":
    print("⚠️  ANTIPATTERN EXAMPLES - DO NOT USE THESE PATTERNS")
    print("These examples show hidden business logic and LLM calls in utilities.")
    print("See templates/examples/good/ for correct utility patterns.")
    
    # These examples are intentionally problematic and serve as educational
    # material about what NOT to do in PocketFlow applications.