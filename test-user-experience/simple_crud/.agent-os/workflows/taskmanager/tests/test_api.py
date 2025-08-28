import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from taskmanager.main import app

client = TestClient(app)

