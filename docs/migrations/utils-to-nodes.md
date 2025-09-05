# Migration Guide: Move Logic from Utils to Nodes

**Antipattern**: Business Logic in Utilities  
**Severity**: 🟡 High  
**Time Estimate**: 2-3 hours  
**Risk Level**: Medium (architectural changes affecting multiple files)

## Problem Description

Utility functions should be simple, pure helpers. When they contain business logic (LLM calls, complex branching, decision making), they become invisible complexity that's hard to test and maintain.

## Detecting the Problem

### Automated Detection
```bash
# Run antipattern detector
python pocketflow-tools/antipattern_detector.py your_code/

# Look for violations like:
# "Utility function contains LLM calls"
# "Utility function has complex branching logic (X branches)"
```

### Manual Inspection
Look for these patterns in utility functions:

```python
# 🚨 ANTIPATTERN EXAMPLES - Business logic in utils

# utils/data_processor.py
def smart_data_processor(data, user_context, processing_options):
    """❌ BAD: Complex business logic in utility"""
    
    # ❌ Business decision logic
    if user_context.subscription_tier == 'premium':
        # ❌ LLM call in utility
        enhanced_data = call_llm_enhance(data, 'premium_model')
    else:
        enhanced_data = call_llm_enhance(data, 'basic_model')
    
    # ❌ Complex branching based on business rules
    if processing_options.quality_level == 'high':
        # ❌ Another LLM call
        quality_check = call_llm_quality_validator(enhanced_data)
        if quality_check.score < 0.8:
            # ❌ Fallback business logic
            enhanced_data = call_llm_enhance(data, 'premium_model', retries=3)
    
    # ❌ More business decisions
    if processing_options.include_metadata:
        metadata = extract_business_metadata(enhanced_data, user_context)
        enhanced_data.metadata = metadata
    
    return enhanced_data


def intelligent_content_analyzer(content, analysis_type, context):
    """❌ BAD: Decision-making logic in utility"""
    
    # ❌ Business logic for analysis type selection
    if analysis_type == 'auto':
        # ❌ LLM call to determine analysis type
        detected_type = call_llm_classify_content(content)
        analysis_type = detected_type.category
    
    # ❌ Complex business rules
    if context.user_preferences.detailed_analysis:
        # ❌ Multiple LLM calls
        sentiment = call_llm_sentiment_analysis(content)
        entities = call_llm_entity_extraction(content)
        topics = call_llm_topic_modeling(content)
        
        return {
            'analysis_type': analysis_type,
            'sentiment': sentiment,
            'entities': entities,
            'topics': topics
        }
    else:
        # ❌ Different business path
        summary = call_llm_summarize(content)
        return {
            'analysis_type': analysis_type,
            'summary': summary
        }


# ❌ BAD: Exception handling with business decisions
def robust_api_call(endpoint, data, user_context):
    """❌ BAD: Business retry logic in utility"""
    
    try:
        response = make_api_call(endpoint, data)
        return response
    except APIRateLimitError:
        # ❌ Business decision in utility
        if user_context.subscription_tier == 'premium':
            # ❌ Business logic for premium users
            time.sleep(1)
            return make_api_call(endpoint, data)
        else:
            # ❌ Business logic for regular users  
            return call_llm_generate_fallback_response(data)
    except APIError as e:
        # ❌ Complex error handling business logic
        if user_context.fallback_enabled:
            return call_llm_generate_fallback_response(data)
        else:
            raise BusinessLogicError("API failed and fallback disabled")
```

## Migration Steps

### Step 1: Identify Business Logic in Utils (20 minutes)

Audit your utility functions for business logic indicators:

```python
# Utility audit checklist
BUSINESS_LOGIC_INDICATORS = [
    "LLM calls (call_llm*, openai.*, anthropic.*)",
    "Complex conditional logic (>2 if/else branches)",
    "User context/subscription tier decisions", 
    "Error handling with business rules",
    "Configuration-based behavior changes",
    "State modifications",
    "External API calls with business retry logic"
]

# Example audit result:
utils_audit = {
    "smart_data_processor": {
        "llm_calls": 3,  # ❌ Move to nodes
        "branches": 4,   # ❌ Move to nodes
        "business_decisions": ["subscription_tier", "quality_level"]  # ❌ Move to nodes
    },
    "intelligent_content_analyzer": {
        "llm_calls": 5,  # ❌ Move to nodes  
        "branches": 3,   # ❌ Move to nodes
        "business_decisions": ["auto_detection", "user_preferences"]  # ❌ Move to nodes
    },
    "safe_file_reader": {  # ✅ Good utility
        "llm_calls": 0,
        "branches": 1,   # Simple error handling
        "business_decisions": []  # Pure utility
    }
}
```

