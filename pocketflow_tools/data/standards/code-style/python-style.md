# Python Style Guide

> Version: 1.0.0
> Last Updated: 2025-01-11

## Python-Specific Standards

This file contains detailed Python formatting and style conventions that extend the base code-style.md rules.

## Import Organization

### Import Order
1. Standard library imports
2. Core framework imports (FastAPI, PocketFlow)
3. Third-party package imports
4. Local application imports

### Import Formatting
```python
# Standard library
import os
import sys
from typing import Optional, List, Dict

# Core frameworks
from fastapi import FastAPI, HTTPException
from pocketflow import Flow, Node

# Third-party
import httpx
from pydantic import BaseModel

# Local application
from .schemas import UserRequest
from .utils import call_llm
```

## Type Hints

### Required Usage
- **All function parameters** must have type hints
- **All function returns** must specify return type
- **Class attributes** should use type annotations

### Type Hint Examples
```python
def process_data(items: List[str], config: Dict[str, Any]) -> Optional[Result]:
    """Process data with given configuration."""
    pass

class UserProfile:
    name: str
    age: int
    preferences: Dict[str, Any]
    created_at: datetime
```

### Modern Python Types (3.10+)
```python
# Union types
def fetch(id: str | int) -> User | None:
    pass

# Type aliases
UserId = str | int
ResponseData = Dict[str, List[User]]
```

## Docstrings

### Function Docstrings
```python
def calculate_metrics(data: pd.DataFrame, threshold: float = 0.5) -> Dict[str, float]:
    """Calculate performance metrics from data.
    
    Args:
        data: Input dataframe with prediction columns
        threshold: Classification threshold (default: 0.5)
    
    Returns:
        Dictionary containing precision, recall, and F1 scores
        
    Raises:
        ValueError: If data is empty or missing required columns
    """
    pass
```

### Class Docstrings
```python
class DataProcessor:
    """Handles data preprocessing and transformation.
    
    This class provides methods for cleaning, normalizing,
    and transforming raw data into model-ready format.
    
    Attributes:
        config: Processing configuration dictionary
        logger: Structured logger instance
    """
```

## Error Handling

### Exception Patterns
```python
# Specific exceptions
try:
    result = process_data(input_data)
except ValueError as e:
    logger.error("Invalid data format", error=str(e))
    raise
except KeyError as e:
    logger.error("Missing required field", field=str(e))
    return default_value

# Never use bare except
# Bad
except:
    pass

# Good
except Exception as e:
    logger.exception("Unexpected error occurred")
    raise
```

### Custom Exceptions
```python
class DataValidationError(Exception):
    """Raised when input data fails validation."""
    def __init__(self, field: str, value: Any, message: str):
        self.field = field
        self.value = value
        super().__init__(f"Validation failed for {field}: {message}")
```

## Data Classes and Pydantic

### Pydantic Models
```python
from pydantic import BaseModel, Field, validator

class UserRequest(BaseModel):
    """User creation request model."""
    
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=120)
    
    @validator('email')
    def validate_email(cls, v):
        if not v.lower().endswith('.com'):
            raise ValueError('Only .com emails allowed')
        return v.lower()
```

### Dataclasses
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ProcessingConfig:
    """Configuration for data processing."""
    
    batch_size: int = 32
    max_retries: int = 3
    timeout: float = 30.0
    features: List[str] = field(default_factory=list)
```

## Async/Await

### Async Function Patterns
```python
async def fetch_data(url: str) -> Dict[str, Any]:
    """Fetch data from external API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Parallel async operations
async def fetch_multiple(urls: List[str]) -> List[Dict]:
    """Fetch data from multiple URLs concurrently."""
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle partial failures
    valid_results = []
    for result in results:
        if isinstance(result, Exception):
            logger.error("Failed to fetch", error=str(result))
        else:
            valid_results.append(result)
    
    return valid_results
```

## Context Managers

### Custom Context Managers
```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """Time a code block execution."""
    start = time.time()
    logger.info(f"Starting {name}")
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"Finished {name}", duration=elapsed)

# Usage
with timer("data_processing"):
    process_large_dataset()
```

## Comprehensions and Generators

### List Comprehensions
```python
# Good: Simple, readable
filtered = [x for x in items if x.is_valid()]

# Avoid: Complex nested comprehensions
# Bad
result = [[func(y) for y in x if condition(y)] for x in data if x]

# Good: Break into steps
valid_data = [x for x in data if x]
result = []
for item in valid_data:
    processed = [func(y) for y in item if condition(y)]
    result.append(processed)
```

### Generator Expressions
```python
# Memory efficient for large datasets
def process_large_file(filepath: str):
    """Process file line by line without loading into memory."""
    with open(filepath) as f:
        valid_lines = (line.strip() for line in f if line.strip())
        for line in valid_lines:
            yield process_line(line)
```

## Constants and Configuration

### Module-Level Constants
```python
# Place after imports, before classes/functions
DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3
VALID_STATUSES = frozenset(['active', 'pending', 'completed'])

# Environment variables
API_KEY = os.getenv('API_KEY', '')
BASE_URL = os.getenv('BASE_URL', 'https://api.example.com')
```

## Python-Specific Best Practices

### Pathlib Usage
```python
from pathlib import Path

# Good: Use pathlib for file operations
config_path = Path(__file__).parent / 'config.json'
if config_path.exists():
    config = json.loads(config_path.read_text())

# Avoid: String concatenation for paths
# Bad
config_path = os.path.dirname(__file__) + '/config.json'
```

### F-String Formatting
```python
# Good: F-strings for readability
message = f"User {user.name} (ID: {user.id}) logged in at {timestamp}"

# Good: Multiline f-strings
query = f"""
    SELECT * FROM users
    WHERE created_at > '{start_date}'
    AND status = '{status}'
"""

# Avoid: Old-style formatting
# Bad
message = "User %s (ID: %d)" % (name, user_id)
message = "User {} (ID: {})".format(name, user_id)
```

### Dictionary Operations
```python
# Good: Use .get() with defaults
value = config.get('timeout', 30.0)

# Good: Dictionary comprehensions
filtered = {k: v for k, v in data.items() if v is not None}

# Good: Merge dictionaries (Python 3.9+)
merged = defaults | overrides

# Good: setdefault for initialization
groups = {}
for item in items:
    groups.setdefault(item.category, []).append(item)
```

## Performance Considerations

### Use Built-ins
```python
# Good: Built-in functions are optimized
total = sum(x.value for x in items)
filtered = filter(lambda x: x > 0, numbers)

# Avoid: Manual loops when built-ins exist
# Bad
total = 0
for x in items:
    total += x.value
```

### Lazy Evaluation
```python
# Good: Generator for memory efficiency
def read_large_file(path: Path):
    """Read file lazily, yielding one record at a time."""
    with open(path) as f:
        for line in f:
            yield json.loads(line)

# Use itertools for efficient operations
from itertools import islice, chain

# Process first 100 items
for item in islice(read_large_file(path), 100):
    process(item)
```