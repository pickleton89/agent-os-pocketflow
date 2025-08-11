# Testing Style Guide

> Version: 1.0.0
> Last Updated: 2025-01-11

## Python Testing Standards

This file contains detailed testing conventions for Python projects, focusing on pytest patterns and best practices.

## Test File Organization

### File Structure
```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_main.py            # Test main application entry point
├── unit/                   # Unit tests
│   ├── __init__.py
│   ├── test_nodes.py      # PocketFlow nodes
│   ├── test_flows.py      # PocketFlow flows
│   ├── test_utils.py      # Utility functions
│   └── test_services.py   # Service layer
├── integration/           # Integration tests
│   ├── __init__.py
│   ├── test_api.py       # FastAPI endpoints
│   ├── test_flows.py     # Full flow execution
│   └── test_external.py  # External API integrations
├── fixtures/              # Test data
│   ├── sample_data.json
│   ├── mock_responses.json
│   └── test_documents/
└── performance/           # Performance tests
    ├── __init__.py
    ├── test_load.py
    └── test_benchmarks.py
```

### Naming Conventions
```python
# Test files: test_*.py pattern
test_user_service.py      # Good
user_service_test.py      # Avoid

# Test classes: Test* prefix
class TestUserService:    # Good
class UserServiceTests:   # Avoid

# Test methods: test_* prefix
def test_create_user_success():       # Good
def test_create_user_with_invalid_data():  # Good
def create_user_test():               # Avoid
```

## Fixture Patterns

### Common Fixtures (conftest.py)
```python
# conftest.py
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from pocketflow import SharedStore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import Settings

# Database fixtures
@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(bind=engine)
    
    TestSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine
    )
    
    yield TestSessionLocal
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    """Provide database session for tests."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()

# FastAPI fixtures
@pytest.fixture
def client(db_session):
    """FastAPI test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    """Authentication headers for API tests."""
    return {"Authorization": "Bearer test-token"}

# PocketFlow fixtures
@pytest.fixture
def shared_store():
    """Basic shared store for testing."""
    return SharedStore({
        'test_mode': True,
        'mock_llm': True
    })

@pytest.fixture
def sample_data():
    """Sample test data."""
    return {
        'users': [
            {'id': 1, 'name': 'Test User', 'email': 'test@example.com'},
            {'id': 2, 'name': 'Another User', 'email': 'user@example.com'},
        ],
        'documents': [
            {'id': 1, 'title': 'Test Document', 'content': 'Sample content'},
            {'id': 2, 'title': 'Another Document', 'content': 'More content'},
        ]
    }

# Async fixtures
@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_client(db_session):
    """Async FastAPI test client."""
    from httpx import AsyncClient
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()
```

### Parametrized Fixtures
```python
@pytest.fixture(params=[
    {'batch_size': 5, 'timeout': 30},
    {'batch_size': 10, 'timeout': 60},
    {'batch_size': 20, 'timeout': 120},
])
def processing_config(request):
    """Different processing configurations for testing."""
    return request.param

@pytest.fixture(params=['sqlite', 'postgresql'])
def database_type(request):
    """Test with different database types."""
    return request.param
```

## Unit Testing Patterns