### Step 2: Design Node Architecture (30 minutes)

Plan how to convert utilities into focused nodes:

```yaml
# Migration plan for smart_data_processor
original_utility: smart_data_processor(data, user_context, processing_options)

new_node_architecture:
  - name: UserTierClassificationNode
    responsibility: Determine processing tier based on subscription
    input: user_context
    output: processing_tier
    
  - name: DataEnhancementNode  
    responsibility: Enhance data using appropriate LLM model
    input: data, processing_tier
    output: enhanced_data
    
  - name: QualityValidationNode
    responsibility: Validate data quality with LLM
    input: enhanced_data, quality_requirements
    output: validation_result
    
  - name: MetadataExtractionNode
    responsibility: Extract business metadata if requested
    input: enhanced_data, user_context, include_metadata_flag
    output: final_data_with_metadata

flow_design:
  edges:
    - UserTierClassificationNode -> DataEnhancementNode
    - DataEnhancementNode -> QualityValidationNode  
    - [DataEnhancementNode, QualityValidationNode] -> MetadataExtractionNode
```

### Step 3: Create Focused Nodes (90 minutes)

Convert each business responsibility into a dedicated node:

```python
# ✅ CONVERTED TO FOCUSED NODES

class UserTierClassificationNode(Node):
    """Determine processing tier based on user subscription"""
    
    def prep(self):
        return {
            'user_context': self.shared['user_context']
        }
    
    def exec(self, prep_result):
        user_context = prep_result['user_context']
        
        # Business logic is now visible and testable in a node
        if user_context.subscription_tier == 'premium':
            return {
                'processing_tier': 'premium',
                'model_type': 'premium_model'
            }
        else:
            return {
                'processing_tier': 'basic',
                'model_type': 'basic_model'
            }


class DataEnhancementNode(Node):
    """Enhance data using appropriate LLM model"""
    
    def prep(self):
        return {
            'data': self.shared['input_data'],
            'model_type': self.shared['model_type']
        }
    
    def exec(self, prep_result):
        # LLM calls are now properly placed in node exec()
        enhanced_data = call_llm_enhance(
            prep_result['data'],
            prep_result['model_type']
        )
        return {'enhanced_data': enhanced_data}


class QualityValidationNode(Node):
    """Validate data quality and apply business rules"""
    
    def prep(self):
        return {
            'enhanced_data': self.shared['enhanced_data'],
            'processing_options': self.shared['processing_options'],
            'processing_tier': self.shared['processing_tier']
        }
    
    def exec(self, prep_result):
        data = prep_result['enhanced_data']
        options = prep_result['processing_options']
        tier = prep_result['processing_tier']
        
        # Business logic is explicit and testable
        if options.quality_level == 'high':
            quality_check = call_llm_quality_validator(data)
            
            if quality_check.score < 0.8:
                # Business retry logic is now visible
                if tier == 'premium':
                    # Premium users get retry with better model
                    data = call_llm_enhance(data, 'premium_model', retries=3)
                else:
                    # Basic users get standard retry
                    data = call_llm_enhance(data, 'basic_model', retries=1)
        
        return {
            'validated_data': data,
            'quality_score': quality_check.score if 'quality_check' in locals() else None
        }


class MetadataExtractionNode(Node):
    """Extract business metadata based on user preferences"""
    
    def prep(self):
        return {
            'validated_data': self.shared['validated_data'],
            'processing_options': self.shared['processing_options'],
            'user_context': self.shared['user_context']
        }
    
    def exec(self, prep_result):
        data = prep_result['validated_data']
        options = prep_result['processing_options']
        context = prep_result['user_context']
        
        # Business decision is explicit
        if options.include_metadata:
            # Business logic for metadata extraction
            metadata = extract_business_metadata(data, context)
            data.metadata = metadata
        
        return {'final_data': data}


# ✅ Convert complex utility to flow  
class SmartDataProcessingFlow(Flow):
    """Replaces the smart_data_processor utility function"""
    
    def __init__(self):
        super().__init__()
        
        self.add_node("classify_tier", UserTierClassificationNode())
        self.add_node("enhance", DataEnhancementNode())
        self.add_node("validate", QualityValidationNode())
        self.add_node("metadata", MetadataExtractionNode())
        
        # Define business process flow
        self.add_edge("classify_tier", "enhance")
        self.add_edge("enhance", "validate")
        self.add_edge("validate", "metadata")
```

