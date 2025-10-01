# FastAPI Templates

> Version: 2.0  
> Last Updated: 2025-01-08  
> Purpose: Templates for FastAPI integration with modern Python stack

## Overview

This file contains all FastAPI-specific templates for creating API specifications with Pydantic models, proper error handling, and PocketFlow integration patterns.

## API & Data Models Section Template

### For spec.md API & Data Models Section

```markdown
## API & Data Models

### FastAPI Endpoints

#### [HTTP_METHOD] /[endpoint-path]
- **Purpose:** [ONE_SENTENCE_DESCRIPTION]
- **Authentication:** [REQUIRED/NOT_REQUIRED]
- **Rate Limiting:** [IF_APPLICABLE]

**Request Model:**
```python
class [RequestModelName](BaseModel):
    [field_name]: [Type] = [default_value]  # [description]
    [field_name]: Optional[[Type]] = None   # [description]
    
    class Config:
        example = {
            "[field_name]": "[example_value]",
            "[field_name]": "[example_value]"
        }
```

**Response Model:**
```python
class [ResponseModelName](BaseModel):
    [result_field]: [Type]  # [description]
    [metadata_field]: Dict[str, Any] = {}  # [description]
    [timestamp]: datetime  # [description]
    
    class Config:
        example = {
            "[result_field]": "[example_value]",
            "[metadata_field]": {},
            "[timestamp]": "2025-01-XX"
        }
```

**Error Response Model:**
```python
class [ErrorResponseName](BaseModel):
    error_code: str  # [error_type_description]
    message: str     # [human_readable_message]
    details: Optional[Dict[str, Any]] = None  # [additional_context]
    
    class Config:
        example = {
            "error_code": "VALIDATION_ERROR",
            "message": "Invalid input data",
            "details": {"field": "field_name", "issue": "required"}
        }
```

### Pydantic Schema Design

#### Core Data Models
```python
class [CoreEntityName](BaseModel):
    """[ENTITY_DESCRIPTION]"""
    id: Optional[str] = None  # [id_field_description]
    [business_field]: [Type]  # [field_description]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    @validator('[field_name]')
    def validate_[field_name](cls, v):
        # [validation_logic]
        return v
    
    class Config:
        validate_assignment = True
        extra = "forbid"  # Strict mode - no extra fields allowed
```

#### Input/Output Transformations
```python
class [TransformationModelName](BaseModel):
    """Data transformation between API and internal processing"""
    raw_input: [InputType]
    processed_data: Optional[[ProcessedType]] = None
    validation_status: Literal["pending", "valid", "invalid"] = "pending"
    
    def to_shared_store(self) -> Dict[str, Any]:
        """Convert to SharedStore format for PocketFlow processing"""
        return {
            "input_data": self.raw_input,
            "validation_status": self.validation_status,
            "processed_data": self.processed_data
        }
    
    @classmethod
    def from_shared_store(cls, shared: Dict[str, Any]) -> '[TransformationModelName]':
        """Create from SharedStore data after PocketFlow processing"""
        return cls(
            raw_input=shared["input_data"],
            processed_data=shared.get("processed_data"),
            validation_status=shared.get("validation_status", "pending")
        )
```

### API Status Codes & Error Handling
- **200 OK:** Successful GET/PUT operations
- **201 Created:** Successful POST operations
- **204 No Content:** Successful DELETE operations
- **400 Bad Request:** Invalid request data (Pydantic validation failures)
- **401 Unauthorized:** Authentication required
- **403 Forbidden:** Authorization failed
- **404 Not Found:** Resource not found
- **422 Unprocessable Entity:** Business logic validation failures
- **429 Too Many Requests:** Rate limit exceeded
- **500 Internal Server Error:** Unexpected server errors

### Integration with PocketFlow
```python
@app.post("/[endpoint]", response_model=[ResponseModel])
async def [endpoint_function](request: [RequestModel]):
    # Convert API request to SharedStore format
    shared = SharedStore(request.dict())
    
    # Execute PocketFlow workflow
    flow = [WorkflowName]()
    await flow.run_async(shared)
    
    # Handle flow results
    if "error" in shared:
        raise HTTPException(
            status_code=422,
            detail=[ErrorResponseName](
                error_code=shared["error_code"],
                message=shared["error_message"]
            ).dict()
        )
    
    # Convert SharedStore results back to API response
    return [ResponseModel](**shared["result"])
```

### Data Validation Strategy
- **API Boundary:** Pydantic models validate all incoming/outgoing data
- **Business Logic:** Additional validation in PocketFlow nodes
- **Database Layer:** Final validation before persistence
- **Error Propagation:** Structured error responses with consistent format

### Type Safety Requirements
- All API endpoints must have complete type hints
- All Pydantic models must define explicit field types
- SharedStore keys should use consistent naming conventions
- Optional fields must be clearly marked with Optional[] or default values
```

## API Specification Template

### For api-spec.md File

```markdown
# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/YYYY-MM-DD-spec-name/spec.md

> Created: [CURRENT_DATE]
> Version: 1.0.0

## FastAPI Endpoints

### [HTTP_METHOD] /[endpoint-path]

**Purpose:** [ONE_SENTENCE_DESCRIPTION]
**Authentication:** [Required|Not Required]
**Rate Limit:** [X requests per minute|None]

#### Request Specification
```python
@app.[method]("/[endpoint-path]", 
             response_model=[ResponseModel],
             status_code=[STATUS_CODE],
             tags=["[tag_name]"])
async def [function_name](
    request: [RequestModel],
    [dependency]: [DependencyType] = Depends([dependency_function])
) -> [ResponseModel]:
```

**Request Model:**
```python
class [RequestModelName](BaseModel):
    [field_name]: [Type] = Field(..., description="[field_description]")
    [optional_field]: Optional[[Type]] = Field(None, description="[field_description]")
    
    @validator('[field_name]')
    def validate_[field_name](cls, v):
        # [validation_logic]
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "[field_name]": "[example_value]"
            }
        }
