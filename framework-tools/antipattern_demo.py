#!/usr/bin/env python3
# ruff: noqa: E402, F821
"""
EDUCATIONAL DEMONSTRATION FILE - Contains Intentional Antipatterns

This file demonstrates BAD practices for the PocketFlow antipattern detector.
ALL linting errors in this file are EXPECTED and INTENTIONAL.

Purpose:
- Showcases various PocketFlow antipatterns for educational purposes
- Provides test cases for the antipattern detector tool
- Demonstrates both correct and incorrect patterns side-by-side

Linting Suppressions (ALL INTENTIONAL):
- E402: Module imports not at top (demonstrates bad import practices)
- F821: Undefined names (mock external dependencies for demonstration)

🎯 FRAMEWORK CONTEXT: This is framework repository code that demonstrates antipatterns
for educational purposes. In actual end-user projects, these imports would work:
    from pocketflow import Node, AsyncNode, BatchNode, call_llm

But since this is the FRAMEWORK repository (not a usage repository), we use
mock classes to demonstrate the patterns without requiring PocketFlow installation.

Usage:
    python antipattern_detector.py antipattern_demo.py --format console

Author: Agent OS + PocketFlow Framework
Version: 1.0.0
"""

# 🎯 MOCK IMPORTS FOR FRAMEWORK CONTEXT
# In end-user projects, these would be: from pocketflow import Node, AsyncNode, BatchNode
# But this is the framework repository, so we mock these for demonstration
class Node:
    """Mock Node class for framework demonstration"""
    def __init__(self, **kwargs):
        self.shared = {}  # Mock shared store for demonstration
    
class AsyncNode:
    """Mock AsyncNode class for framework demonstration"""
    pass

class BatchNode:
    """Mock BatchNode class for framework demonstration"""
    pass

class AsyncParallelBatchNode:
    """Mock AsyncParallelBatchNode class for framework demonstration"""
    pass

def call_llm(prompt: str, **kwargs):
    """Mock LLM call for framework demonstration"""
    return f"Mock LLM response for: {prompt[:50]}..."

def call_llm_async(prompt: str, **kwargs):
    """Mock async LLM call for framework demonstration"""
    return f"Mock async LLM response for: {prompt[:50]}..."

# Mock external dependencies
import requests


# ❌ ANTIPATTERN: Monolithic Node Syndrome
class BadProcessDocuments(Node):
    """This node violates single responsibility by doing too many things"""
    
    def exec(self, documents):
        # BAD: Too many responsibilities in one method
        validated_docs = []
        for doc in documents:
            if self.validate_document(doc):
                validated_docs.append(doc)
        
        extracted_texts = []
        for doc in validated_docs:
            text = self.extract_text(doc)
            extracted_texts.append(text)
        
        # BAD: Multiple LLM calls suggest different responsibilities
        entities = []
        for text in extracted_texts:
            entity = call_llm(f"Extract entities: {text}")
            entities.append(entity)
        
        summaries = []
        for entity in entities:
            summary = call_llm(f"Summarize: {entity}")
            summaries.append(summary)
        
        # BAD: Yet another responsibility
        report = self.generate_report(summaries)
        self.send_notifications(report)
        
        return report


# ❌ ANTIPATTERN: Shared Store Access in exec()
class BadSharedStoreNode(Node):
    """This node violates lifecycle by accessing shared store in exec"""
    
    def prep(self, shared):
        return shared["user_id"]
    
    def exec(self, user_id):
        # BAD: Direct shared store access in exec
        user_data = self.shared["users"][user_id]
        preferences = self.shared["user_preferences"][user_id]
        
        # BAD: More shared store access
        if self.shared["is_premium_user"]:
            result = self.premium_processing(user_data, preferences)
        else:
            result = self.standard_processing(user_data, preferences)
        
        # BAD: Writing to shared store from exec
        self.shared["processing_count"] += 1
        
        return result


# ❌ ANTIPATTERN: Lifecycle Method Confusion  
class BadLifecycleNode(Node):
    """This node misuses lifecycle methods"""
    
    def prep(self, shared):
        # BAD: Complex computation in prep
        data = shared["raw_data"]
        processed_data = self.complex_processing(data)
        
        # BAD: LLM call in prep
        analysis_result = call_llm(f"Analyze: {processed_data}")
        return analysis_result
    
    def exec(self, prep_result):
        # BAD: Simple formatting (should be in prep)
        formatted_result = prep_result.upper()
        return formatted_result
    
    def post(self, shared, prep_res, exec_res):
        # BAD: Complex logic in post
        if "error" in exec_res:
            corrected_result = call_llm(f"Fix this error: {exec_res}")
            shared["analysis"] = corrected_result
        else:
            shared["analysis"] = exec_res
        return "complete"