### Step 4: Create Simple, Pure Utilities (30 minutes)

Keep utilities for simple, reusable operations:

```python
# ✅ GOOD UTILITIES - Simple and pure

def safe_file_reader(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """Pure utility: safely read file contents"""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except (IOError, UnicodeDecodeError) as e:
        logger.warning(f"Could not read {file_path}: {e}")
        return None


def normalize_text(text: str) -> str:
    """Pure utility: normalize text formatting"""
    if not text:
        return ""
    
    # Simple, deterministic transformations
    normalized = text.strip()
    normalized = re.sub(r'\s+', ' ', normalized)  # Collapse whitespace
    return normalized


def calculate_text_metrics(text: str) -> Dict[str, int]:
    """Pure utility: calculate basic text statistics"""
    if not text:
        return {'char_count': 0, 'word_count': 0, 'line_count': 0}
    
    return {
        'char_count': len(text),
        'word_count': len(text.split()),
        'line_count': text.count('\n') + 1
    }


def format_currency(amount: float, currency: str = 'USD') -> str:
    """Pure utility: format currency display"""
    if currency == 'USD':
        return f"${amount:.2f}"
    elif currency == 'EUR':
        return f"€{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"


# ✅ Configuration utilities - simple parsing only
def parse_processing_config(config_dict: Dict[str, Any]) -> ProcessingConfig:
    """Pure utility: parse configuration without business decisions"""
    return ProcessingConfig(
        quality_level=config_dict.get('quality_level', 'medium'),
        include_metadata=config_dict.get('include_metadata', False),
        timeout_seconds=config_dict.get('timeout', 30)
    )


def validate_email_format(email: str) -> bool:
    """Pure utility: basic email format validation"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))
```

### Step 5: Update Flow Integration (45 minutes)

Replace utility calls with node flows:

```python
# ❌ Before: Using utility function
class BadProcessingNode(Node):
    def exec(self, prep_result):
        # ❌ Business logic hidden in utility
        result = smart_data_processor(
            prep_result['data'],
            prep_result['user_context'], 
            prep_result['options']
        )
        return result

# ✅ After: Using focused node flow
class GoodProcessingNode(Node):
    """Node that delegates to the smart processing flow"""
    
    def prep(self):
        return {
            'input_data': self.shared['raw_data'],
            'user_context': self.shared['user_context'],
            'processing_options': self.shared['options']
        }
    
    def exec(self, prep_result):
        # Business logic is now explicit in the flow
        flow = SmartDataProcessingFlow()
        result = flow.run(prep_result)
        return result['final_data']


# ✅ Alternative: Incorporate nodes into parent flow
class DocumentAnalysisFlow(Flow):
    """Main flow that includes the converted logic"""
    
    def __init__(self):
        super().__init__()
        
        # Include the nodes that replace the utility
        self.add_node("classify_tier", UserTierClassificationNode())
        self.add_node("enhance", DataEnhancementNode())
        self.add_node("validate", QualityValidationNode())
        self.add_node("metadata", MetadataExtractionNode())
        
        # Other business nodes
        self.add_node("analyze_sentiment", SentimentAnalysisNode())
        self.add_node("extract_entities", EntityExtractionNode())
        
        # Connect replaced utility logic into main flow
        self.add_edge("classify_tier", "enhance")
        self.add_edge("enhance", "validate") 
        self.add_edge("validate", "metadata")
        
        # Continue with other analysis
        self.add_edge("metadata", "analyze_sentiment")
        self.add_edge("analyze_sentiment", "extract_entities")
```

