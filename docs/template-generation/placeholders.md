# Placeholder Philosophy: TODOs as Features

> **Why Generated Templates Have Intentional Placeholders**

## 🎯 Core Principle

**Missing implementations in generated templates are features, not bugs.**

The Agent OS + PocketFlow framework creates educational starting points for developers, not finished applications. Our intentional placeholder system teaches proper implementation patterns while providing clear guidance.

---

## Why Placeholders Matter

### 🎓 Educational Value
```python
# ❌ Bad: Completed implementation (hides learning opportunity)
def process_document(doc: Document) -> ProcessedDocument:
    return ProcessedDocument(content=doc.content.upper())

# ✅ Good: Educational placeholder (teaches proper pattern)
def process_document(doc: Document) -> ProcessedDocument:
    """
    Process a document using the configured processing strategy.
    
    TODO: Implement document processing logic:
    1. Validate input document format
    2. Apply transformation rules from self.config
    3. Handle errors gracefully with proper logging
    4. Return ProcessedDocument with metadata
    
    Example implementation approaches:
    - Text processing: NLP pipelines, content analysis
    - Data processing: Validation, transformation, enrichment
    - Media processing: Format conversion, quality optimization
    """
    raise NotImplementedError("Document processing logic needs implementation")
```

### 🏗️ Architectural Guidance
```python
# ✅ Shows proper PocketFlow node structure
class DocumentProcessorNode(Node):
    """Processes documents using configurable strategies."""
    
    async def prep(self, shared_store: SharedStore) -> Dict[str, Any]:
        """
        Prepare for document processing.
        
        TODO: Implement preparation logic:
        - Load processing configuration
        - Initialize external services
        - Validate required resources
        - Set up error handling
        """
        raise NotImplementedError("Prep phase needs implementation")
    
    async def exec(self, shared_store: SharedStore) -> Dict[str, Any]:
        """
        Execute document processing.
        
        TODO: Implement core processing:
        - Retrieve document from shared_store
        - Apply processing logic
        - Store results back to shared_store
        - Return execution metadata
        """
        raise NotImplementedError("Exec phase needs implementation")
    
    async def post(self, shared_store: SharedStore) -> Dict[str, Any]:
        """
        Post-process and cleanup.
        
        TODO: Implement cleanup logic:
        - Validate processing results
        - Clean up temporary resources
        - Log processing metrics
        - Prepare for next node
        """
        raise NotImplementedError("Post phase needs implementation")
```

---

## Types of Placeholders

### 1. Method Stubs
```python
def extract_entities(self, text: str) -> List[Entity]:
    """
    Extract named entities from text.
    
    TODO: Choose and implement entity extraction:
    - Option 1: spaCy NER pipeline
    - Option 2: Transformers-based models
    - Option 3: OpenAI API calls
    - Consider: Accuracy, speed, cost, privacy
    """
    raise NotImplementedError("Entity extraction needs implementation")
```

### 2. Configuration Templates
```python
class RAGConfig(BaseModel):
    """Configuration for RAG (Retrieval-Augmented Generation) system."""
    
    # TODO: Configure vector database
    vector_db_type: str = "chroma"  # or "pinecone", "faiss", "weaviate"
    vector_db_config: Dict[str, Any] = {}
    
    # TODO: Configure embedding model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimensions: int = 384
    
    # TODO: Configure retrieval settings
    top_k_results: int = 5
    similarity_threshold: float = 0.7
    
    # TODO: Configure generation model
    llm_provider: str = "openai"  # or "anthropic", "local"
    model_name: str = "gpt-4"
    max_tokens: int = 2000
```

### 3. Integration Points
```python
# TODO: Replace with your authentication system
async def authenticate_user(token: str) -> Optional[User]:
    """
    Authenticate user from token.
    
    Integration options:
    - JWT validation with your secret key
    - OAuth2 with your provider (Google, Auth0, etc.)
    - Custom authentication service
    - Session-based authentication
    """
    raise NotImplementedError("Authentication integration required")
```

### 4. Business Logic Stubs
```python
async def calculate_pricing(self, usage_data: UsageData) -> PricingResult:
    """
    Calculate pricing based on usage data.
    
    TODO: Implement your pricing logic:
    - Define pricing tiers and rates
    - Apply usage-based calculations
    - Handle discounts and promotions
    - Consider regional pricing variations
    - Implement billing cycle logic
    """
    raise NotImplementedError("Pricing logic needs your business rules")
```

---

## Quality Standards for Placeholders

### ✅ Good Placeholders Should:

1. **Explain What to Implement**
```python
# ✅ Clear explanation
def process_payment(self, payment_info: PaymentInfo) -> PaymentResult:
    """
    TODO: Integrate with your payment processor:
    - Validate payment information
    - Call payment gateway API (Stripe, PayPal, etc.)
    - Handle payment errors and retries
    - Store transaction records
    - Send confirmation notifications
    """
```

2. **Provide Implementation Options**
```python
# ✅ Shows multiple approaches
def store_embeddings(self, embeddings: List[Embedding]) -> None:
    """
    TODO: Choose vector storage solution:
    
    Option 1: Chroma (local development)
    Option 2: Pinecone (hosted, scalable)
    Option 3: Weaviate (self-hosted, advanced)
    Option 4: FAISS (high-performance, local)
    
    Consider: Cost, scale, query features, deployment
    """
```

3. **Include Example Patterns**
```python
# ✅ Shows implementation pattern
async def handle_workflow_error(self, error: Exception, context: Dict) -> None:
    """
    TODO: Implement error handling strategy:
    
    Example pattern:
    ```python
    if isinstance(error, RetryableError):
        await self.schedule_retry(context, delay=30)
    elif isinstance(error, ValidationError):
        await self.notify_user(error.message)
        await self.log_error(error, context)
    else:
        await self.escalate_error(error, context)
    ```
    """
```

### ❌ Bad Placeholders to Avoid:

```python
# ❌ No guidance
def do_something(self):
    pass

# ❌ Too vague
def process_data(self, data):
    # TODO: Process the data
    return data

# ❌ Completed implementation (wrong for templates)
def validate_email(self, email: str) -> bool:
    return "@" in email and "." in email
```

---

## Framework vs Usage Context

### In This Framework Repository:
- **We CREATE** placeholder templates
- **We TEST** that placeholders are educational
- **We MAINTAIN** placeholder quality standards
- **We DON'T** implement business logic

### In End-User Projects:
- **They RECEIVE** placeholder templates
- **They IMPLEMENT** the TODO stubs
- **They CUSTOMIZE** for their use case
- **They CREATE** working applications

---

## Best Practices for Framework Contributors

### When Adding New Templates:

1. **Make TODOs Educational**
   - Explain what needs implementation
   - Show multiple approaches
   - Include example patterns

2. **Maintain Clear Interfaces**
   - Define proper method signatures
   - Use type hints consistently
   - Document expected inputs/outputs

3. **Provide Context**
   - Explain when to use different options
   - Include performance considerations
   - Note security implications

4. **Test Placeholder Quality**
   - Ensure TODOs are actionable
   - Verify examples compile
   - Check educational value

Remember: Our placeholders are the bridge between framework generation and user implementation. Make them count!