# ❌ ANTIPATTERN: Synchronous Collection Processing
class BadSyncCollectionNode(Node):
    """This regular node processes collections synchronously"""
    
    def exec(self, file_list):
        # BAD: Manual iteration in regular node
        results = []
        for file_path in file_list:
            # BAD: Sequential processing - no parallelization
            content = self.read_file(file_path)
            summary = call_llm(f"Summarize: {content}")
            results.append({"file": file_path, "summary": summary})
        
        return results


# ❌ ANTIPATTERN: Blocking I/O in Regular Node
class BadBlockingIONode(Node):
    """This regular node uses blocking I/O operations"""
    
    def exec(self, urls):
        # BAD: Blocking I/O in regular Node
        results = []
        for url in urls:
            response = requests.get(url, timeout=30)
            analysis = call_llm(f"Analyze: {response.text}")
            results.append(analysis)
        
        return results


# ❌ ANTIPATTERN: Business Logic in Utilities
def bad_process_customer_inquiry(inquiry, customer_data, shared_store):
    """BAD: Complex business logic in utility function"""
    
    # BAD: Business logic for customer classification
    if customer_data["tier"] == "premium":
        priority = "high"
    elif customer_data["complaints"] > 3:
        priority = "urgent"
    elif "cancel" in inquiry.lower() or "refund" in inquiry.lower():
        priority = "retention"
    else:
        priority = "normal"
    
    # BAD: LLM call in utility
    sentiment = call_llm(f"Analyze sentiment: {inquiry}")
    
    # BAD: Complex routing logic
    if sentiment == "angry" and priority != "urgent":
        priority = "escalated"
        # BAD: Side effect in utility
        send_manager_alert(customer_data["id"], inquiry)
    
    # BAD: More business logic
    if priority == "retention":
        response = call_llm(f"Generate retention response for: {inquiry}")
        # BAD: Modifying shared store from utility
        shared_store["retention_cases"].append(customer_data["id"])
    else:
        response = call_llm(f"Generate response: {inquiry}")
    
    return {"response": response, "priority": priority, "sentiment": sentiment}


# ✅ GOOD EXAMPLES - These should not trigger violations

class GoodValidateDocuments(BatchNode):
    """GOOD: Single responsibility - document validation only"""
    
    def prep(self, shared):
        return shared["raw_documents"]
    
    def exec(self, document):
        # Single responsibility: validate one document
        return self.validate_document(document)
    
    def post(self, shared, prep_res, exec_res_list):
        # Simple state update
        valid_docs = [doc for doc, is_valid in zip(prep_res, exec_res_list) if is_valid]
        shared["validated_documents"] = valid_docs
        
        if len(valid_docs) == 0:
            return "no_valid_documents"
        return "validation_complete"


class GoodUserProcessor(Node):
    """GOOD: Proper lifecycle usage with dependency injection"""
    
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


class GoodAsyncCollectionProcessor(AsyncParallelBatchNode):
    """GOOD: Proper async collection processing"""
    
    async def prep_async(self, shared):
        return shared["file_list"]
    
    async def exec_async(self, single_file):
        # GOOD: Processes each file independently and in parallel
        content = await self.read_file_async(single_file)
        summary = await call_llm_async(f"Summarize: {content}")
        
        return {
            "file": single_file,
            "summary": summary
        }
    
    async def post_async(self, shared, prep_res, exec_res_list):
        # GOOD: Results collected after all items processed
        shared["file_summaries"] = exec_res_list
        return "processing_complete"


# GOOD: Simple utility functions - external interfaces only
def get_customer_data(customer_id):
    """GOOD: Simple utility - just data access"""
    return database.get_customer(customer_id)


def send_notification(customer_id, message):
    """GOOD: Simple utility - just external service call"""
    return notification_service.send(customer_id, message)


def save_result(data):
    """GOOD: Simple utility - just data persistence"""
    return database.save(data)


if __name__ == '__main__':
    print("This file contains intentional antipatterns for demonstration purposes.")
    print("Run: python antipattern_detector.py antipattern_demo.py --format console")
    print("Expected violations:")
    print("- Monolithic Node Syndrome: BadProcessDocuments")
    print("- Shared Store Access in exec(): BadSharedStoreNode")
    print("- Lifecycle Method Confusion: BadLifecycleNode") 
    print("- Synchronous Collection Processing: BadSyncCollectionNode")
    print("- Blocking I/O in Regular Node: BadBlockingIONode")
    print("- Business Logic in Utilities: bad_process_customer_inquiry")