### Service Layer Testing
```python
# test_user_service.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.schemas.requests import UserCreate, UserUpdate
from app.models import User

class TestUserService:
    """Test suite for UserService."""
    
    @pytest.fixture
    def user_service(self):
        """Create UserService instance."""
        return UserService()
    
    @pytest.fixture
    def mock_user(self):
        """Mock user object."""
        return User(
            id=1,
            email="test@example.com",
            username="testuser",
            full_name="Test User"
        )
    
    def test_create_user_success(self, user_service, db_session, mock_user):
        """Test successful user creation."""
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            full_name="Test User"
        )
        
        with patch.object(db_session, 'add') as mock_add, \
             patch.object(db_session, 'commit') as mock_commit, \
             patch.object(db_session, 'refresh') as mock_refresh:
            
            result = user_service.create_user(db_session, user_data)
            
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_refresh.assert_called_once()
    
    def test_create_user_duplicate_email(self, user_service, db_session):
        """Test user creation with duplicate email."""
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            full_name="Test User"
        )
        
        # Mock database integrity error
        from sqlalchemy.exc import IntegrityError
        db_session.commit.side_effect = IntegrityError("", "", "")
        
        with pytest.raises(ValueError, match="Email already exists"):
            user_service.create_user(db_session, user_data)
    
    @pytest.mark.asyncio
    async def test_async_user_creation(self, user_service):
        """Test async user creation."""
        user_data = UserCreate(
            email="async@example.com",
            username="asyncuser",
            full_name="Async User"
        )
        
        with patch.object(user_service, 'create_user_async') as mock_create:
            mock_create.return_value = AsyncMock(return_value={"id": 1})
            
            result = await user_service.create_user_async(user_data)
            
            assert result["id"] == 1
            mock_create.assert_called_once_with(user_data)
```

### PocketFlow Node Testing
```python
# test_nodes.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from pocketflow import SharedStore

from app.nodes import DataProcessingNode, LLMProcessingNode

class TestDataProcessingNode:
    """Test suite for DataProcessingNode."""
    
    @pytest.fixture
    def node(self):
        """Create node instance."""
        return DataProcessingNode()
    
    @pytest.fixture
    def populated_store(self):
        """Shared store with test data."""
        return SharedStore({
            'input_data': ['item1', 'item2', 'item3'],
            'processing_config': {
                'batch_size': 2,
                'timeout': 30
            }
        })
    
    def test_prep_success(self, node, populated_store):
        """Test successful preparation."""
        result = node.prep(populated_store)
        
        assert result is None
        assert 'processing_started' in populated_store
        assert populated_store['processing_started'] is True
    
    def test_prep_missing_data(self, node):
        """Test preparation with missing input data."""
        empty_store = SharedStore({})
        
        result = node.prep(empty_store)
        
        assert result == "error"
    
    @patch.object(DataProcessingNode, 'process_data')
    def test_exec_success(self, mock_process, node, populated_store):
        """Test successful execution."""
        mock_process.return_value = ['processed1', 'processed2']
        
        result = node.exec(populated_store)
        
        assert result is None
        assert 'processed_results' in populated_store
        assert len(populated_store['processed_results']) == 2
        mock_process.assert_called_once()
    
    @patch.object(DataProcessingNode, 'process_data')
    def test_exec_exception(self, mock_process, node, populated_store):
        """Test execution with exception."""
        mock_process.side_effect = Exception("Processing failed")
        
        result = node.exec(populated_store)
        
        assert result == "error"
        assert 'error_details' in populated_store
        assert "Processing failed" in populated_store['error_details']['error']
    
    def test_post_cleanup(self, node, populated_store):
        """Test post-execution cleanup."""
        # Add some temporary data
        populated_store['temp_processing_data'] = "temporary"
        populated_store['processed_results'] = ['result1', 'result2']
        
        result = node.post(populated_store)
        
        assert result is None
        assert 'temp_processing_data' not in populated_store
        assert 'processed_results' in populated_store
```

