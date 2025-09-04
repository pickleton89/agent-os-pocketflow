from pathlib import Path
from typing import Dict

from pocketflow_tools.spec import WorkflowSpec
from pocketflow_tools.generators.template_engine import TemplateEngine
from pocketflow_tools.generators.code_generators import (
    generate_utility,
    generate_pydantic_models,
    generate_nodes,
    generate_flow,
    generate_init_file,
    generate_install_checker_reference,
    generate_fastapi_main,
    generate_fastapi_router,
)
from pocketflow_tools.generators.doc_generators import (
    generate_design_doc,
    generate_tasks,
)
from pocketflow_tools.generators.test_generators import (
    generate_node_tests,
    generate_flow_tests,
    generate_api_tests,
)
from pocketflow_tools.generators.config_generators import (
    generate_dependency_files,
    generate_basic_pyproject,
)
from pocketflow_tools.generators.context import GenerationContext


class PocketFlowGenerator:
    """Compose and generate PocketFlow workflows.

    Complete modular implementation using all new generator functions.
    """

    def __init__(
        self,
        templates_path: str = "templates",
        output_path: str = ".agent-os/workflows",
        enable_hybrid_promotion: bool = False,
    ) -> None:
        self.templates_path = Path(templates_path)
        self.output_path = Path(output_path)
        self.enable_hybrid_promotion = enable_hybrid_promotion

        # Ensure output directory exists 
        self.output_path.mkdir(exist_ok=True, parents=True)

        # Load templates and extensions via new TemplateEngine
        # Create fallback empty context if templates directory doesn't exist
        try:
            engine = TemplateEngine(self.templates_path)
            templates = engine.load_templates()
            extensions = engine.load_enhanced_extensions()
        except (FileNotFoundError, OSError):
            # Fallback to empty templates/extensions if directory missing
            templates = {}
            extensions = {}
        
        # Build generation context for sharing across generation steps
        self.context = GenerationContext(
            templates=templates,
            extensions=extensions,
            enable_hybrid_promotion=self.enable_hybrid_promotion,
        )

    def _detect_batch_patterns(self, spec: WorkflowSpec) -> WorkflowSpec:
        """Analyze nodes and suggest BatchNode usage when appropriate patterns are detected."""
        import copy
        import re
        
        # Input validation
        if not spec or not hasattr(spec, 'nodes') or not spec.nodes:
            return spec
            
        # Collection-related keywords that suggest batch processing
        collection_keywords = {
            'files', 'documents', 'document', 'items', 'records', 'entries', 'elements',
            'data', 'chunks', 'pieces', 'segments', 'batches', 'groups',
            'collections', 'collection', 'lists', 'arrays', 'datasets', 'sources',
            'inputs', 'outputs', 'results', 'responses', 'queries'
        }
        
        # Iteration-related keywords in descriptions
        iteration_keywords = {
            'process', 'handle', 'transform', 'analyze', 'parse', 'convert',
            'generate', 'create', 'load', 'fetch', 'retrieve', 'extract',
            'validate', 'filter', 'sort', 'group', 'aggregate', 'summarize'
        }
        
        # All batch node types to exclude from suggestions
        batch_node_types = {
            'BatchNode', 'AsyncBatchNode', 'AsyncParallelBatchNode'
        }
        
        # Improved plural detection with proper word boundary matching
        def is_likely_plural(name: str) -> bool:
            if not name or not isinstance(name, str):
                return False
                
            name_lower = name.lower()
            
            # Common plural patterns
            if name_lower.endswith(('s', 'es', 'ies', 'ves')):
                # False positives - words that end in these patterns but aren't plural
                false_positives = {
                    'process', 'address', 'analysis', 'class', 'pass',
                    'access', 'success', 'express', 'suppress', 'progress',
                    'business', 'status', 'focus', 'basis', 'crisis', 'stress',
                    'eness', 'ness'  # Common suffixes that aren't plural
                }
                
                # Check if the entire name ends with a false positive word
                if any(name_lower.endswith(fp) for fp in false_positives):
                    return False
                    
                # Additional check: avoid very short names that might be acronyms
                if len(name_lower) <= 3:
                    return False
                    
                return True
            return False

        updated_nodes = []
        for node in spec.nodes:
            if not isinstance(node, dict):
                updated_nodes.append(node)
                continue
                
            node_name = node.get('name', '')
            node_desc = node.get('description', '')
            node_type = node.get('type', 'Node')
            
            # Skip if essential data is missing
            if not node_name and not node_desc:
                updated_nodes.append(node)
                continue
                
            # Ensure description is a string and convert to lowercase for analysis
            node_desc_lower = node_desc.lower() if isinstance(node_desc, str) else ''
            
            # Check for batch processing indicators
            batch_indicators = []
            
            # 1. Check for plural nouns in node names
            if is_likely_plural(node_name):
                batch_indicators.append("plural noun in name")
            
            # 2. Check for collection-related keywords in description
            if node_desc_lower:
                desc_words = set(re.findall(r'\b\w+\b', node_desc_lower))
                if desc_words & collection_keywords:
                    batch_indicators.append("collection-related keywords")
                
                # 3. Check for iteration patterns combined with collections
                # Only add if we have both iteration AND collection words
                has_iteration = bool(desc_words & iteration_keywords)
                has_collection = bool(desc_words & collection_keywords)
                if has_iteration and has_collection:
                    # Only add if we haven't already added collection keywords
                    if "collection-related keywords" not in batch_indicators:
                        batch_indicators.append("iteration pattern with collections")
                
                # 4. Check for explicit plural/multiple mentions
                plural_phrases = ['multiple', 'many', 'all', 'each', 'every', 'several', 'various']
                if any(phrase in node_desc_lower for phrase in plural_phrases):
                    batch_indicators.append("explicit multiple item mentions")
            
            # Generate batch node suggestion comments if indicators found
            if batch_indicators and node_type not in batch_node_types:
                guidance_comments = [
                    "# SMART PATTERN DETECTION: This node may benefit from batch processing",
                    f"# Detected indicators: {', '.join(batch_indicators)}",
                    "# CONSIDER: Using BatchNode instead of Node for better performance",
                    "# BatchNode automatically handles:",
                    "#   - Parallel processing of multiple items",
                    "#   - Automatic chunking and batching",
                    "#   - Built-in error handling per item",
                    "#   - Progress tracking and logging"
                ]
                
                # Use deep copy to avoid modifying original spec
                node_copy = copy.deepcopy(node)
                node_copy.setdefault('framework_reminders', []).extend(guidance_comments)
                updated_nodes.append(node_copy)
            else:
                # Still use deep copy for consistency
                updated_nodes.append(copy.deepcopy(node))
        
        # Create new spec with enhanced nodes (don't modify original)
        spec_copy = copy.deepcopy(spec)
        spec_copy.nodes = updated_nodes
        return spec_copy

    def _enrich_spec_with_pattern_nodes(self, spec: WorkflowSpec) -> WorkflowSpec:
        """Enrich spec with pattern-specific nodes, utilities, and API endpoints."""
        # Define pattern-specific node configurations
        pattern_node_configs = {
            "RAG": [
                {"name": "DocumentLoader", "type": "Node", "description": "Load and preprocess documents for indexing"},
                {"name": "TextChunker", "type": "Node", "description": "Split documents into manageable chunks"},
                {"name": "EmbeddingGenerator", "type": "AsyncNode", "description": "Generate embeddings for text chunks"},
                {"name": "QueryProcessor", "type": "Node", "description": "Process and analyze incoming queries"},
                {"name": "Retriever", "type": "AsyncNode", "description": "Retrieve relevant documents based on query"},
                {"name": "ContextFormatter", "type": "Node", "description": "Format retrieved context for response generation"},
                {"name": "ResponseGenerator", "type": "AsyncNode", "description": "Generate response using retrieved context"},
            ],
            "AGENT": [
                {"name": "TaskAnalyzer", "type": "AsyncNode", "description": "Analyze incoming tasks and requirements"},
                {"name": "ReasoningEngine", "type": "AsyncNode", "description": "Apply reasoning and decision-making logic"},
                {"name": "ActionPlanner", "type": "AsyncNode", "description": "Plan sequence of actions to accomplish task"},
                {"name": "ActionExecutor", "type": "AsyncNode", "description": "Execute planned actions and tools"},
                {"name": "ResultEvaluator", "type": "Node", "description": "Evaluate results and determine next steps"},
                {"name": "MemoryUpdater", "type": "Node", "description": "Update agent memory with new information"},
            ],
            "TOOL": [
                {"name": "RequestValidator", "type": "Node", "description": "Validate incoming API requests"},
                {"name": "AuthHandler", "type": "AsyncNode", "description": "Handle authentication and authorization"},
                {"name": "ExternalConnector", "type": "AsyncNode", "description": "Connect to external APIs and services"},
                {"name": "DataTransformer", "type": "Node", "description": "Transform data between formats"},
                {"name": "ResponseProcessor", "type": "Node", "description": "Process and format API responses"},
            ],
            "WORKFLOW": [
                {"name": "InputValidator", "type": "Node", "description": "Validate and sanitize input data"},
                {"name": "BusinessLogicProcessor", "type": "Node", "description": "Execute core business logic"},
                {"name": "OutputFormatter", "type": "Node", "description": "Format output data for consumers"},
            ],
        }

        # Define pattern-specific utilities
        pattern_utilities = {
            "RAG": [
                {"name": "vector_search", "description": "Search vector database for similar embeddings", "parameters": [
                    {"name": "query_embedding", "type": "List[float]", "optional": False},
                    {"name": "top_k", "type": "int", "optional": True}
                ], "return_type": "List[Dict[str, Any]]"},
                {"name": "chunk_text", "description": "Split text into semantic chunks", "parameters": [
                    {"name": "text", "type": "str", "optional": False},
                    {"name": "chunk_size", "type": "int", "optional": True}
                ], "return_type": "List[str]"},
            ],
            "AGENT": [
                {"name": "llm_reasoning", "description": "Apply LLM-based reasoning to analyze problems", "parameters": [
                    {"name": "context", "type": "str", "optional": False},
                    {"name": "task", "type": "str", "optional": False}
                ], "return_type": "str", "async": True},
                {"name": "action_planning", "description": "Generate step-by-step action plan", "parameters": [
                    {"name": "goal", "type": "str", "optional": False}
                ], "return_type": "List[Dict[str, str]]"},
            ],
            "TOOL": [
                {"name": "http_client", "description": "Make HTTP requests to external APIs", "parameters": [
                    {"name": "url", "type": "str", "optional": False},
                    {"name": "method", "type": "str", "optional": True},
                    {"name": "headers", "type": "Dict[str, str]", "optional": True}
                ], "return_type": "Dict[str, Any]", "async": True},
                {"name": "data_mapper", "description": "Map data between different schemas", "parameters": [
                    {"name": "data", "type": "Dict[str, Any]", "optional": False},
                    {"name": "mapping_config", "type": "Dict[str, str]", "optional": False}
                ], "return_type": "Dict[str, Any]"},
            ],
        }

        # Define pattern-specific API endpoints
        pattern_endpoints = {
            "RAG": [
                {"name": "SearchQuery", "path": "/search", "method": "post", "description": "Search knowledge base with query",
                 "request_fields": [{"name": "query", "type": "str"}, {"name": "limit", "type": "Optional[int]"}],
                 "response_fields": [{"name": "results", "type": "List[Dict[str, Any]]"}, {"name": "count", "type": "int"}]},
            ],
            "AGENT": [
                {"name": "ProcessTask", "path": "/process", "method": "post", "description": "Process task using agent reasoning",
                 "request_fields": [{"name": "task", "type": "str"}, {"name": "context", "type": "Optional[str]"}],
                 "response_fields": [{"name": "result", "type": "str"}, {"name": "actions_taken", "type": "List[str]"}]},
            ],
            "TOOL": [
                {"name": "ExecuteTool", "path": "/execute", "method": "post", "description": "Execute tool integration",
                 "request_fields": [{"name": "operation", "type": "str"}, {"name": "parameters", "type": "Dict[str, Any]"}],
                 "response_fields": [{"name": "status", "type": "str"}, {"name": "data", "type": "Dict[str, Any]"}]},
            ],
            "WORKFLOW": [
                {"name": "ProcessWorkflow", "path": "/process", "method": "post", "description": "Process workflow request",
                 "request_fields": [{"name": "input_data", "type": "Dict[str, Any]"}],
                 "response_fields": [{"name": "output_data", "type": "Dict[str, Any]"}, {"name": "status", "type": "str"}]},
            ],
        }

        # Define pattern-specific shared store schemas
        pattern_schemas = {
            "RAG": {
                "query": "str",
                "documents": "List[Dict[str, Any]]",
                "embeddings": "List[List[float]]",
                "search_results": "List[Dict[str, Any]]",
                "context": "str",
                "response": "str",
            },
            "AGENT": {
                "task": "str",
                "context": "Optional[str]",
                "reasoning_steps": "List[str]", 
                "action_plan": "List[Dict[str, str]]",
                "actions_taken": "List[str]",
                "result": "str",
                "memory": "Dict[str, Any]",
            },
            "TOOL": {
                "request_data": "Dict[str, Any]",
                "auth_token": "Optional[str]",
                "external_response": "Dict[str, Any]",
                "transformed_data": "Dict[str, Any]",
                "response_data": "Dict[str, Any]",
            },
            "WORKFLOW": {
                "input_data": "Dict[str, Any]",
                "validation_result": "Dict[str, Any]",
                "processed_data": "Dict[str, Any]",
                "output_data": "Dict[str, Any]",
            },
        }

        # Enrich spec if it has empty nodes
        if not spec.nodes and spec.pattern in pattern_node_configs:
            spec.nodes = pattern_node_configs[spec.pattern]

        # Enrich utilities
        if not spec.utilities and spec.pattern in pattern_utilities:
            spec.utilities = pattern_utilities[spec.pattern]

        # Enrich API endpoints  
        if not spec.api_endpoints and spec.pattern in pattern_endpoints:
            spec.api_endpoints = pattern_endpoints[spec.pattern]

        # Enrich shared store schema
        if not spec.shared_store_schema and spec.pattern in pattern_schemas:
            spec.shared_store_schema = pattern_schemas[spec.pattern]

        return spec

    def generate_workflow(self, spec: WorkflowSpec) -> Dict[str, str]:
        """Generate all workflow files using the new modular generators."""
        # Apply smart pattern detection for batch processing suggestions
        spec_with_patterns = self._detect_batch_patterns(spec)
        
        # Enrich spec with pattern-specific nodes, utilities, and endpoints
        enriched_spec = self._enrich_spec_with_pattern_nodes(spec_with_patterns)
        
        output_files = {}
        
        # Generate core code files - these return strings, need to map to filenames
        output_files["schemas/models.py"] = generate_pydantic_models(enriched_spec)
        output_files["nodes.py"] = generate_nodes(enriched_spec) 
        output_files["flow.py"] = generate_flow(enriched_spec)
        output_files["__init__.py"] = generate_init_file(enriched_spec, is_root=True)
        output_files["schemas/__init__.py"] = generate_init_file(enriched_spec, is_schema=True)
        output_files["tests/__init__.py"] = generate_init_file(enriched_spec, is_test=True)
        output_files["utils/__init__.py"] = generate_init_file(enriched_spec, is_utils=True)
        
        # Generate utilities - need to pass individual utilities from spec
        for utility in enriched_spec.utilities:
            utility_content = generate_utility(utility)
            utility_name = utility.get('name', 'utility').lower()
            output_files[f"utils/{utility_name}.py"] = utility_content
        
        # Generate FastAPI components  
        output_files["main.py"] = generate_fastapi_main(enriched_spec)
        output_files["router.py"] = generate_fastapi_router(enriched_spec)
        
        # Generate configuration files - this returns a Dict[str, str] including README.md
        output_files.update(generate_dependency_files(enriched_spec))
        
        output_files["pyproject.toml"] = generate_basic_pyproject(enriched_spec)
        
        # Generate documentation
        output_files["docs/design.md"] = generate_design_doc(enriched_spec)
        output_files["docs/tasks.md"] = generate_tasks(enriched_spec)
        
        # Generate tests
        output_files["tests/test_nodes.py"] = generate_node_tests(enriched_spec)
        output_files["tests/test_flow.py"] = generate_flow_tests(enriched_spec)
        output_files["tests/test_api.py"] = generate_api_tests(enriched_spec)
        
        # Generate install checker reference - no parameters
        output_files["check_install.py"] = generate_install_checker_reference()
        
        return output_files

    def save_workflow(self, spec: WorkflowSpec, output_files: Dict[str, str]) -> None:
        """Save generated workflow files to disk."""
        # Safely sanitize workflow directory name
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9]', '', spec.name.lower())
        if not safe_name:  # Fallback if name becomes empty after sanitization
            safe_name = "workflow"
            
        workflow_dir = self.output_path / safe_name
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        for relative_path, content in output_files.items():
            file_path = workflow_dir / relative_path
            # Ensure we don't create files outside the workflow directory
            if not str(file_path).startswith(str(workflow_dir)):
                continue  # Skip potentially dangerous paths
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')

