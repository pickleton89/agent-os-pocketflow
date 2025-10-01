# FastAPI Style Guide

> Version: 1.0.0
> Last Updated: 2025-01-11

## FastAPI-Specific Conventions

This file contains detailed FastAPI patterns and conventions that extend the base code-style.md rules.

## Project Structure

### Standard Layout
```
project/
├── main.py              # FastAPI app entry point
├── config.py            # Settings and configuration
├── dependencies.py      # Shared dependencies
├── middleware.py        # Custom middleware
├── routers/            # API route modules
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── items.py
├── schemas/            # Pydantic models
│   ├── __init__.py
│   ├── requests.py     # Request models
│   ├── responses.py    # Response models
│   └── common.py       # Shared models
├── services/           # Business logic
│   ├── __init__.py
│   ├── auth_service.py
│   └── user_service.py
├── utils/              # Utility functions
│   ├── __init__.py
│   └── validators.py
└── tests/              # Test files
    ├── __init__.py
    ├── test_auth.py
    └── test_users.py
```

## Application Setup

### Main Application
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from .config import settings
from .routers import auth, users, items

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("Starting up", environment=settings.ENVIRONMENT)
    yield
    # Shutdown
    logger.info("Shutting down")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs" if settings.SHOW_DOCS else None,
    redoc_url="/redoc" if settings.SHOW_DOCS else None,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
```

### Configuration Management
```python
# config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings."""
    
    APP_NAME: str = "MyAPI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI application"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str
    
    # Features
    SHOW_DOCS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## Router Organization

### Router Module Pattern
```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from ..schemas.requests import UserCreate, UserUpdate
from ..schemas.responses import UserResponse, UsersListResponse
from ..services import user_service
from ..dependencies import get_current_user, PaginationParams

router = APIRouter()

@router.get("/", response_model=UsersListResponse)
async def list_users(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None, description="Search term"),
    current_user: User = Depends(get_current_user),
) -> UsersListResponse:
    """List all users with pagination."""
    users = await user_service.list_users(
        skip=pagination.skip,
        limit=pagination.limit,
        search=search,
    )
    return UsersListResponse(
        users=users,
        total=len(users),
        skip=pagination.skip,
        limit=pagination.limit,
    )

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Create a new user."""
    user = await user_service.create_user(user_data)
    return UserResponse.from_orm(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get user by ID."""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Update user by ID."""
    user = await user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return UserResponse.from_orm(user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete user by ID."""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
```

## Schema Organization

### Request Models
```python
# schemas/requests.py
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    """User creation request."""
    
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    birth_date: Optional[date] = Field(None, description="Date of birth")
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "birth_date": "1990-01-01",
            }
        }

class UserUpdate(BaseModel):
    """User update request."""
    
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    birth_date: Optional[date] = None
```

### Response Models
```python
# schemas/responses.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class UserResponse(BaseModel):
    """User response model."""
    
    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    birth_date: Optional[date] = Field(None, description="Date of birth")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy
        
class UsersListResponse(BaseModel):
    """Paginated users list response."""
    
    users: List[UserResponse]
    total: int = Field(..., description="Total number of users")
    skip: int = Field(..., description="Number of skipped items")
    limit: int = Field(..., description="Page size limit")
    
class ErrorResponse(BaseModel):
    """Standard error response."""
    
    detail: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## Dependencies

### Common Dependencies
```python
# dependencies.py
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import JWTError, jwt

from .config import settings
from .schemas.common import TokenData, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

class PaginationParams:
    """Common pagination parameters."""
    
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    ):
        self.skip = skip
        self.limit = limit
```

## Error Handling

### Exception Handlers
```python
# main.py or exceptions.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, 
    exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )

# Custom exceptions
class ResourceNotFoundError(HTTPException):
    """Resource not found exception."""
    
    def __init__(self, resource: str, id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {id} not found",
        )

class PermissionDeniedError(HTTPException):
    """Permission denied exception."""
    
    def __init__(self, action: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied for action: {action}",
        )
```

## Middleware

### Custom Middleware
```python
# middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import structlog
from uuid import uuid4

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        
        # Add request ID to logger context
        structlog.contextvars.bind_contextvars(request_id=request_id)
        
        # Log request
        logger.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            client=request.client.host,
        )
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            "Request completed",
            status_code=response.status_code,
            process_time=round(process_time, 3),
        )
        
        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

# Register middleware
app.add_middleware(LoggingMiddleware)
```

## Background Tasks

### Task Patterns
```python
from fastapi import BackgroundTasks

@router.post("/send-notification/")
async def send_notification(
    email: EmailStr,
    background_tasks: BackgroundTasks,
) -> dict:
    """Send notification email in background."""
    
    # Add task to background
    background_tasks.add_task(
        send_email_notification,
        email=email,
        subject="Welcome!",
        body="Thank you for signing up.",
    )
    
    return {"message": "Notification will be sent"}

async def send_email_notification(
    email: str, 
    subject: str, 
    body: str
) -> None:
    """Background task to send email."""
    logger.info("Sending email", email=email, subject=subject)
    # Email sending logic here
    await asyncio.sleep(2)  # Simulate email sending
    logger.info("Email sent successfully", email=email)
```

## WebSocket Endpoints

### WebSocket Pattern
```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_personal_message(self, message: str, client_id: str):
        if websocket := self.active_connections.get(client_id):
            await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication."""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client {client_id} left")
```

## Testing Patterns

### API Testing
```python
# tests/test_users.py
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import pytest

from ..main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    """Get authentication headers for testing."""
    return {"Authorization": "Bearer test-token"}

def test_create_user(auth_headers):
    """Test user creation endpoint."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_async_endpoint():
    """Test async endpoint with mocking."""
    with patch("app.services.user_service.get_user") as mock_get:
        mock_get.return_value = AsyncMock(
            return_value={"id": "123", "email": "test@example.com"}
        )
        
        response = client.get("/api/v1/users/123")
        assert response.status_code == 200
```

## Performance Best Practices

### Response Model Optimization
```python
# Use response_model_exclude_unset to omit null fields
@router.get("/users/{user_id}", response_model_exclude_unset=True)
async def get_user(user_id: int):
    return await get_user_from_db(user_id)

# Use response_model_include/exclude for field selection
@router.get(
    "/users/{user_id}/public",
    response_model=User,
    response_model_exclude={"password", "email"},
)
async def get_public_user(user_id: int):
    return await get_user_from_db(user_id)
```

### Database Connection Pooling
```python
# Use async database sessions with context manager
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Use in endpoints
@router.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```