### LLM Node Testing
```python
class TestLLMProcessingNode:
    """Test suite for LLM processing nodes."""
    
    @pytest.fixture
    def llm_node(self):
        """Create LLM node instance."""
        return LLMProcessingNode()
    
    @pytest.fixture
    def llm_store(self):
        """Shared store with LLM test data."""
        return SharedStore({
            'input_text': "Test input for processing",
            'llm_config': {
                'model': 'gpt-4',
                'temperature': 0.7,
                'max_tokens': 500
            }
        })
    
    @patch('app.utils.call_llm.call_llm')
    def test_llm_processing_success(self, mock_call_llm, llm_node, llm_store):
        """Test successful LLM processing."""
        mock_call_llm.return_value = "Processed response from LLM"
        
        result = llm_node.exec(llm_store)
        
        assert result is None
        assert 'llm_raw_response' in llm_store
        assert llm_store['llm_raw_response'] == "Processed response from LLM"
        
        mock_call_llm.assert_called_once_with(
            prompt=llm_node.build_prompt("Test input for processing"),
            model='gpt-4',
            temperature=0.7,
            max_tokens=500
        )
    
    @patch('app.utils.call_llm.call_llm')
    def test_llm_processing_failure(self, mock_call_llm, llm_node, llm_store):
        """Test LLM processing failure."""
        mock_call_llm.side_effect = Exception("API rate limit exceeded")
        
        result = llm_node.exec(llm_store)
        
        assert result == "retry"
        assert 'llm_error' in llm_store
        assert "API rate limit exceeded" in llm_store['llm_error']
    
    @patch('app.utils.call_llm.call_llm')
    def test_structured_output_parsing(self, mock_call_llm, llm_node, llm_store):
        """Test structured output parsing."""
        from pydantic import BaseModel
        
        class OutputSchema(BaseModel):
            summary: str
            score: float
        
        mock_call_llm.return_value = '{"summary": "Test summary", "score": 0.85}'
        llm_store['output_schema'] = OutputSchema
        
        result = llm_node.exec(llm_store)
        
        assert result is None
        assert 'llm_parsed_response' in llm_store
        parsed = llm_store['llm_parsed_response']
        assert parsed['summary'] == "Test summary"
        assert parsed['score'] == 0.85
```

## Integration Testing

### FastAPI Integration Tests
```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

class TestUserAPI:
    """Integration tests for User API endpoints."""
    
    def test_create_user_endpoint(self, client, auth_headers):
        """Test user creation endpoint."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User"
        }
        
        response = client.post(
            "/api/v1/users/",
            json=user_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data
        assert "created_at" in data
    
    def test_create_user_validation_error(self, client, auth_headers):
        """Test user creation with invalid data."""
        invalid_data = {
            "email": "invalid-email",  # Invalid email format
            "username": "",            # Empty username
        }
        
        response = client.post(
            "/api/v1/users/",
            json=invalid_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        
        # Check specific validation errors
        errors = data["detail"]
        error_fields = [error["loc"][-1] for error in errors]
        assert "email" in error_fields
        assert "username" in error_fields
    
    def test_get_user_not_found(self, client, auth_headers):
        """Test getting non-existent user."""
        response = client.get(
            "/api/v1/users/99999",
            headers=auth_headers
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_list_users_pagination(self, client, auth_headers, sample_data):
        """Test user listing with pagination."""
        # First, create test users
        for user in sample_data['users']:
            client.post(
                "/api/v1/users/",
                json=user,
                headers=auth_headers
            )
        
        # Test pagination
        response = client.get(
            "/api/v1/users/?skip=0&limit=1",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) == 1
        assert data["skip"] == 0
        assert data["limit"] == 1
        assert data["total"] >= 1
```

### Flow Integration Tests
```python
# test_flows.py
import pytest
from pocketflow import SharedStore

from app.flows import DocumentProcessingFlow

class TestDocumentProcessingFlow:
    """Integration tests for complete flow execution."""
    
    @pytest.fixture
    def flow(self):
        """Create flow instance."""
        return DocumentProcessingFlow()
    
    @pytest.fixture
    def flow_input(self):
        """Input data for flow testing."""
        return SharedStore({
            'document_urls': [
                'https://example.com/doc1.pdf',
                'https://example.com/doc2.pdf'
            ],
            'processing_config': {
                'batch_size': 5,
                'llm_model': 'gpt-4',
                'extract_summary': True
            }
        })
    
    @pytest.mark.asyncio
    @patch('app.utils.call_llm.call_llm')
    @patch('app.utils.document_fetcher.fetch_document')
    async def test_complete_flow_success(
        self, 
        mock_fetch, 
        mock_llm, 
        flow, 
        flow_input
    ):
        """Test complete flow execution with mocked dependencies."""
        
        # Mock document fetching
        mock_fetch.side_effect = [
            "Content of document 1",
            "Content of document 2"
        ]
        
        # Mock LLM processing
        mock_llm.return_value = "Summary of processed content"
        
        # Execute flow
        result_store = await flow.run(flow_input)
        
        # Verify results
        assert 'final_results' in result_store
        assert 'processing_stats' in result_store
        assert result_store['processing_stats']['successful'] == 2
        
        # Verify mocks were called
        assert mock_fetch.call_count == 2
        assert mock_llm.called
    
    @pytest.mark.asyncio
    @patch('app.utils.document_fetcher.fetch_document')
    async def test_flow_with_fetch_errors(self, mock_fetch, flow, flow_input):
        """Test flow handling of document fetch errors."""
        
        # Mock partial failures
        mock_fetch.side_effect = [
            "Content of document 1",
            Exception("Failed to fetch document 2")
        ]
        
        result_store = await flow.run(flow_input)
        
        # Should complete with partial results
        assert 'final_results' in result_store
        assert result_store['processing_stats']['failed'] == 1
        assert result_store['processing_stats']['successful'] == 1
    
    @pytest.mark.asyncio
    async def test_flow_validation_errors(self, flow):
        """Test flow with invalid input data."""
        invalid_input = SharedStore({
            'document_urls': [],  # Empty URL list
            'processing_config': {}  # Missing required config
        })
        
        result_store = await flow.run(invalid_input)
        
        # Should fail validation
        assert 'error_details' in result_store
        assert 'validation' in result_store['error_details']['error'].lower()
```

