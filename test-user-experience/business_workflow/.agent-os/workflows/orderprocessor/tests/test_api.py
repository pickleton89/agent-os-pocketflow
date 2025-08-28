import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from orderprocessor.main import app

client = TestClient(app)