```

**Response Model:**
```python
class [ResponseModelName](BaseModel):
    [result_field]: [Type] = Field(..., description="[field_description]")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
```

#### PocketFlow Integration
```python
async def [function_name](request: [RequestModel]) -> [ResponseModel]:
    # Initialize SharedStore with request data
    shared = SharedStore({
        "request_data": request.dict(),
        "timestamp": datetime.utcnow(),
        "user_context": {}  # Add auth context if needed
    })
    
    # Execute PocketFlow workflow
    flow = [WorkflowName]()
    try:
        await flow.run_async(shared)
    except Exception as e:
        logger.error(f"Flow execution failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal processing error"
        )
    
    # Check for processing errors
    if "error" in shared:
        raise HTTPException(
            status_code=422,
            detail={
                "error_code": shared.get("error_code", "PROCESSING_ERROR"),
                "message": shared.get("error_message", "Processing failed"),
                "details": shared.get("error_details")
            }
        )
    
    # Extract and return results
    if "result" not in shared:
        raise HTTPException(
            status_code=500,
            detail="Processing completed but no result generated"
        )
    
    return [ResponseModel](**shared["result"])
```

#### Status Codes
- **[SUCCESS_CODE]:** [SUCCESS_DESCRIPTION]
- **400 Bad Request:** Invalid request data (Pydantic validation failure)
- **401 Unauthorized:** Authentication required
- **403 Forbidden:** Insufficient permissions
- **422 Unprocessable Entity:** Business logic validation failure
- **429 Too Many Requests:** Rate limit exceeded
- **500 Internal Server Error:** Unexpected processing error

#### Error Response Format
```python
{
    "error_code": "VALIDATION_ERROR",
    "message": "Invalid input data provided",
    "details": {
        "field": "field_name",
        "issue": "Field is required"
    },
    "timestamp": "2025-01-XX"
}
```

## Middleware & Configuration

### Application Setup
```python
# main.py - Application setup
from fastapi import FastAPI
from [feature_name].router import router as [feature_name]_router

app = FastAPI(title="[API_TITLE]", version="1.0.0")
app.include_router([feature_name]_router, prefix="/[prefix]", tags=["[feature_name]"])
```

### Middleware Requirements
- **CORS:** [IF_APPLICABLE]
- **Authentication:** [AUTH_METHOD]
- **Rate Limiting:** [IF_APPLICABLE]
- **Request Logging:** [LOGGING_STRATEGY]

### Error Response Standardization
```python
class StandardErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```
```

## Technical Specification Templates

### For technical-spec.md Pydantic Section

```markdown
## Pydantic Schema Specifications

### Request/Response Models
```python
# API Models (schemas/requests.py)
class [FeatureName]Request(BaseModel):
    [field_name]: [Type]
    [optional_field]: Optional[[Type]] = None
    
    @validator('[field_name]')
    def [validation_method](cls, v):
        # Custom validation logic
        return v
    
    class Config:
        example = {"[field_name]": "[example_value]"}

# Response Models (schemas/responses.py)
class [FeatureName]Response(BaseModel):
    result: [ResultType]
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### SharedStore Integration Models
```python
# Internal processing models
class [ProcessingModel](BaseModel):
    """Model for SharedStore data transformations"""
    
    def to_shared_store(self) -> Dict[str, Any]:
        """Convert to SharedStore format"""
        return self.dict()
    
    @classmethod
    def from_shared_store(cls, data: Dict[str, Any]) -> '[ProcessingModel]':
        """Create from SharedStore data"""
        return cls(**data)
```

### Validation Rules
- [VALIDATION_RULE_1]
- [VALIDATION_RULE_2]
```

### For technical-spec.md FastAPI Section

```markdown
## FastAPI Integration

### Route Organization
```python
# main.py - Application setup
from fastapi import FastAPI
from [feature_name].router import router as [feature_name]_router

app = FastAPI(title="[API_TITLE]", version="1.0.0")
app.include_router([feature_name]_router, prefix="/[prefix]", tags=["[feature_name]"])
```

### Middleware Requirements
- **CORS:** [IF_APPLICABLE]
- **Authentication:** [AUTH_METHOD]
- **Rate Limiting:** [IF_APPLICABLE]
- **Request Logging:** [LOGGING_STRATEGY]

### Error Response Standardization
```python
class StandardErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```
```

## Project Structure Template

### Standard FastAPI + PocketFlow Structure

```
project/
├── main.py           # FastAPI app entry point
├── nodes.py          # PocketFlow nodes
├── flow.py           # PocketFlow flows
├── schemas/          # Pydantic models
│   ├── __init__.py
│   ├── requests.py   # API request models
│   └── responses.py  # API response models
├── utils/            # Custom utilities
│   ├── __init__.py
│   ├── call_llm.py
│   └── [other_utils].py
├── docs/
│   └── design.md     # MANDATORY design document
└── requirements.txt
```

## Integration Architecture Pattern

### Complete Integration Flow

```
FastAPI (main.py)
    ↓ receives requests
Pydantic Models (schemas/)
    ↓ validates data
PocketFlow Flows (flow.py)
    ↓ orchestrates logic
PocketFlow Nodes (nodes.py)
    ↓ executes tasks
Utility Functions (utils/)
    ↓ interfaces with external services
FastMCP Tools (when multi-agent coordination needed)
```

This ensures:
- **Type safety** at every boundary with Pydantic
- **Clear separation** between API layer and business logic
- **Modular design** with reusable nodes and utilities
- **Agent coordination** through FastMCP when needed