## Async Testing Patterns

### Async Test Setup
```python
import pytest
import asyncio
from unittest.mock import AsyncMock, patch

class TestAsyncOperations:
    """Test suite for async operations."""
    
    @pytest.mark.asyncio
    async def test_async_data_processing(self):
        """Test async data processing function."""
        from app.services import async_process_data
        
        test_data = ['item1', 'item2', 'item3']
        
        result = await async_process_data(test_data)
        
        assert len(result) == 3
        assert all('processed' in item for item in result)
    
    @pytest.mark.asyncio
    @patch('app.external.api_client.fetch_data')
    async def test_async_external_api(self, mock_fetch):
        """Test async external API calls."""
        from app.services import fetch_user_data
        
        # Mock async API response
        mock_fetch.return_value = AsyncMock(
            return_value={"id": 1, "name": "Test User"}
        )
        
        result = await fetch_user_data(user_id=1)
        
        assert result["id"] == 1
        assert result["name"] == "Test User"
        mock_fetch.assert_called_once_with(user_id=1)
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent async operations."""
        from app.services import process_batch_async
        
        items = [f"item_{i}" for i in range(10)]
        
        start_time = asyncio.get_event_loop().time()
        results = await process_batch_async(items)
        end_time = asyncio.get_event_loop().time()
        
        # Should complete faster than sequential processing
        assert len(results) == 10
        assert end_time - start_time < 2.0  # Assuming parallel speedup
```

## Mocking Patterns

### Database Mocking
```python
@pytest.fixture
def mock_db_session():
    """Mock database session."""
    session = Mock()
    
    # Mock query results
    session.query.return_value.filter.return_value.first.return_value = Mock(
        id=1,
        email="test@example.com",
        username="testuser"
    )
    
    session.query.return_value.all.return_value = [
        Mock(id=1, name="User 1"),
        Mock(id=2, name="User 2")
    ]
    
    return session

def test_with_mocked_db(mock_db_session):
    """Test using mocked database session."""
    from app.services import UserService
    
    service = UserService()
    user = service.get_user_by_email(mock_db_session, "test@example.com")
    
    assert user.email == "test@example.com"
    mock_db_session.query.assert_called()
```

### External Service Mocking
```python
@pytest.fixture
def mock_llm_service():
    """Mock LLM service calls."""
    with patch('app.utils.call_llm.call_llm') as mock:
        # Configure different responses for different prompts
        def side_effect(prompt, **kwargs):
            if "summarize" in prompt.lower():
                return "This is a summary of the content."
            elif "analyze" in prompt.lower():
                return "Analysis: The content shows positive sentiment."
            else:
                return "Default LLM response."
        
        mock.side_effect = side_effect
        yield mock

def test_llm_integration(mock_llm_service):
    """Test LLM integration with mocked service."""
    from app.services import process_with_llm
    
    result = process_with_llm("Please summarize this text.")
    
    assert "summary" in result.lower()
    mock_llm_service.assert_called_once()
```