### Step 6: Handle Complex Cases (60 minutes)

#### Case A: Utilities with Multiple Responsibilities

```python
# ❌ Before: Multi-responsibility utility
def content_processor_utility(content, processing_type, user_prefs, context):
    """❌ BAD: Multiple responsibilities in one utility"""
    
    # Responsibility 1: Content classification
    if processing_type == 'auto':
        content_type = call_llm_classify_content(content)
    else:
        content_type = processing_type
    
    # Responsibility 2: Content processing based on type
    if content_type == 'news':
        processed = call_llm_news_processor(content, user_prefs.news_style)
    elif content_type == 'academic':
        processed = call_llm_academic_processor(content, user_prefs.academic_level)
    else:
        processed = call_llm_general_processor(content)
    
    # Responsibility 3: Quality assurance
    if user_prefs.quality_check_enabled:
        quality_score = call_llm_quality_checker(processed)
        if quality_score < 0.7:
            processed = call_llm_improve_content(processed)
    
    # Responsibility 4: Formatting based on context
    if context.output_format == 'markdown':
        processed = format_as_markdown(processed)
    elif context.output_format == 'html':
        processed = format_as_html(processed)
    
    return processed

# ✅ After: Separate nodes for each responsibility
class ContentClassificationNode(Node):
    def exec(self, prep_result):
        if prep_result['processing_type'] == 'auto':
            return {'content_type': call_llm_classify_content(prep_result['content'])}
        else:
            return {'content_type': prep_result['processing_type']}


class ContentProcessingNode(Node):
    def exec(self, prep_result):
        content = prep_result['content']
        content_type = prep_result['content_type']
        user_prefs = prep_result['user_prefs']
        
        if content_type == 'news':
            return {'processed': call_llm_news_processor(content, user_prefs.news_style)}
        elif content_type == 'academic':
            return {'processed': call_llm_academic_processor(content, user_prefs.academic_level)}
        else:
            return {'processed': call_llm_general_processor(content)}


class QualityAssuranceNode(Node):
    def exec(self, prep_result):
        processed = prep_result['processed']
        user_prefs = prep_result['user_prefs']
        
        if user_prefs.quality_check_enabled:
            quality_score = call_llm_quality_checker(processed)
            if quality_score < 0.7:
                processed = call_llm_improve_content(processed)
        
        return {'processed': processed}


class ContentFormattingNode(Node):
    def exec(self, prep_result):
        processed = prep_result['processed']
        output_format = prep_result['output_format']
        
        if output_format == 'markdown':
            return {'formatted': format_as_markdown(processed)}  # ✅ Pure utility OK
        elif output_format == 'html':
            return {'formatted': format_as_html(processed)}      # ✅ Pure utility OK
        else:
            return {'formatted': processed}
```

#### Case B: Error Handling Utilities

```python
# ❌ Before: Business error handling in utility
def robust_llm_caller(prompt, model_config, user_context):
    """❌ BAD: Business error handling logic in utility"""
    
    try:
        return call_llm(prompt, model_config.primary_model)
    except RateLimitError:
        # ❌ Business decision in utility
        if user_context.subscription == 'premium':
            time.sleep(2)  # Premium users wait less
            return call_llm(prompt, model_config.primary_model)
        else:
            # ❌ Business fallback logic
            return call_llm(prompt, model_config.fallback_model)
    except ModelUnavailableError:
        # ❌ Complex business fallback
        if model_config.allow_fallback:
            return call_llm(prompt, model_config.fallback_model)
        else:
            return generate_error_response("Model unavailable")

# ✅ After: Business error handling in dedicated node
class RobustLLMProcessingNode(Node):
    """Handle LLM calls with business-aware error handling"""
    
    def exec(self, prep_result):
        prompt = prep_result['prompt']
        config = prep_result['model_config']
        user_context = prep_result['user_context']
        
        try:
            # Primary attempt
            return {
                'success': True,
                'result': call_llm(prompt, config.primary_model),
                'model_used': config.primary_model
            }
            
        except RateLimitError:
            # Business logic is now explicit and testable
            if user_context.subscription == 'premium':
                time.sleep(2)  # Premium users get retry
                try:
                    return {
                        'success': True,
                        'result': call_llm(prompt, config.primary_model),
                        'model_used': config.primary_model,
                        'retry_used': True
                    }
                except RateLimitError:
                    pass  # Fall through to fallback
            
            # Fallback for rate limits
            return {
                'success': True,
                'result': call_llm(prompt, config.fallback_model),
                'model_used': config.fallback_model,
                'reason': 'rate_limit_fallback'
            }
            
        except ModelUnavailableError:
            if config.allow_fallback:
                return {
                    'success': True,
                    'result': call_llm(prompt, config.fallback_model),
                    'model_used': config.fallback_model,
                    'reason': 'primary_unavailable'
                }
            else:
                return {
                    'success': False,
                    'error': 'Model unavailable and fallback disabled',
                    'model_used': None
                }


# ✅ Keep simple error handling utilities
def safe_api_call(url: str, data: Dict, timeout: int = 30) -> Optional[Dict]:
    """Simple utility: safe API call with basic error handling"""
    try:
        response = requests.post(url, json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        logger.warning(f"API call failed: {e}")
        return None  # Simple failure, no business logic
```

