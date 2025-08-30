"""
Tests for utility functions enhanced with proper type hints and docstrings.
Validates Task 2.3: Add proper type hints and docstrings for all utilities.
"""

import pytest
from typing import Dict, Any, List
from ..utils.call_llm_analyzer import call_llm_analyzer
from ..utils.retrieve_documents import retrieve_documents


class TestCallLLMAnalyzer:
    """Tests for call_llm_analyzer utility function type hints and docstrings."""

    def test_function_exists(self):
        """Test that call_llm_analyzer function exists and is callable."""
        assert callable(call_llm_analyzer)

    def test_function_annotations(self):
        """Test that function has proper type hints."""
        annotations = call_llm_analyzer.__annotations__
        assert "context" in annotations
        assert "query" in annotations
        assert "return" in annotations
        # Verify string type hints
        assert annotations["context"] == str
        assert annotations["query"] == str
        assert annotations["return"] == str

    def test_function_docstring(self):
        """Test that function has comprehensive docstring."""
        docstring = call_llm_analyzer.__doc__
        assert docstring is not None
        assert len(docstring) > 100  # Should be comprehensive
        assert "Args:" in docstring
        assert "Returns:" in docstring
        assert "Raises:" in docstring
        assert "context" in docstring
        assert "query" in docstring

    @pytest.mark.asyncio
    async def test_input_validation_empty_context(self):
        """Test validation for empty context."""
        with pytest.raises(ValueError, match="Context cannot be empty"):
            await call_llm_analyzer("", "test query")

    @pytest.mark.asyncio
    async def test_input_validation_empty_query(self):
        """Test validation for empty query."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await call_llm_analyzer("test context", "")

    @pytest.mark.asyncio
    async def test_input_validation_whitespace_context(self):
        """Test validation for whitespace-only context."""
        with pytest.raises(ValueError, match="Context cannot be empty"):
            await call_llm_analyzer("   ", "test query")

    @pytest.mark.asyncio
    async def test_input_validation_whitespace_query(self):
        """Test validation for whitespace-only query."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await call_llm_analyzer("test context", "   ")

    @pytest.mark.asyncio
    async def test_not_implemented_error(self):
        """Test that function raises NotImplementedError (template state)."""
        with pytest.raises(NotImplementedError, match="not implemented"):
            await call_llm_analyzer("valid context", "valid query")


class TestRetrieveDocuments:
    """Tests for retrieve_documents utility function type hints and docstrings."""

    def test_function_exists(self):
        """Test that retrieve_documents function exists and is callable."""
        assert callable(retrieve_documents)

    def test_function_annotations(self):
        """Test that function has proper type hints."""
        annotations = retrieve_documents.__annotations__
        assert "query" in annotations
        assert "return" in annotations
        # Verify the return type is List[Dict[str, Any]]
        assert str(annotations["return"]) == "typing.List[typing.Dict[str, typing.Any]]"

    def test_function_docstring(self):
        """Test that function has comprehensive docstring."""
        docstring = retrieve_documents.__doc__
        assert docstring is not None
        assert len(docstring) > 200  # Should be very comprehensive
        assert "Args:" in docstring
        assert "Returns:" in docstring
        assert "Raises:" in docstring
        assert "similarity_threshold" in docstring
        assert "metadata_filters" in docstring
        assert "Example:" in docstring

    @pytest.mark.asyncio
    async def test_input_validation_empty_query(self):
        """Test validation for empty query."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await retrieve_documents("")

    @pytest.mark.asyncio
    async def test_input_validation_whitespace_query(self):
        """Test validation for whitespace-only query."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await retrieve_documents("   ")

    @pytest.mark.asyncio
    async def test_input_validation_negative_limit(self):
        """Test validation for negative limit."""
        with pytest.raises(ValueError, match="Limit must be positive"):
            await retrieve_documents("test", limit=-1)

    @pytest.mark.asyncio
    async def test_input_validation_zero_limit(self):
        """Test validation for zero limit."""
        with pytest.raises(ValueError, match="Limit must be positive"):
            await retrieve_documents("test", limit=0)

    @pytest.mark.asyncio
    async def test_input_validation_invalid_threshold_high(self):
        """Test validation for similarity threshold too high."""
        with pytest.raises(ValueError, match="Similarity threshold must be between"):
            await retrieve_documents("test", similarity_threshold=1.5)

    @pytest.mark.asyncio
    async def test_input_validation_invalid_threshold_low(self):
        """Test validation for similarity threshold too low."""
        with pytest.raises(ValueError, match="Similarity threshold must be between"):
            await retrieve_documents("test", similarity_threshold=-0.1)

    @pytest.mark.asyncio
    async def test_input_validation_invalid_timeout(self):
        """Test validation for invalid timeout."""
        with pytest.raises(ValueError, match="Timeout must be positive"):
            await retrieve_documents("test", timeout_seconds=-1)

    @pytest.mark.asyncio
    async def test_not_implemented_error(self):
        """Test that function raises NotImplementedError (template state)."""
        with pytest.raises(NotImplementedError, match="not implemented"):
            await retrieve_documents("valid query")

    def test_default_parameters(self):
        """Test that function has appropriate default parameters."""
        import inspect
        sig = inspect.signature(retrieve_documents)
        
        # Check default values
        assert sig.parameters["limit"].default is None
        assert sig.parameters["similarity_threshold"].default == 0.7
        assert sig.parameters["metadata_filters"].default is None
        assert sig.parameters["include_embeddings"].default is False
        assert sig.parameters["timeout_seconds"].default == 30.0


class TestUtilityPackage:
    """Tests for utils package structure and exports."""

    def test_package_imports(self):
        """Test that utils package properly exports functions."""
        from ..utils import call_llm_analyzer, retrieve_documents
        assert callable(call_llm_analyzer)
        assert callable(retrieve_documents)

    def test_package_all_attribute(self):
        """Test that utils package has __all__ defined correctly."""
        from .. import utils
        assert hasattr(utils, "__all__")
        assert "call_llm_analyzer" in utils.__all__
        assert "retrieve_documents" in utils.__all__
        assert len(utils.__all__) == 2

    def test_package_docstring(self):
        """Test that utils package has descriptive docstring."""
        from .. import utils
        assert utils.__doc__ is not None
        assert "PocketFlow" in utils.__doc__
        assert "utility functions" in utils.__doc__