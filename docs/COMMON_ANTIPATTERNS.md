# Common PocketFlow Antipatterns

> Version: 1.0.0  
> Date: 2025-01-04  
> Purpose: Catalog of common mistakes in PocketFlow implementations with corrections and prevention strategies

## Table of Contents

1. [Introduction](#introduction)
2. [Framework Context](#framework-context)
3. [Node Design Antipatterns](#node-design-antipatterns)
4. [Flow Architecture Antipatterns](#flow-architecture-antipatterns)
5. [Utility Function Antipatterns](#utility-function-antipatterns)
6. [Error Handling Antipatterns](#error-handling-antipatterns)
7. [Performance Antipatterns](#performance-antipatterns)
8. [Testing and Development Antipatterns](#testing-and-development-antipatterns)
9. [Detection and Prevention Tools](#detection-and-prevention-tools)

## Introduction

This document catalogs recurring mistakes found in PocketFlow implementations across multiple real-world projects. Each antipattern includes detection methods, specific corrections, and prevention strategies to help developers build better LLM applications.

### How to Use This Guide

- **For Code Reviews**: Reference specific antipatterns during review process
- **For Learning**: Study the "Why It's Problematic" sections to understand principles
- **For Validation**: Use detection patterns to identify issues in existing code
- **For Prevention**: Apply prevention strategies during initial design

### Severity Levels

- 🔴 **Critical**: Breaks core PocketFlow principles, causes failures
- 🟡 **High**: Significantly impacts maintainability or performance  
- 🟠 **Medium**: Creates technical debt or testing difficulties
- 🟢 **Low**: Style issues or minor inefficiencies

## Framework Context

🎯 **Framework vs Usage Statement**: This repository IS the Agent OS + PocketFlow framework itself - NOT a project using it.

**Framework Repository (this repo):**
- Generates PocketFlow templates for other projects
- Template placeholders and TODO stubs are intentional design features
- Missing implementations in generated templates are features, not bugs

**Usage Repository (end-user projects):**
- Where PocketFlow gets installed as a dependency
- Where generated templates become working applications
- Where these antipatterns would be actual problems to fix

## Node Design Antipatterns

### 1. Monolithic Node Syndrome 🔴

**Name**: Monolithic Node Syndrome  
**Description**: Single nodes that handle multiple distinct responsibilities, violating the single responsibility principle.

**Example (ANTIPATTERN):**
```python
class ProcessDocuments(Node):
    def exec(self, docs):
        # BAD: Multiple responsibilities in one node
        # 1. Data validation
        validated_docs = []
        for doc in docs:
            if self.validate_document(doc):
                validated_docs.append(doc)
        
        # 2. Text extraction  
        extracted_texts = []
        for doc in validated_docs:
            text = self.extract_text(doc)
            extracted_texts.append(text)
        
        # 3. Entity extraction
        entities = []
        for text in extracted_texts:
            entity = call_llm(f"Extract entities: {text}")
            entities.append(entity)
        
        # 4. Report generation
        report = self.generate_report(entities)
        
        # 5. Notification sending
        self.send_notifications(report)
        
        return report
```

**Why It's Problematic:**
- **Testing Complexity**: Single point of failure makes unit testing extremely difficult
- **Debugging Nightmare**: When failures occur, it's unclear which step failed
- **No Reusability**: Individual steps cannot be reused in other flows
- **Poor Error Handling**: One step's failure brings down the entire process
- **Scalability Issues**: Cannot optimize individual steps (e.g., parallelize entity extraction)

**Correction (GOOD):**
```python
class ValidateDocuments(BatchNode):
    """Single responsibility: Document validation"""
    def prep(self, shared):
        return shared["raw_documents"]
    
    def exec(self, document):
        return self.validate_document(document)
    
    def post(self, shared, prep_res, exec_res_list):
        # Filter out invalid documents
        valid_docs = [doc for doc, is_valid in zip(prep_res, exec_res_list) if is_valid]
        shared["validated_documents"] = valid_docs
        if len(valid_docs) == 0:
            return "no_valid_documents"
        return "validation_complete"

class ExtractText(BatchNode):
    """Single responsibility: Text extraction"""
    def prep(self, shared):
        return shared["validated_documents"]
    
    def exec(self, document):
        return extract_text(document)  # Simple utility call
    
    def post(self, shared, prep_res, exec_res_list):
        shared["document_texts"] = dict(zip(
            [doc.id for doc in prep_res], 
            exec_res_list
        ))
        return "extraction_complete"

class ExtractEntities(AsyncParallelBatchNode):
    """Single responsibility: Entity extraction with parallelization"""
    async def prep_async(self, shared):
        return list(shared["document_texts"].items())
    
    async def exec_async(self, doc_text_pair):
        doc_id, text = doc_text_pair
        entities = await call_llm_async(f"Extract entities from: {text}")
        return doc_id, entities
    
    async def post_async(self, shared, prep_res, exec_res_list):
        shared["document_entities"] = dict(exec_res_list)
        return "entities_complete"

class GenerateReport(Node):
    """Single responsibility: Report generation"""
    def prep(self, shared):
        return {
            "documents": shared["validated_documents"],
            "texts": shared["document_texts"], 
            "entities": shared["document_entities"]
        }
    
    def exec(self, data):
        return generate_comprehensive_report(
            data["documents"], 
            data["texts"], 
            data["entities"]
        )
    
    def post(self, shared, prep_res, exec_res):
        shared["final_report"] = exec_res
        return "report_complete"

class SendNotifications(Node):
    """Single responsibility: Notification delivery"""
    def prep(self, shared):
        return shared["final_report"]
    
    def exec(self, report):
        return send_notification_email(report)
    
    def post(self, shared, prep_res, exec_res):
        shared["notification_sent"] = exec_res
        return "notifications_complete"

# Clear flow with explicit branching
validate = ValidateDocuments()
extract_text = ExtractText()
extract_entities = ExtractEntities()  
generate_report = GenerateReport()
send_notifications = SendNotifications()

# Wire the flow with error paths
validate >> extract_text >> extract_entities >> generate_report >> send_notifications
validate - "no_valid_documents" >> error_handler

flow = AsyncFlow(start=validate)
```

**Detection**: 
- Look for nodes with multiple verbs in their names (ProcessAndValidateDocuments)
- exec() methods longer than 20 lines
- Multiple sequential LLM calls in single exec() method
- Nodes that both read and write multiple unrelated keys in shared store

**Prevention**: 
- Apply single responsibility principle: each node should do one thing well
- Break complex operations into pipeline stages
- Use descriptive node names that reflect single purpose
- Design flow diagrams first to identify natural breakpoints

---

### 2. Shared Store Access in exec() 🔴

**Name**: Shared Store Access in exec()  
**Description**: Accessing the shared store directly from within exec() methods, violating the prep/exec/post lifecycle.

**Example (ANTIPATTERN):**
```python
class BadUserProcessor(Node):
    def prep(self, shared):
        return shared["current_user_id"]
    
    def exec(self, user_id):
        # BAD: Direct shared store access in exec
        user_data = self.shared["users"][user_id]  # ❌ Breaks isolation
        preferences = self.shared["user_preferences"][user_id]  # ❌ Not testable
        
        # BAD: More shared store access
        if self.shared["is_premium_user"]:  # ❌ Breaks node isolation
            result = self.premium_processing(user_data, preferences)
        else:
            result = self.standard_processing(user_data, preferences)
        
        # BAD: Writing to shared store from exec
        self.shared["processing_count"] += 1  # ❌ Side effects in exec
        
        return result
```

**Why It's Problematic:**
- **Breaks Node Isolation**: exec() should be a pure function for testability
- **Makes Retry Logic Unpredictable**: Shared store may change between retries
- **Violates Separation of Concerns**: Data access mixed with computation
- **Impossible to Mock and Test**: Cannot isolate computation logic
- **Race Conditions**: Multiple nodes accessing shared store simultaneously
- **Debugging Difficulty**: Side effects hidden within computation

**Correction (GOOD):**
```python
class GoodUserProcessor(Node):
    def prep(self, shared):
        # GOOD: All data access in prep
        user_id = shared["current_user_id"]
        user_data = shared["users"][user_id]
        preferences = shared["user_preferences"][user_id]
        is_premium = shared["is_premium_user"]
        
        return {
            "user_id": user_id,
            "user_data": user_data,
            "preferences": preferences,
            "is_premium": is_premium
        }
    
    def exec(self, prep_result):
        # GOOD: Only use prep_result - pure function
        if prep_result["is_premium"]:
            result = self.premium_processing(
                prep_result["user_data"], 
                prep_result["preferences"]
            )
        else:
            result = self.standard_processing(
                prep_result["user_data"], 
                prep_result["preferences"]
            )
        
        return result
    
    def post(self, shared, prep_res, exec_res):
        # GOOD: All shared store writes in post
        shared["processed_users"][prep_res["user_id"]] = exec_res
        shared["processing_count"] = shared.get("processing_count", 0) + 1
        
        return "processing_complete"

# Easy to test exec() in isolation
def test_user_processor_exec():
    processor = GoodUserProcessor()
    prep_result = {
        "user_id": "123",
        "user_data": {"name": "Alice"},
        "preferences": {"theme": "dark"},
        "is_premium": True
    }
    
    result = processor.exec(prep_result)
    assert result["processed_successfully"] == True
```

**Detection**: 
- Search for `self.shared[` patterns inside exec() methods
- Look for exec() methods that access shared store directly
- Check for exec() methods that modify shared store directly
- Find exec() methods with side effects (database writes, API calls to update external state)

**Prevention**: 
- Follow the strict prep/exec/post lifecycle
- All data access in prep(), all computation in exec(), all state updates in post()
- Design exec() as a pure function that only uses its input parameter
- Use type hints to enforce input/output contracts

---

### 3. Lifecycle Method Confusion 🟡

**Name**: Lifecycle Method Confusion  
**Description**: Misunderstanding the purpose of prep/exec/post methods and placing logic in inappropriate phases.

**Example (ANTIPATTERN):**
```python
class BadAnalysisNode(Node):
    def prep(self, shared):
        # BAD: Computation in prep (should be in exec)
        data = shared["raw_data"]
        processed_data = self.complex_processing(data)  # ❌ Heavy computation
        analysis_result = call_llm(f"Analyze: {processed_data}")  # ❌ LLM call in prep
        return analysis_result
    
    def exec(self, prep_result):
        # BAD: Data access in exec (should be in prep)
        additional_context = self.shared["context_data"]  # ❌ Shared store access
        
        # BAD: Simple data manipulation (should be in prep)
        formatted_result = prep_result.upper()  # ❌ Trivial transformation
        return formatted_result
    
    def post(self, shared, prep_res, exec_res):
        # BAD: Complex logic in post (should be in exec)
        if "error" in exec_res:
            corrected_result = call_llm(f"Fix this error: {exec_res}")  # ❌ LLM call in post
            shared["analysis"] = corrected_result
        else:
            shared["analysis"] = exec_res
        return "complete"
```

**Why It's Problematic:**
- **Breaks Retry Logic**: LLM calls in prep() are not retried properly
- **Performance Issues**: Complex computation in prep() runs on every retry
- **Testing Complexity**: Cannot isolate and test individual phases properly
- **Violates Single Responsibility**: Each method should have one clear purpose
- **Error Handling Confusion**: Unclear which phase should handle different types of errors

**Correction (GOOD):**
```python
class GoodAnalysisNode(Node):
    def prep(self, shared):
        # GOOD: Only data gathering and simple preprocessing
        raw_data = shared["raw_data"]
        context_data = shared["context_data"]
        
        # Simple data preparation (no heavy computation)
        formatted_data = raw_data.strip().upper()
        
        return {
            "data": formatted_data,
            "context": context_data
        }
    
    def exec(self, prep_result):
        # GOOD: All computation and LLM calls here
        processed_data = self.complex_processing(prep_result["data"])
        
        # LLM calls belong in exec for proper retry handling
        analysis_result = call_llm(
            f"Analyze this data: {processed_data}\n"
            f"Context: {prep_result['context']}"
        )
        
        return {
            "analysis": analysis_result,
            "processed_data": processed_data
        }
    
    def post(self, shared, prep_res, exec_res):
        # GOOD: Simple state updates and flow control
        shared["analysis_result"] = exec_res["analysis"]
        shared["processed_data"] = exec_res["processed_data"]
        
        # Flow control based on results
        if "needs_review" in exec_res["analysis"].lower():
            return "requires_human_review"
        return "analysis_complete"

# If error correction is needed, create a separate node
class CorrectAnalysisErrors(Node):
    def prep(self, shared):
        return shared["analysis_result"]
    
    def exec(self, analysis_with_errors):
        # Proper place for error correction LLM calls
        return call_llm(f"Correct errors in: {analysis_with_errors}")
    
    def post(self, shared, prep_res, exec_res):
        shared["corrected_analysis"] = exec_res
        return "correction_complete"
```

**Detection**:
- LLM calls or heavy computation in prep() methods
- Shared store access in exec() methods  
- Complex business logic in post() methods
- prep() methods that return computed results instead of raw data
- post() methods that perform computation instead of just updating state

**Prevention**:
- **prep()**: Data gathering, simple formatting, validation
- **exec()**: All computation, LLM calls, complex processing
- **post()**: State updates, flow control decisions, result storage
- Use clear method documentation to specify responsibilities

---

## Flow Architecture Antipatterns

### 4. Hidden Flow Control 🟡

**Name**: Hidden Flow Control  
**Description**: Complex branching logic buried in utility functions instead of being visible in the flow diagram.

**Example (ANTIPATTERN):**
```python
# utils/document_processor.py - BAD: Hidden flow control
def process_document_with_routing(doc, shared_store):
    """BAD: Complex routing logic hidden in utility function"""
    
    # Hidden decision logic
    if doc.type == "legal":
        result = process_legal_document(doc)
        if result.urgency == "high":
            send_urgent_notification(result)
            shared_store["urgent_cases"].append(doc.id)
            return "urgent_legal"
        elif result.compliance_issues:
            assign_to_specialist(result)
            shared_store["compliance_queue"].append(doc.id)
            return "compliance_review"
        else:
            shared_store["processed_legal"].append(result)
            return "legal_complete"
    
    elif doc.type == "financial":
        result = process_financial_document(doc)
        if result.amount > 10000:
            require_approval(result)
            shared_store["approval_queue"].append(doc.id)
            return "needs_approval"
        else:
            shared_store["processed_financial"].append(result)
            return "financial_complete"
    
    else:
        # More hidden logic...
        return process_generic_document(doc, shared_store)

class BadDocumentNode(Node):
    """Flow diagram doesn't show the complex branching that happens"""
    def exec(self, document):
        # BAD: All decision logic hidden in utility
        return process_document_with_routing(document, shared)
    
    def post(self, shared, prep_res, exec_res):
        # BAD: Utility function already modified shared store
        return exec_res  # Could be many different values
```

**Why It's Problematic:**
- **Invisible Flow Logic**: Decision points not visible in flow diagrams
- **Testing Nightmare**: Cannot test individual decision branches in isolation
- **Debugging Complexity**: Hard to understand which path was taken
- **Poor Maintainability**: Changes require modifying utility functions instead of flows
- **Violates Transparency**: Business logic hidden from high-level view

**Correction (GOOD):**
```python
# utils/document_service.py - Simple external interfaces
def extract_document_metadata(doc):
    """Simple utility - just external interface"""
    return {
        "type": doc.type,
        "urgency": doc.urgency,
        "amount": getattr(doc, 'amount', 0)
    }

def process_legal_document(doc):
    """Simple utility - no decision logic"""
    return legal_processing_service.process(doc)

def send_urgent_notification(doc_id, result):
    """Simple utility - just external interface"""
    notification_service.send_urgent_alert(doc_id, result)

# All decision logic in nodes - visible in flow
class ClassifyDocument(Node):
    """Clear single responsibility: document classification"""
    def prep(self, shared):
        return shared["current_document"]
    
    def exec(self, document):
        metadata = extract_document_metadata(document)
        return metadata
    
    def post(self, shared, prep_res, exec_res):
        shared["document_metadata"] = exec_res
        # Clear branching visible in flow
        return exec_res["type"]  # "legal", "financial", "generic"

class ProcessLegalDocument(Node):
    """Handles legal document processing"""
    def prep(self, shared):
        return shared["current_document"]
    
    def exec(self, document):
        return process_legal_document(document)
    
    def post(self, shared, prep_res, exec_res):
        shared["legal_result"] = exec_res
        
        # Clear decision logic in post
        if exec_res.urgency == "high":
            return "urgent"
        elif exec_res.compliance_issues:
            return "compliance_review"
        else:
            return "complete"

class HandleUrgentLegal(Node):
    """Handles urgent legal documents"""  
    def prep(self, shared):
        return shared["current_document"].id, shared["legal_result"]
    
    def exec(self, doc_result):
        doc_id, result = doc_result
        send_urgent_notification(doc_id, result)
        return {"notified": True, "doc_id": doc_id}
    
    def post(self, shared, prep_res, exec_res):
        shared["urgent_cases"].append(exec_res["doc_id"])
        return "urgent_handled"

# Flow makes all decision paths visible
classify = ClassifyDocument()
process_legal = ProcessLegalDocument()  
process_financial = ProcessFinancialDocument()
process_generic = ProcessGenericDocument()
handle_urgent = HandleUrgentLegal()
handle_compliance = HandleComplianceReview()

# Clear flow diagram shows all paths
classify - "legal" >> process_legal
classify - "financial" >> process_financial  
classify - "generic" >> process_generic

process_legal - "urgent" >> handle_urgent
process_legal - "compliance_review" >> handle_compliance
process_legal - "complete" >> finalize_processing

flow = Flow(start=classify)
```

**Detection**:
- Utility functions that return different string values for flow control
- Utility functions that modify shared store directly
- Complex if/else chains in utility functions
- Utility functions with names like "process_and_route" or "handle_with_logic"
- exec() methods that just call one complex utility function

**Prevention**:
- Keep utilities simple and focused on external interfaces
- Make all decision logic explicit in node post() methods
- Use clear action names for flow branching
- Create flow diagrams first to identify decision points

---

### 5. Synchronous Collection Processing 🟠

**Name**: Synchronous Collection Processing  
**Description**: Using loops within regular nodes to process collections instead of using BatchNode or AsyncParallelBatchNode.

**Example (ANTIPATTERN):**
```python
class ProcessFiles(Node):
    def exec(self, file_list):
        # BAD: Manual iteration in regular node
        results = []
        for file_path in file_list:
            try:
                # Sequential processing - no parallelization
                content = read_file(file_path)
                summary = call_llm(f"Summarize: {content}")
                analysis = call_llm(f"Analyze sentiment: {summary}")
                
                results.append({
                    "file": file_path,
                    "summary": summary, 
                    "analysis": analysis
                })
            except Exception as e:
                # BAD: Individual failures affect entire collection
                results.append({
                    "file": file_path,
                    "error": str(e)
                })
        
        return results  # All processed sequentially

class AnalyzeUsers(Node):
    def prep(self, shared):
        return shared["user_ids"]  # List of 1000 user IDs
    
    def exec(self, user_ids):
        # BAD: Sequential API calls - very slow
        user_analyses = []
        for user_id in user_ids:
            user_data = fetch_user_data(user_id)  # API call
            analysis = call_llm(f"Analyze user: {user_data}")  # LLM call
            user_analyses.append({
                "user_id": user_id,
                "analysis": analysis
            })
        
        return user_analyses  # Takes forever for large collections
```

**Why It's Problematic:**
- **No Parallel Processing**: Sequential execution is extremely slow
- **All-or-Nothing Failure**: One item failure can break entire collection
- **No Progress Tracking**: Can't monitor progress of large collections
- **Memory Issues**: Loading all results at once for large collections
- **Retry Complexity**: Retrying affects entire collection, not individual items
- **Resource Waste**: Cannot optimize individual item processing

**Correction (GOOD):**
```python
class ProcessFiles(AsyncParallelBatchNode):
    """Parallel file processing with proper error handling"""
    
    async def prep_async(self, shared):
        # Return the collection to be processed
        return shared["file_list"]
    
    async def exec_async(self, single_file):
        # GOOD: Processes each file independently and in parallel
        content = await read_file_async(single_file)
        summary = await call_llm_async(f"Summarize: {content}")
        analysis = await call_llm_async(f"Analyze sentiment: {summary}")
        
        return {
            "file": single_file,
            "summary": summary,
            "analysis": analysis
        }
    
    async def post_async(self, shared, prep_res, exec_res_list):
        # GOOD: Results collected after all items processed
        shared["file_analyses"] = exec_res_list
        
        # Can analyze results and handle partial failures
        successful = [r for r in exec_res_list if "error" not in r]
        failed = [r for r in exec_res_list if "error" in r]
        
        shared["processing_stats"] = {
            "total": len(prep_res),
            "successful": len(successful),
            "failed": len(failed)
        }
        
        if len(failed) > len(successful):
            return "mostly_failed"
        elif len(failed) > 0:
            return "partial_success"
        else:
            return "all_success"

class AnalyzeUsers(AsyncParallelBatchNode):
    """Parallel user analysis with rate limiting"""
    
    def __init__(self, max_concurrent=10, **kwargs):
        super().__init__(**kwargs)
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def prep_async(self, shared):
        return shared["user_ids"]
    
    async def exec_async(self, user_id):
        # GOOD: Rate limiting to avoid API throttling
        async with self.semaphore:
            user_data = await fetch_user_data_async(user_id)
            analysis = await call_llm_async(f"Analyze user: {user_data}")
            
            return {
                "user_id": user_id,
                "analysis": analysis,
                "processed_at": datetime.utcnow().isoformat()
            }
    
    async def post_async(self, shared, prep_res, exec_res_list):
        shared["user_analyses"] = exec_res_list
        return "analysis_complete"

# For CPU-bound collections, use BatchNode (not parallel)
class ProcessDataBatch(BatchNode):
    """Use BatchNode for CPU-intensive work that doesn't benefit from async"""
    
    def prep(self, shared):
        return shared["data_items"]
    
    def exec(self, single_item):
        # CPU-intensive processing that doesn't need async
        return self.complex_cpu_computation(single_item)
    
    def post(self, shared, prep_res, exec_res_list):
        shared["processed_items"] = exec_res_list
        return "batch_complete"
```

**Detection**:
- for loops in exec() methods processing collections
- Nodes named with plural nouns using regular Node class (ProcessFiles, AnalyzeUsers)
- Sequential API calls or LLM calls in loops
- exec() methods that take lists as input and return lists as output

**Prevention**:
- Use BatchNode for collection processing
- Use AsyncParallelBatchNode for I/O-bound parallel processing
- Implement rate limiting for external service calls
- Design for individual item failure handling

---

## Utility Function Antipatterns

### 6. Business Logic in Utilities 🟡

**Name**: Business Logic in Utilities  
**Description**: Placing complex business logic, LLM calls, or decision-making in utility functions instead of nodes.

**Example (ANTIPATTERN):**
```python
# utils/customer_processor.py - BAD: Complex business logic in utility
def process_customer_inquiry(inquiry, customer_data, shared_store):
    """BAD: This utility contains complex business decisions"""
    
    # BAD: Business logic for customer classification
    if customer_data["tier"] == "premium":
        priority = "high"
    elif customer_data["complaints"] > 3:
        priority = "urgent"
    elif "cancel" in inquiry.lower() or "refund" in inquiry.lower():
        priority = "retention"
    else:
        priority = "normal"
    
    # BAD: LLM call hidden in utility
    sentiment = call_llm(f"Analyze sentiment: {inquiry}")
    
    # BAD: Complex routing logic
    if sentiment == "angry" and priority != "urgent":
        priority = "escalated"
        # BAD: Side effect - sending notification
        send_manager_alert(customer_data["id"], inquiry)
    
    # BAD: Multiple decision branches
    if priority == "retention":
        response = call_llm(f"""
        Customer inquiry: {inquiry}
        Customer tier: {customer_data['tier']}
        Generate retention-focused response with special offers.
        """)
        # BAD: Modifying shared store from utility
        shared_store["retention_cases"].append(customer_data["id"])
    else:
        response = call_llm(f"Generate professional response: {inquiry}")
    
    # BAD: More business logic
    if len(response) > 500:
        response = call_llm(f"Shorten this response: {response}")
    
    return {
        "response": response,
        "priority": priority,
        "sentiment": sentiment
    }

# Node just calls the complex utility - flow is invisible
class CustomerServiceNode(Node):
    def exec(self, inquiry_data):
        # BAD: All logic hidden in utility
        return process_customer_inquiry(
            inquiry_data["inquiry"],
            inquiry_data["customer"], 
            shared
        )
```

**Why It's Problematic:**
- **Invisible Business Logic**: Decision points not visible in flow diagrams
- **Untestable Components**: Cannot test individual decision branches
- **Hidden LLM Calls**: Cannot optimize, cache, or monitor LLM usage
- **Side Effects**: Utilities performing actions like sending notifications
- **Poor Maintainability**: Business rules scattered across utility functions
- **Violation of Single Responsibility**: Utilities doing too many things

**Correction (GOOD):**
```python
# utils/customer_service.py - Simple external interfaces only
def get_customer_data(customer_id):
    """Simple utility - just data access"""
    return database.get_customer(customer_id)

def send_manager_alert(customer_id, inquiry):
    """Simple utility - just external notification"""
    return notification_service.send_alert(customer_id, inquiry)

def save_customer_response(customer_id, response):
    """Simple utility - just data persistence"""
    return database.save_response(customer_id, response)

# Business logic in nodes - visible in flow
class ClassifyCustomerInquiry(Node):
    """Single responsibility: classify customer and inquiry priority"""
    
    def prep(self, shared):
        return {
            "inquiry": shared["customer_inquiry"],
            "customer": shared["customer_data"]
        }
    
    def exec(self, data):
        inquiry = data["inquiry"]
        customer = data["customer"]
        
        # Clear business logic in node
        if customer["tier"] == "premium":
            priority = "high"
        elif customer["complaints"] > 3:
            priority = "urgent" 
        elif "cancel" in inquiry.lower() or "refund" in inquiry.lower():
            priority = "retention"
        else:
            priority = "normal"
        
        return {"priority": priority}
    
    def post(self, shared, prep_res, exec_res):
        shared["inquiry_priority"] = exec_res["priority"]
        return exec_res["priority"]  # Branch on priority

class AnalyzeSentiment(Node):
    """Single responsibility: sentiment analysis"""
    
    def prep(self, shared):
        return shared["customer_inquiry"]
    
    def exec(self, inquiry):
        return call_llm(f"Analyze sentiment (happy/neutral/frustrated/angry): {inquiry}")
    
    def post(self, shared, prep_res, exec_res):
        shared["inquiry_sentiment"] = exec_res
        return exec_res  # Branch on sentiment

class HandleRetentionCase(Node):
    """Single responsibility: retention-specific responses"""
    
    def prep(self, shared):
        return {
            "inquiry": shared["customer_inquiry"],
            "customer": shared["customer_data"]
        }
    
    def exec(self, data):
        return call_llm(f"""
        Customer inquiry: {data['inquiry']}
        Customer tier: {data['customer']['tier']}
        Generate retention-focused response with special offers.
        """)
    
    def post(self, shared, prep_res, exec_res):
        shared["customer_response"] = exec_res
        shared["retention_cases"] = shared.get("retention_cases", [])
        shared["retention_cases"].append(prep_res["customer"]["id"])
        
        if len(exec_res) > 500:
            return "needs_shortening"
        return "retention_complete"

class ShortenResponse(Node):
    """Single responsibility: response length optimization"""
    
    def prep(self, shared):
        return shared["customer_response"]
    
    def exec(self, long_response):
        return call_llm(f"Shorten this response to under 500 characters: {long_response}")
    
    def post(self, shared, prep_res, exec_res):
        shared["customer_response"] = exec_res
        return "response_ready"

# Flow makes all decision paths visible
classify = ClassifyCustomerInquiry()
analyze_sentiment = AnalyzeSentiment()
handle_retention = HandleRetentionCase()
handle_urgent = HandleUrgentCase()
generate_standard = GenerateStandardResponse()
shorten_response = ShortenResponse()

# Clear branching based on classification
classify - "retention" >> handle_retention
classify - "urgent" >> handle_urgent  
classify - "high" >> generate_standard
classify - "normal" >> generate_standard

# Response length handling
handle_retention - "needs_shortening" >> shorten_response
generate_standard - "needs_shortening" >> shorten_response

flow = Flow(start=classify)
```

**Detection**:
- Utility functions with multiple if/else branches
- LLM calls inside utility functions
- Utility functions that modify shared store or have side effects
- Utility functions with business domain names (process_order, handle_customer)
- Complex utility functions with multiple responsibilities

**Prevention**:
- Keep utilities focused on external interfaces only
- Move all business logic into nodes
- Use clear node names that reflect business operations
- Make decision points explicit in flow diagrams

---

### 7. Trivial Utility Overuse 🟢

**Name**: Trivial Utility Overuse  
**Description**: Creating utility functions for simple operations that could be done directly in nodes.

**Example (ANTIPATTERN):**
```python
# utils/string_helpers.py - BAD: Over-engineered simple operations
def uppercase_text(text):
    """BAD: Trivial operation wrapped in utility"""
    return text.upper()

def lowercase_text(text):
    """BAD: Built-in operation wrapped unnecessarily"""
    return text.lower()

def join_with_commas(items):
    """BAD: Simple join operation over-abstracted"""
    return ", ".join(items)

def get_text_length(text):
    """BAD: Built-in len() wrapped for no reason"""
    return len(text)

def add_prefix(text, prefix):
    """BAD: Simple string concatenation wrapped"""
    return f"{prefix}{text}"

# utils/list_helpers.py - More trivial operations
def get_first_item(items):
    """BAD: Simple indexing wrapped"""
    return items[0] if items else None

def count_items(items):
    """BAD: Built-in len() wrapped again"""
    return len(items)

def reverse_list(items):
    """BAD: Built-in reverse wrapped"""
    return list(reversed(items))

# Node using trivial utilities - hard to understand actual logic
class TextProcessor(Node):
    def exec(self, raw_text):
        # BAD: Logic obscured by trivial utility calls
        clean_text = uppercase_text(raw_text)
        text_length = get_text_length(clean_text)
        
        if text_length > 100:
            return add_prefix(clean_text, "LONG: ")
        else:
            return add_prefix(clean_text, "SHORT: ")
```

**Why It's Problematic:**
- **Obscures Simple Logic**: Makes code harder to read and understand
- **Unnecessary Abstraction**: Adds complexity without benefit
- **Testing Overhead**: Creates more functions to test for no reason
- **Import Bloat**: Excessive imports make files cluttered
- **Performance Overhead**: Function call overhead for trivial operations
- **Maintenance Burden**: More code to maintain for simple operations

**Correction (GOOD):**
```python
# No utility files for trivial operations

class TextProcessor(Node):
    """Clear, direct implementation"""
    
    def exec(self, raw_text):
        # GOOD: Direct, clear operations
        clean_text = raw_text.upper()
        
        if len(clean_text) > 100:
            return f"LONG: {clean_text}"
        else:
            return f"SHORT: {clean_text}"

class ListProcessor(Node):
    """Direct list operations"""
    
    def prep(self, shared):
        return shared["items"]
    
    def exec(self, items):
        # GOOD: Clear, direct list operations
        if not items:
            return {"result": "empty", "count": 0}
        
        first_item = items[0]
        item_count = len(items)
        reversed_items = list(reversed(items))
        
        return {
            "first": first_item,
            "count": item_count, 
            "reversed": reversed_items,
            "summary": ", ".join(items[:3])  # Direct join
        }

# Only create utilities for meaningful abstractions
# utils/document_service.py - Good utilities
def extract_text_from_pdf(pdf_path):
    """Meaningful utility - complex external operation"""
    import PyPDF2
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def save_to_database(data, table_name):
    """Meaningful utility - external system interaction"""
    connection = database.get_connection()
    return connection.execute(
        f"INSERT INTO {table_name} VALUES (?)", 
        data
    )
```

**Detection**:
- Utility functions that just wrap built-in Python operations
- Utility functions shorter than 3 lines
- Utilities that don't interact with external systems
- One-liner functions that add no meaningful abstraction
- Utilities that just rearrange parameters to built-in functions

**Prevention**:
- Only create utilities for external system interactions
- Use built-in operations directly in nodes
- Ask "Does this utility add meaningful value?" before creating it
- Focus utilities on complex operations or external interfaces

---

## Error Handling Antipatterns

### 8. Exception Handling for Flow Control 🟡

**Name**: Exception Handling for Flow Control  
**Description**: Using try/catch blocks within exec() methods to handle business logic instead of using flow branching.

**Example (ANTIPATTERN):**
```python
class BadOrderProcessor(Node):
    def exec(self, order_data):
        try:
            # BAD: Using exceptions for business flow control
            payment_result = process_payment(order_data["payment"])
            
            if payment_result.status == "declined":
                # BAD: Throwing exception for normal business scenario
                raise PaymentDeclinedException("Payment was declined")
            
            if payment_result.amount > 1000:
                # BAD: Exception for business rule
                raise RequiresApprovalException("Large payment needs approval")
            
            shipping_result = arrange_shipping(order_data["shipping"])
            
            if not shipping_result.available:
                # BAD: Exception for normal business scenario  
                raise ShippingUnavailableException("Shipping not available")
            
            return {
                "payment": payment_result,
                "shipping": shipping_result,
                "status": "complete"
            }
            
        except PaymentDeclinedException:
            # BAD: Inline handling of business logic
            return self.handle_declined_payment(order_data)
        except RequiresApprovalException:
            # BAD: Business logic in exception handler
            return self.request_manager_approval(order_data)
        except ShippingUnavailableException:
            # BAD: Alternative flow in exception handler
            return self.try_alternative_shipping(order_data)
        except Exception as e:
            # BAD: Mixing technical and business exceptions
            return {"status": "error", "message": str(e)}

    def handle_declined_payment(self, order_data):
        # More hidden business logic...
        pass
```

**Why It's Problematic:**
- **Invisible Flow Paths**: Exception paths don't appear in flow diagrams
- **Testing Complexity**: Hard to test all exception scenarios
- **Performance Overhead**: Exception handling is computationally expensive
- **Mixed Concerns**: Business logic mixed with error handling
- **Retry Confusion**: Node retry mechanism conflicts with exception handling
- **Debugging Difficulty**: Stack traces for business logic scenarios

**Correction (GOOD):**
```python
class ProcessPayment(Node):
    """Single responsibility: payment processing with clear outcomes"""
    
    def prep(self, shared):
        return shared["order_data"]["payment"]
    
    def exec(self, payment_data):
        # GOOD: Let technical exceptions bubble up for retry
        payment_result = process_payment(payment_data)
        return payment_result
    
    def post(self, shared, prep_res, exec_res):
        shared["payment_result"] = exec_res
        
        # GOOD: Clear business flow branching
        if exec_res.status == "declined":
            return "payment_declined"
        elif exec_res.amount > 1000:
            return "requires_approval"
        else:
            return "payment_success"

class HandleDeclinedPayment(Node):
    """Handles declined payment scenario"""
    
    def prep(self, shared):
        return {
            "order": shared["order_data"],
            "payment_result": shared["payment_result"]
        }
    
    def exec(self, data):
        # Business logic for handling declined payments
        return self.process_payment_decline(data["order"], data["payment_result"])
    
    def post(self, shared, prep_res, exec_res):
        shared["decline_handling"] = exec_res
        return "decline_handled"

class RequestApproval(Node):
    """Handles approval request for large payments"""
    
    def prep(self, shared):
        return shared["order_data"], shared["payment_result"]
    
    def exec(self, order_payment):
        order, payment = order_payment
        return request_manager_approval(order, payment)
    
    def post(self, shared, prep_res, exec_res):
        shared["approval_request"] = exec_res
        return "approval_requested"

class ArrangeShipping(Node):
    """Handles shipping arrangement"""
    
    def prep(self, shared):
        return shared["order_data"]["shipping"]
    
    def exec(self, shipping_data):
        return arrange_shipping(shipping_data)
    
    def post(self, shared, prep_res, exec_res):
        shared["shipping_result"] = exec_res
        
        if not exec_res.available:
            return "shipping_unavailable"
        else:
            return "shipping_arranged"

# Flow makes all business paths visible
process_payment = ProcessPayment()
handle_declined = HandleDeclinedPayment()
request_approval = RequestApproval()
arrange_shipping = ArrangeShipping()
try_alternative = TryAlternativeShipping()
complete_order = CompleteOrder()

# Clear flow diagram shows all business scenarios
process_payment - "payment_declined" >> handle_declined
process_payment - "requires_approval" >> request_approval
process_payment - "payment_success" >> arrange_shipping

arrange_shipping - "shipping_unavailable" >> try_alternative
arrange_shipping - "shipping_arranged" >> complete_order

flow = Flow(start=process_payment)
```

**Detection**:
- try/catch blocks in exec() methods that don't re-raise exceptions
- Custom exception classes for business scenarios
- Exception handlers that return different result types
- exec() methods with multiple exception handlers
- Business logic inside exception handlers

**Prevention**:
- Use exceptions only for technical failures (network errors, API timeouts)
- Use return values and flow branching for business logic
- Let technical exceptions bubble up to node retry mechanism
- Make all business decision points explicit in flow diagram

---

### 9. Missing Error Recovery Paths 🟠

**Name**: Missing Error Recovery Paths  
**Description**: Failing to plan and implement recovery paths for common failure scenarios.

**Example (ANTIPATTERN):**
```python
class BadDataProcessor(Node):
    def exec(self, data_batch):
        # BAD: No consideration of failure scenarios
        processed_results = []
        
        for item in data_batch:
            # What if LLM call fails?
            result = call_llm(f"Process: {item}")
            processed_results.append(result)
        
        # What if external service is down?
        validation_results = external_validation_service.validate_batch(processed_results)
        
        # What if database is unavailable?
        database.save_results(validation_results)
        
        return validation_results
    
    def post(self, shared, prep_res, exec_res):
        # BAD: No handling of partial failures or error states
        shared["results"] = exec_res
        return "complete"  # Only one outcome considered

# Flow only handles happy path
process_node = BadDataProcessor()
finalize_node = FinalizeResults()
process_node >> finalize_node  # What happens when process_node fails?

flow = Flow(start=process_node)
```

**Why It's Problematic:**
- **Brittle System**: Single points of failure bring down entire process
- **No Graceful Degradation**: System fails completely on any error
- **Poor User Experience**: No feedback or recovery options for failures
- **Data Loss Risk**: Partial work lost when failures occur
- **No Monitoring**: Cannot track or alert on failure scenarios
- **Difficult Debugging**: No visibility into failure modes

**Correction (GOOD):**
```python
class ProcessDataBatch(AsyncParallelBatchNode):
    """Robust data processing with error handling"""
    
    async def prep_async(self, shared):
        return shared["data_batch"]
    
    async def exec_async(self, single_item):
        # Individual item processing with built-in retry
        result = await call_llm_async(f"Process: {single_item}")
        return {"item_id": single_item.id, "result": result}
    
    async def post_async(self, shared, prep_res, exec_res_list):
        # Analyze results and plan recovery
        successful = [r for r in exec_res_list if "error" not in r]
        failed = [r for r in exec_res_list if "error" in r]
        
        shared["processing_results"] = {
            "successful": successful,
            "failed": failed,
            "total": len(prep_res)
        }
        
        failure_rate = len(failed) / len(prep_res)
        
        if failure_rate > 0.5:
            return "high_failure_rate"  # Too many failures - escalate
        elif len(failed) > 0:
            return "partial_failure"    # Some failures - retry failed items
        else:
            return "all_success"        # Continue to validation

class RetryFailedItems(Node):
    """Retry processing for failed items"""
    
    def prep(self, shared):
        failed_items = shared["processing_results"]["failed"]
        return [item["item_id"] for item in failed_items]
    
    def exec(self, failed_item_ids):
        # Different processing strategy for failed items
        retry_results = []
        for item_id in failed_item_ids:
            try:
                # Try simpler processing for failed items
                result = call_llm(f"Simple process: {item_id}", model="fast-model")
                retry_results.append({"item_id": item_id, "result": result, "retried": True})
            except Exception as e:
                # Mark as permanently failed
                retry_results.append({"item_id": item_id, "error": str(e), "permanent_failure": True})
        
        return retry_results
    
    def post(self, shared, prep_res, exec_res):
        # Merge retry results with original successful results
        original_successful = shared["processing_results"]["successful"]
        retry_successful = [r for r in exec_res if "error" not in r]
        permanently_failed = [r for r in exec_res if "permanent_failure" in r]
        
        shared["final_results"] = {
            "successful": original_successful + retry_successful,
            "permanently_failed": permanently_failed
        }
        
        if len(permanently_failed) > 0:
            return "has_permanent_failures"
        else:
            return "retry_success"

class ValidateResults(Node):
    """Validation with fallback strategies"""
    
    def prep(self, shared):
        return shared["final_results"]["successful"]
    
    def exec(self, successful_results):
        try:
            # Try primary validation service
            return external_validation_service.validate_batch(successful_results)
        except ServiceUnavailableException:
            # Fallback to local validation
            return self.local_validation(successful_results)
        except Exception as e:
            # Log error but don't fail - return results with validation warning
            return {
                "results": successful_results,
                "validation_error": str(e),
                "validated": False
            }
    
    def post(self, shared, prep_res, exec_res):
        shared["validated_results"] = exec_res
        
        if "validation_error" in exec_res:
            return "validation_failed"
        else:
            return "validation_complete"

class SaveResults(Node):
    """Database save with backup strategies"""
    
    def prep(self, shared):
        return shared["validated_results"]
    
    def exec(self, results):
        try:
            # Try primary database
            database.save_results(results)
            return {"saved_to": "primary_db", "results": results}
        except DatabaseUnavailableException:
            # Fallback to backup database
            backup_database.save_results(results)
            return {"saved_to": "backup_db", "results": results}
        except Exception as e:
            # Final fallback - save to file system
            filepath = self.save_to_file(results)
            return {"saved_to": "filesystem", "filepath": filepath, "results": results}
    
    def post(self, shared, prep_res, exec_res):
        shared["save_result"] = exec_res
        
        if exec_res["saved_to"] != "primary_db":
            return "used_fallback_storage"
        else:
            return "saved_successfully"

class HandlePermanentFailures(Node):
    """Handle items that couldn't be processed"""
    
    def prep(self, shared):
        return shared["final_results"]["permanently_failed"]
    
    def exec(self, failed_items):
        # Create failure report and notify administrators
        failure_report = self.create_failure_report(failed_items)
        self.notify_administrators(failure_report)
        
        return failure_report
    
    def post(self, shared, prep_res, exec_res):
        shared["failure_report"] = exec_res
        return "failures_reported"

# Flow with comprehensive error paths
process_batch = ProcessDataBatch()
retry_failed = RetryFailedItems()
validate_results = ValidateResults()
save_results = SaveResults()
handle_failures = HandlePermanentFailures()
escalate_failures = EscalateToHuman()
notify_fallback = NotifyFallbackUsed()

# Main flow with recovery paths
process_batch - "all_success" >> validate_results
process_batch - "partial_failure" >> retry_failed
process_batch - "high_failure_rate" >> escalate_failures

retry_failed - "retry_success" >> validate_results
retry_failed - "has_permanent_failures" >> handle_failures

validate_results - "validation_complete" >> save_results
validate_results - "validation_failed" >> save_results  # Continue with warning

save_results - "saved_successfully" >> finalize_results
save_results - "used_fallback_storage" >> notify_fallback

handle_failures >> finalize_results  # Continue even with some failures

flow = AsyncFlow(start=process_batch)
```

**Detection**:
- Nodes with only one return path from post()
- Flows with no error handling nodes
- exec() methods that don't handle external service failures
- Missing fallback strategies for external dependencies
- No partial failure handling in batch operations

**Prevention**:
- Plan error scenarios during flow design
- Create explicit error handling nodes
- Implement fallback strategies for external services
- Design for partial failures in batch operations
- Include error paths in flow diagrams

---

## Performance Antipatterns

### 10. Blocking I/O in Regular Nodes 🟠

**Name**: Blocking I/O in Regular Nodes  
**Description**: Using synchronous I/O operations in regular Node classes instead of AsyncNode.

**Example (ANTIPATTERN):**
```python
class BadAPIProcessor(Node):
    def exec(self, api_requests):
        # BAD: Synchronous I/O blocks the entire process
        results = []
        
        for request in api_requests:
            # BAD: Blocking network call in regular node
            response = requests.get(request.url, timeout=30)
            
            # BAD: Blocking LLM call
            analysis = call_llm(f"Analyze this API response: {response.text}")
            
            # BAD: Blocking database write
            database.save_analysis(request.id, analysis)
            
            results.append({
                "request_id": request.id,
                "analysis": analysis
            })
        
        return results  # Everything processed sequentially

class BadFileProcessor(Node):
    def prep(self, shared):
        # BAD: Blocking file I/O in prep
        files_data = []
        for file_path in shared["file_paths"]:
            # Blocks while reading each file
            with open(file_path, 'r') as f:
                content = f.read()
            files_data.append({"path": file_path, "content": content})
        
        return files_data
    
    def exec(self, files_data):
        # More blocking operations...
        summaries = []
        for file_data in files_data:
            # Blocking LLM call
            summary = call_llm(f"Summarize: {file_data['content']}")
            summaries.append(summary)
        
        return summaries
```

**Why It's Problematic:**
- **Poor Performance**: Sequential I/O operations are extremely slow
- **Resource Waste**: CPU idle while waiting for I/O operations
- **No Concurrency Benefits**: Cannot process multiple items simultaneously
- **Poor Scalability**: Performance degrades linearly with data size
- **User Experience**: Long wait times for simple operations
- **Inefficient Resource Usage**: Cannot utilize async capabilities of modern systems

**Correction (GOOD):**
```python
class GoodAPIProcessor(AsyncParallelBatchNode):
    """Async I/O with proper parallelization"""
    
    def __init__(self, max_concurrent=10, **kwargs):
        super().__init__(**kwargs)
        self.session = None
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def prep_async(self, shared):
        # Set up async HTTP session
        import aiohttp
        self.session = aiohttp.ClientSession()
        return shared["api_requests"]
    
    async def exec_async(self, single_request):
        # GOOD: Async I/O with rate limiting
        async with self.semaphore:
            async with self.session.get(single_request.url, timeout=30) as response:
                response_text = await response.text()
            
            # GOOD: Async LLM call
            analysis = await call_llm_async(f"Analyze this API response: {response_text}")
            
            # GOOD: Async database write
            await database_async.save_analysis(single_request.id, analysis)
            
            return {
                "request_id": single_request.id,
                "analysis": analysis,
                "status_code": response.status
            }
    
    async def post_async(self, shared, prep_res, exec_res_list):
        # Clean up resources
        if self.session:
            await self.session.close()
        
        shared["api_results"] = exec_res_list
        return "api_processing_complete"

class GoodFileProcessor(AsyncParallelBatchNode):
    """Async file processing"""
    
    async def prep_async(self, shared):
        return shared["file_paths"]
    
    async def exec_async(self, file_path):
        # GOOD: Async file I/O
        import aiofiles
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
        
        # GOOD: Async LLM processing
        summary = await call_llm_async(f"Summarize: {content}")
        
        return {
            "file_path": file_path,
            "summary": summary,
            "file_size": len(content)
        }
    
    async def post_async(self, shared, prep_res, exec_res_list):
        shared["file_summaries"] = exec_res_list
        
        total_size = sum(result["file_size"] for result in exec_res_list)
        shared["processing_stats"] = {
            "total_files": len(exec_res_list),
            "total_size": total_size
        }
        
        return "file_processing_complete"

# For mixed I/O and CPU operations
class OptimizedProcessor(AsyncNode):
    """Single async node for mixed operations"""
    
    async def prep_async(self, shared):
        # GOOD: Async data loading
        data = await load_data_async(shared["data_source"])
        return data
    
    async def exec_async(self, data):
        # GOOD: Mix async I/O with sync CPU operations
        processed_data = []
        
        # CPU-intensive operation (sync)
        analyzed_data = self.cpu_intensive_analysis(data)
        
        # I/O operation (async)
        enriched_data = await self.enrich_with_external_api(analyzed_data)
        
        return enriched_data
    
    async def post_async(self, shared, prep_res, exec_res):
        # GOOD: Async result storage
        await save_results_async(exec_res)
        shared["processed_data"] = exec_res
        return "processing_complete"
```

**Detection**:
- requests.get(), urllib calls in Node.exec() methods
- Synchronous file I/O (open(), read(), write()) in nodes
- Synchronous database calls in nodes processing multiple items
- Loop with blocking operations in regular Node classes
- Long-running exec() methods with I/O operations

**Prevention**:
- Use AsyncNode for any I/O operations
- Use AsyncParallelBatchNode for processing collections with I/O
- Implement proper async session management
- Use rate limiting with semaphores for external API calls

---

### 11. Inefficient LLM Usage Patterns 🟡

**Name**: Inefficient LLM Usage Patterns  
**Description**: Poor LLM call patterns that waste tokens, time, and money.

**Example (ANTIPATTERN):**
```python
class BadLLMUsage(Node):
    def exec(self, documents):
        # BAD: Repeated context in every call
        results = []
        long_system_prompt = """
        You are an expert document analyzer with 20 years of experience...
        [500 lines of repeated context]
        Please follow these detailed guidelines...
        [Another 200 lines repeated in every call]
        """
        
        for doc in documents:
            # BAD: Sending entire document for simple classification
            full_prompt = f"""
            {long_system_prompt}
            
            Document content:
            {doc.full_content}  # 50,000 tokens
            
            Question: What is the document type?
            """
            
            # BAD: Expensive call for simple task
            doc_type = call_llm(full_prompt, model="gpt-4-32k")  # Overkill
            
            # BAD: Another expensive call with repeated context
            sentiment_prompt = f"""
            {long_system_prompt}
            
            Document content:
            {doc.full_content}  # Same 50,000 tokens again
            
            Question: What is the sentiment?
            """
            
            sentiment = call_llm(sentiment_prompt, model="gpt-4-32k")  # More overkill
            
            # BAD: Third call with same massive context
            summary_prompt = f"""
            {long_system_prompt}
            
            Document content:
            {doc.full_content}  # Same content third time
            
            Question: Provide a summary.
            """
            
            summary = call_llm(summary_prompt, model="gpt-4-32k")  # Even more overkill
            
            results.append({
                "type": doc_type,
                "sentiment": sentiment,
                "summary": summary
            })
        
        return results  # Extremely expensive and slow
```

**Why It's Problematic:**
- **High Token Costs**: Repeated context multiplies costs exponentially
- **Slow Performance**: Large prompts take longer to process
- **Model Overkill**: Using expensive models for simple tasks
- **Poor Token Efficiency**: Sending same content multiple times
- **Rate Limit Issues**: Large prompts hit rate limits faster
- **Memory Waste**: Inefficient prompt construction

**Correction (GOOD):**
```python
class EfficientDocumentAnalysis(AsyncParallelBatchNode):
    """Efficient LLM usage with optimized prompts"""
    
    async def prep_async(self, shared):
        return shared["documents"]
    
    async def exec_async(self, single_document):
        # GOOD: Single call for multiple tasks
        optimized_prompt = self.create_efficient_prompt(single_document)
        
        # GOOD: Use appropriate model for task complexity
        if len(optimized_prompt) < 1000:
            model = "gpt-3.5-turbo"  # Cheaper for simple tasks
        else:
            model = "gpt-4"  # Only when needed
        
        result = await call_llm_async(optimized_prompt, model=model)
        
        return self.parse_multi_task_result(result, single_document.id)
    
    def create_efficient_prompt(self, document):
        """Create optimized prompt with minimal context"""
        
        # GOOD: Extract only relevant content
        if len(document.content) > 2000:
            # Use first/last paragraphs + middle sample
            content = self.extract_representative_content(document.content)
        else:
            content = document.content
        
        # GOOD: Concise system prompt
        return f"""
        Analyze this document and provide:
        1. Type: (legal/financial/technical/other)
        2. Sentiment: (positive/negative/neutral)
        3. Summary: (2-3 sentences)
        
        Document:
        {content}
        
        Response format:
        Type: [type]
        Sentiment: [sentiment]
        Summary: [summary]
        """
    
    def extract_representative_content(self, full_content):
        """Extract key portions instead of sending everything"""
        paragraphs = full_content.split('\n\n')
        
        if len(paragraphs) <= 5:
            return full_content
        
        # First 2, middle 1, last 2 paragraphs
        representative = (
            '\n\n'.join(paragraphs[:2]) + 
            '\n\n[...content abbreviated...]\n\n' +
            paragraphs[len(paragraphs)//2] +
            '\n\n[...content abbreviated...]\n\n' +
            '\n\n'.join(paragraphs[-2:])
        )
        
        return representative
    
    def parse_multi_task_result(self, llm_result, doc_id):
        """Parse structured response"""
        lines = llm_result.strip().split('\n')
        result = {"doc_id": doc_id}
        
        for line in lines:
            if line.startswith("Type:"):
                result["type"] = line.replace("Type:", "").strip()
            elif line.startswith("Sentiment:"):
                result["sentiment"] = line.replace("Sentiment:", "").strip()
            elif line.startswith("Summary:"):
                result["summary"] = line.replace("Summary:", "").strip()
        
        return result
    
    async def post_async(self, shared, prep_res, exec_res_list):
        shared["document_analyses"] = exec_res_list
        
        # Track usage for optimization
        shared["llm_usage_stats"] = {
            "total_calls": len(exec_res_list),
            "estimated_tokens": len(exec_res_list) * 800,  # Estimated per call
            "model_used": "mixed"
        }
        
        return "analysis_complete"

# For very large documents, use a different strategy
class LargeDocumentProcessor(AsyncNode):
    """Handle large documents with chunking and summarization"""
    
    async def exec_async(self, large_document):
        # GOOD: Chunking strategy for large documents
        chunks = self.smart_chunk_document(large_document.content)
        
        # GOOD: Process chunks in parallel with smaller model
        chunk_summaries = []
        semaphore = asyncio.Semaphore(5)  # Rate limiting
        
        async def process_chunk(chunk):
            async with semaphore:
                return await call_llm_async(
                    f"Summarize key points from this section:\n{chunk}",
                    model="gpt-3.5-turbo"  # Cheaper for simple summarization
                )
        
        chunk_summaries = await asyncio.gather(*[
            process_chunk(chunk) for chunk in chunks
        ])
        
        # GOOD: Final synthesis with larger model only when needed
        combined_summary = "\n".join(chunk_summaries)
        
        if len(combined_summary) < 3000:
            final_analysis = await call_llm_async(
                f"""
                Based on these section summaries, provide:
                1. Overall document type
                2. Main themes
                3. Executive summary
                
                Section summaries:
                {combined_summary}
                """,
                model="gpt-4"  # Use powerful model for synthesis
            )
        else:
            # Document still too large, use cheaper model
            final_analysis = await call_llm_async(
                f"Provide brief analysis of: {combined_summary[:2000]}...",
                model="gpt-3.5-turbo"
            )
        
        return {
            "document_id": large_document.id,
            "chunk_count": len(chunks),
            "analysis": final_analysis
        }
    
    def smart_chunk_document(self, content):
        """Intelligent chunking that preserves context"""
        # Chunk by paragraphs/sections, not arbitrary character limits
        sections = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for section in sections:
            if len(current_chunk + section) < 1500:  # Optimal chunk size
                current_chunk += section + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = section + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

# Caching expensive LLM calls
class CachedLLMProcessor(Node):
    """Cache results for repeated similar calls"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}
    
    def exec(self, data):
        # GOOD: Cache expensive operations
        cache_key = self.generate_cache_key(data)
        
        if cache_key in self.cache and self.cur_retry == 0:
            return self.cache[cache_key]
        
        result = call_llm(self.create_prompt(data))
        
        # Cache successful results
        if self.cur_retry == 0:  # Only cache on first attempt
            self.cache[cache_key] = result
        
        return result
```

**Detection**:
- Multiple LLM calls with repeated context
- Sending full documents for simple classification tasks
- Using expensive models for simple tasks
- No caching of similar requests
- Large prompts (>4000 tokens) for simple questions

**Prevention**:
- Combine multiple simple tasks in single LLM call
- Use prompt engineering to minimize token usage
- Choose appropriate model size for task complexity
- Implement caching for repeated similar calls
- Use chunking strategies for large documents

---

## Testing and Development Antipatterns

### 12. Untestable Node Design 🟠

**Name**: Untestable Node Design  
**Description**: Designing nodes that are impossible or extremely difficult to test in isolation.

**Example (ANTIPATTERN):**
```python
class BadUserProcessor(Node):
    def __init__(self):
        super().__init__()
        # BAD: Hard-coded external dependencies
        self.api_client = RealAPIClient(api_key="real-key")
        self.database = RealDatabase(connection_string="real-db")
        self.email_service = RealEmailService()
    
    def exec(self, user_data):
        # BAD: Direct external service calls - can't mock
        current_time = datetime.now()  # BAD: Non-deterministic
        
        # BAD: Multiple responsibilities mixed together
        validation_result = self.api_client.validate_user(user_data)
        
        if validation_result.valid:
            # BAD: More external calls
            enriched_data = self.api_client.enrich_user_data(user_data)
            
            # BAD: Database access in exec
            existing_user = self.database.find_user(user_data["id"])
            
            if existing_user:
                # BAD: Complex logic mixed with external calls
                if existing_user.last_login < current_time - timedelta(days=30):
                    # BAD: Email sending in compute logic
                    self.email_service.send_reactivation_email(user_data["email"])
                    status = "reactivated"
                else:
                    status = "updated"
            else:
                status = "new"
            
            # BAD: More database access
            self.database.save_user(enriched_data, status)
            
            return {
                "status": status,
                "enriched_data": enriched_data,
                "processed_at": current_time.isoformat()
            }
        else:
            # BAD: Exception for business logic
            raise ValidationException("User validation failed")

# Impossible to test in isolation
def test_bad_user_processor():
    processor = BadUserProcessor()
    
    # BAD: Test requires real external services
    test_data = {"id": "123", "name": "Test User"}
    
    # This test will fail if:
    # - API is down
    # - Database is unavailable  
    # - Network is slow
    # - Email service is down
    result = processor.exec(test_data)  # Unreliable test
```

**Why It's Problematic:**
- **Cannot Mock Dependencies**: Hard-coded external services
- **Non-Deterministic Tests**: Time-dependent logic makes tests flaky
- **Slow Tests**: Real external service calls take time
- **Unreliable Tests**: Tests fail due to external service issues
- **Hard to Test Edge Cases**: Cannot simulate external service failures
- **Complex Test Setup**: Requires full infrastructure to run tests

**Correction (GOOD):**
```python
class GoodUserProcessor(Node):
    """Testable node with dependency injection"""
    
    def __init__(self, api_client=None, database=None, email_service=None, 
                 time_provider=None, **kwargs):
        super().__init__(**kwargs)
        # GOOD: Dependency injection allows mocking
        self.api_client = api_client or RealAPIClient()
        self.database = database or RealDatabase()
        self.email_service = email_service or RealEmailService()
        self.time_provider = time_provider or datetime.now
    
    def prep(self, shared):
        # GOOD: Clear data preparation
        return {
            "user_data": shared["user_data"],
            "current_time": self.time_provider()
        }
    
    def exec(self, prep_result):
        # GOOD: Pure computation with injected dependencies
        user_data = prep_result["user_data"]
        current_time = prep_result["current_time"]
        
        # Single responsibility: user processing logic
        validation_result = self.api_client.validate_user(user_data)
        
        if not validation_result.valid:
            return {"status": "invalid", "reason": validation_result.reason}
        
        enriched_data = self.api_client.enrich_user_data(user_data)
        existing_user = self.database.find_user(user_data["id"])
        
        if existing_user:
            status = self._determine_user_status(existing_user, current_time)
            if status == "reactivated":
                self.email_service.send_reactivation_email(user_data["email"])
        else:
            status = "new"
        
        return {
            "status": status,
            "enriched_data": enriched_data,
            "existing_user": existing_user,
            "processed_at": current_time.isoformat()
        }
    
    def _determine_user_status(self, existing_user, current_time):
        """GOOD: Pure function for business logic - easily testable"""
        if existing_user.last_login < current_time - timedelta(days=30):
            return "reactivated"
        else:
            return "updated"
    
    def post(self, shared, prep_res, exec_res):
        # GOOD: Clear side effects in post
        if exec_res["status"] != "invalid":
            self.database.save_user(
                exec_res["enriched_data"], 
                exec_res["status"]
            )
        
        shared["user_processing_result"] = exec_res
        return exec_res["status"]

# GOOD: Comprehensive, fast, reliable tests
def test_user_processor_new_user():
    # GOOD: Mock external dependencies
    mock_api = Mock()
    mock_api.validate_user.return_value = Mock(valid=True)
    mock_api.enrich_user_data.return_value = {"id": "123", "name": "Test", "enriched": True}
    
    mock_database = Mock()
    mock_database.find_user.return_value = None
    
    mock_email = Mock()
    
    # GOOD: Deterministic time for testing
    test_time = datetime(2023, 1, 1, 12, 0, 0)
    mock_time_provider = lambda: test_time
    
    processor = GoodUserProcessor(
        api_client=mock_api,
        database=mock_database,
        email_service=mock_email,
        time_provider=mock_time_provider
    )
    
    # GOOD: Test only the business logic
    prep_result = {
        "user_data": {"id": "123", "name": "Test User"},
        "current_time": test_time
    }
    
    result = processor.exec(prep_result)
    
    # GOOD: Predictable, fast, reliable assertions
    assert result["status"] == "new"
    assert result["enriched_data"]["enriched"] == True
    assert result["processed_at"] == "2023-01-01T12:00:00"
    
    # GOOD: Verify interactions with mocks
    mock_api.validate_user.assert_called_once()
    mock_email.send_reactivation_email.assert_not_called()

def test_user_processor_reactivation():
    # GOOD: Test edge case with mock data
    mock_api = Mock()
    mock_api.validate_user.return_value = Mock(valid=True)
    mock_api.enrich_user_data.return_value = {"id": "123", "enriched": True}
    
    # GOOD: Create old user for reactivation scenario
    old_user = Mock()
    old_user.last_login = datetime(2022, 1, 1)  # Very old login
    
    mock_database = Mock()
    mock_database.find_user.return_value = old_user
    
    mock_email = Mock()
    
    test_time = datetime(2023, 1, 1)
    processor = GoodUserProcessor(
        api_client=mock_api,
        database=mock_database,
        email_service=mock_email,
        time_provider=lambda: test_time
    )
    
    prep_result = {
        "user_data": {"id": "123", "email": "test@example.com"},
        "current_time": test_time
    }
    
    result = processor.exec(prep_result)
    
    assert result["status"] == "reactivated"
    mock_email.send_reactivation_email.assert_called_once_with("test@example.com")

def test_user_status_determination():
    """GOOD: Test pure business logic separately"""
    processor = GoodUserProcessor()
    
    recent_user = Mock()
    recent_user.last_login = datetime(2023, 1, 15)
    
    old_user = Mock() 
    old_user.last_login = datetime(2022, 1, 1)
    
    current_time = datetime(2023, 1, 20)
    
    assert processor._determine_user_status(recent_user, current_time) == "updated"
    assert processor._determine_user_status(old_user, current_time) == "reactivated"
```

**Detection**:
- Nodes with hard-coded external service instantiation
- exec() methods that use datetime.now() or other non-deterministic functions
- Nodes that cannot be tested without external services
- Tests that require database/network connections to pass
- exec() methods that are longer than 30 lines and mix concerns

**Prevention**:
- Use dependency injection for external services
- Make time and randomness injectable for deterministic testing
- Separate pure business logic into testable helper methods
- Keep exec() methods focused on single responsibility
- Mock all external dependencies in tests

---

## Detection and Prevention Tools

### Automated Detection Patterns

Here are patterns and tools to automatically detect these antipatterns:

#### Static Analysis Rules

```python
# Example antipattern detection rules
ANTIPATTERN_RULES = {
    "monolithic_node": {
        "indicators": [
            "exec method > 20 lines",
            "multiple LLM calls in single exec",
            "multiple verb names in class name"
        ],
        "regex_patterns": [
            r"def exec.*\n(?:.*\n){20,}",  # Long exec methods
            r"call_llm.*call_llm",  # Multiple LLM calls
        ]
    },
    
    "shared_store_in_exec": {
        "indicators": ["self.shared[", "self.shared access in exec"],
        "regex_patterns": [
            r"def exec.*self\.shared\[",
            r"def exec.*self\.shared\."
        ],
        "severity": "critical"
    },
    
    "business_logic_in_utils": {
        "indicators": ["if.*else in utils", "call_llm in utils"],
        "file_patterns": ["utils/*.py"],
        "regex_patterns": [
            r"def .*\(.*\):.*if.*else.*call_llm",
        ]
    }
}
```

#### Pre-commit Hooks

```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pocketflow-antipatterns
        name: PocketFlow Antipattern Detection
        entry: python scripts/detect_antipatterns.py
        language: system
        files: \.(py)$
```

#### Integration with CI/CD

```yaml
# .github/workflows/quality.yml
name: Code Quality
on: [push, pull_request]

jobs:
  antipattern-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check for Antipatterns
        run: python scripts/validate-antipatterns.py --strict
      - name: Generate Quality Report
        run: python scripts/quality-report.py
```

### Prevention Strategies

#### Design-Time Prevention

1. **Flow Diagram First**: Always create visual flow diagrams before coding
2. **Pre-flight Checklist**: Use the 9-point checklist from best practices
3. **Code Review Guidelines**: Include antipattern checks in review templates
4. **Template Generation**: Generate code with inline warnings about common mistakes

#### Development-Time Prevention

1. **IDE Plugins**: Create IDE extensions that highlight potential antipatterns
2. **Type Hints**: Use type hints to enforce proper node interfaces
3. **Testing Templates**: Provide testing templates that encourage good practices
4. **Documentation Standards**: Require design docs that prevent architectural antipatterns

#### Runtime Prevention

1. **Monitoring**: Track performance patterns that indicate inefficient implementations
2. **Alerting**: Set up alerts for common failure patterns
3. **Metrics Collection**: Gather data on LLM usage, error rates, and performance
4. **Automatic Optimization**: Suggest optimizations based on runtime behavior

---

## Conclusion

This comprehensive catalog of PocketFlow antipatterns provides a foundation for building higher-quality LLM applications. By understanding these common mistakes, their underlying causes, and proven solutions, developers can:

1. **Avoid Common Pitfalls**: Recognize and prevent recurring implementation mistakes
2. **Improve Code Quality**: Build more maintainable, testable, and scalable systems
3. **Optimize Performance**: Create more efficient LLM applications
4. **Enhance Reliability**: Implement robust error handling and recovery strategies

Remember the core framework principle: **Template generators should create meaningful placeholder code that shows intent and guides implementation, not working implementations.** These antipatterns represent mistakes in end-user applications, not in the framework templates themselves.

For ongoing improvements to this guide, contribute examples from real-world projects and help expand the detection and prevention tooling.

### Quick Reference

**🔴 Critical Antipatterns** (Fix Immediately):
- Monolithic Node Syndrome
- Shared Store Access in exec()

**🟡 High Priority** (Address in Next Sprint):
- Hidden Flow Control  
- Business Logic in Utilities
- Exception Handling for Flow Control
- Inefficient LLM Usage Patterns

**🟠 Medium Priority** (Include in Technical Debt):
- Lifecycle Method Confusion
- Synchronous Collection Processing
- Missing Error Recovery Paths

**🟢 Low Priority** (Address During Refactoring):
- Trivial Utility Overuse
- Blocking I/O in Regular Nodes
- Untestable Node Design

Use this prioritization to focus improvement efforts where they will have the greatest impact on system quality and maintainability.