### Step 7: Update Tests (30 minutes)

Create comprehensive tests for the new node structure:

```python
# ✅ Testing converted nodes

class TestUserTierClassificationNode:
    def test_premium_user_classification(self):
        node = UserTierClassificationNode()
        prep_result = {
            'user_context': Mock(subscription_tier='premium')
        }
        
        result = node.exec(prep_result)
        
        assert result['processing_tier'] == 'premium'
        assert result['model_type'] == 'premium_model'
    
    def test_basic_user_classification(self):
        node = UserTierClassificationNode()
        prep_result = {
            'user_context': Mock(subscription_tier='basic')
        }
        
        result = node.exec(prep_result)
        
        assert result['processing_tier'] == 'basic'
        assert result['model_type'] == 'basic_model'


class TestDataEnhancementNode:
    @patch('your_module.call_llm_enhance')
    def test_data_enhancement_with_premium_model(self, mock_enhance):
        mock_enhance.return_value = "enhanced data"
        
        node = DataEnhancementNode()
        prep_result = {
            'data': "raw data",
            'model_type': 'premium_model'
        }
        
        result = node.exec(prep_result)
        
        mock_enhance.assert_called_once_with("raw data", "premium_model")
        assert result['enhanced_data'] == "enhanced data"


class TestSmartDataProcessingFlow:
    @patch('your_module.call_llm_enhance')
    @patch('your_module.call_llm_quality_validator')
    def test_complete_premium_flow(self, mock_validator, mock_enhance):
        mock_enhance.return_value = "enhanced data"
        mock_validator.return_value = Mock(score=0.9)
        
        flow = SmartDataProcessingFlow()
        
        input_data = {
            'user_context': Mock(subscription_tier='premium'),
            'input_data': "raw data",
            'processing_options': Mock(quality_level='high', include_metadata=False)
        }
        
        result = flow.run(input_data)
        
        assert 'final_data' in result
        mock_enhance.assert_called()
        mock_validator.assert_called()


# ✅ Utility function tests remain simple
class TestPureUtilities:
    def test_safe_file_reader_success(self):
        with patch('builtins.open', mock_open(read_data="file content")):
            result = safe_file_reader("/path/to/file.txt")
            assert result == "file content"
    
    def test_safe_file_reader_failure(self):
        with patch('builtins.open', side_effect=IOError("File not found")):
            result = safe_file_reader("/nonexistent/file.txt")
            assert result is None
    
    def test_normalize_text(self):
        assert normalize_text("  hello   world  \n") == "hello world"
        assert normalize_text("") == ""
        assert normalize_text(None) == ""
```

### Step 8: Update Documentation and Integration Points (20 minutes)