## Performance Testing

### Load Testing
```python
# test_performance.py
import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

class TestPerformance:
    """Performance test suite."""
    
    def test_response_time(self, client):
        """Test API response time."""
        start_time = time.time()
        
        response = client.get("/api/v1/users/")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 0.5  # Should respond within 500ms
    
    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests."""
        def make_request():
            return client.get("/api/v1/users/")
        
        # Make 10 concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [f.result() for f in futures]
        
        # All should succeed
        assert all(r.status_code == 200 for r in responses)
    
    @pytest.mark.asyncio
    async def test_memory_usage(self):
        """Test memory usage during processing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Perform memory-intensive operation
        from app.services import process_large_dataset
        large_data = list(range(10000))
        await process_large_dataset(large_data)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 100 * 1024 * 1024  # Less than 100MB
```

## Test Configuration

### Pytest Configuration (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --strict-config
    --disable-warnings
    --tb=short
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    external: Tests requiring external services
asyncio_mode = auto
```

### Coverage Configuration (.coveragerc)
```ini
[run]
source = app
omit = 
    */tests/*
    */venv/*
    */env/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    @abstract
```

## Test Data Management

### Fixture Files
```python
# fixtures/test_data.py
"""Test data fixtures."""

SAMPLE_USERS = [
    {
        "id": 1,
        "email": "user1@example.com",
        "username": "user1",
        "full_name": "First User",
        "created_at": "2025-01-01T00:00:00Z"
    },
    {
        "id": 2, 
        "email": "user2@example.com",
        "username": "user2",
        "full_name": "Second User",
        "created_at": "2025-01-02T00:00:00Z"
    }
]

SAMPLE_DOCUMENTS = [
    {
        "id": 1,
        "title": "Test Document 1",
        "content": "This is the content of test document 1.",
        "url": "https://example.com/doc1.pdf"
    },
    {
        "id": 2,
        "title": "Test Document 2", 
        "content": "This is the content of test document 2.",
        "url": "https://example.com/doc2.pdf"
    }
]

LLM_MOCK_RESPONSES = {
    "summarize": "This is a test summary.",
    "analyze": "Analysis: Positive sentiment detected.",
    "extract": "Key information extracted successfully."
}
```

### Dynamic Fixtures
```python
@pytest.fixture
def user_factory():
    """Factory for creating test users."""
    def _create_user(**kwargs):
        defaults = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "created_at": datetime.utcnow()
        }
        defaults.update(kwargs)
        return defaults
    
    return _create_user

def test_user_creation(user_factory):
    """Test using user factory."""
    user1 = user_factory(email="user1@test.com")
    user2 = user_factory(username="specialuser")
    
    assert user1["email"] == "user1@test.com"
    assert user2["username"] == "specialuser"
```

## Test Organization Best Practices

### Test Categories
```python
# Use markers to organize tests
@pytest.mark.unit
def test_utility_function():
    """Unit test for utility function."""
    pass

@pytest.mark.integration
def test_api_endpoint():
    """Integration test for API endpoint."""
    pass

@pytest.mark.slow
def test_large_dataset_processing():
    """Slow test for large dataset processing."""
    pass

@pytest.mark.external
def test_third_party_api():
    """Test requiring external service."""
    pass

# Run specific test categories
# pytest -m "unit"
# pytest -m "integration"
# pytest -m "not slow"
```

### Test Documentation
```python
def test_user_registration_flow():
    """Test complete user registration flow.
    
    This test verifies:
    1. User data validation
    2. Email uniqueness check
    3. Password hashing
    4. Database persistence
    5. Welcome email sending
    
    Expected behavior:
    - Valid data creates user successfully
    - Returns 201 status code
    - User receives welcome email
    
    Edge cases tested:
    - Duplicate email addresses
    - Invalid email formats
    - Weak passwords
    """
    # Test implementation here
    pass
```