```python
# Update imports and usage throughout codebase

# ❌ Before: Import utility function
from utils.data_processor import smart_data_processor

class SomeProcessingNode(Node):
    def exec(self, prep_result):
        result = smart_data_processor(...)  # ❌ Hidden business logic
        return result

# ✅ After: Use explicit node flow
from flows.smart_data_processing import SmartDataProcessingFlow

class SomeProcessingNode(Node):
    def exec(self, prep_result):
        flow = SmartDataProcessingFlow()
        result = flow.run(prep_result)  # ✅ Explicit business process
        return result['final_data']


# Update documentation
"""
Migration Notes:

BEFORE:
- smart_data_processor() utility handled user tier detection, data enhancement, 
  quality validation, and metadata extraction in a single function
- Business logic was hidden and hard to test
- LLM calls were scattered throughout utility functions

AFTER:  
- SmartDataProcessingFlow with 4 focused nodes:
  * UserTierClassificationNode: Subscription-based processing decisions
  * DataEnhancementNode: LLM-based data enhancement
  * QualityValidationNode: Quality assurance with business retry logic
  * MetadataExtractionNode: Business metadata extraction
- Each business decision is explicit and testable
- LLM calls are properly placed in node exec() methods
"""
```

## Success Criteria

✅ **Code Quality**
- No LLM calls in utility functions
- Complex branching logic (>2 branches) moved to nodes
- Business decisions are explicit in node exec() methods
- Utilities contain only pure, simple functions

✅ **Testing**
- Business logic is easily testable in dedicated nodes
- Utilities have simple, focused tests
- Complex scenarios are covered by node/flow tests
- Error handling business rules are testable

✅ **Architecture**
- Clear separation between pure utilities and business logic
- Business processes are visible in flow definitions
- Single responsibility principle followed
- Code is more maintainable and debuggable

## Time Estimates by Utility Complexity

| Utility Complexity | LLM Calls | Branches | Estimated Time |
|-------------------|-----------|----------|----------------|
| Simple (1 LLM call, 2-3 branches) | 1 | 2-3 | 1.5-2 hours |
| Medium (2-3 LLM calls, 4-5 branches) | 2-3 | 4-5 | 2-2.5 hours |  
| Complex (4+ LLM calls, 6+ branches) | 4+ | 6+ | 2.5-3+ hours |

Add time for:
- Multiple utilities to migrate: +1 hour per additional utility
- Complex integration points: +30 minutes per integration
- Extensive test updates: +45 minutes

## Troubleshooting

### Issue: "Utility is used in many places"
```python
# Problem: Widely-used utility affects many files
# Solution: Gradual migration with backward compatibility

# Step 1: Create new node-based implementation
class NewBusinessLogicFlow(Flow):
    # ... implementation

# Step 2: Create compatibility wrapper
def old_utility_function(*args, **kwargs):
    """DEPRECATED: Use NewBusinessLogicFlow instead"""
    warnings.warn("old_utility_function is deprecated", DeprecationWarning)
    
    flow = NewBusinessLogicFlow()
    # Convert args/kwargs to flow input format
    flow_input = convert_legacy_args(*args, **kwargs)
    result = flow.run(flow_input)
    return result['final_output']

# Step 3: Gradually migrate call sites
# Step 4: Remove deprecated function
```

### Issue: "Business logic is mixed with pure utilities"
```python
# Problem: Single function has both business logic and pure operations
def mixed_processor(data, config):
    # Pure operation ✅
    normalized = normalize_text(data)
    
    # Business logic ❌  
    if config.user_tier == 'premium':
        enhanced = call_llm_enhance(normalized)
    else:
        enhanced = normalized
    
    # Pure operation ✅
    formatted = format_output(enhanced)
    return formatted

# Solution: Split into pure utility + business node
def normalize_and_format(data, enhanced_data):
    """✅ Pure utility: text operations only"""
    normalized = normalize_text(data)
    formatted = format_output(enhanced_data)
    return formatted

class BusinessEnhancementNode(Node):
    """✅ Business logic: user tier decisions"""
    def exec(self, prep_result):
        data = prep_result['data']
        config = prep_result['config']
        
        normalized = normalize_text(data)  # Use pure utility
        
        if config.user_tier == 'premium':
            enhanced = call_llm_enhance(normalized)
        else:
            enhanced = normalized
        
        formatted = format_output(enhanced)  # Use pure utility
        return {'result': formatted}
```

## Related Guides

- [Monolithic to Focused Nodes](monolithic-to-focused.md) - For splitting large business logic
- [Fix Lifecycle Violations](fix-lifecycle-violations.md) - For proper node method placement
- [Remove Shared Store from exec()](remove-shared-store-exec.md) - For clean data access patterns