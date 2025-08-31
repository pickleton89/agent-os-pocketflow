# Pattern Analyzer Enhancement Implementation Plan

## Overview
Complete the pattern coverage in `pattern_analyzer.py` by addressing three key gaps:
1. **HYBRID pattern incomplete** - missing pattern indicators
2. **Missing auxiliary patterns** - SIMPLE_WORKFLOW, BASIC_API, SIMPLE_ETL not analyzed
3. **No dynamic pattern detection** - can't detect combinations (e.g., RAG + Agent)

## Phase 1: Complete HYBRID Pattern Implementation

### Target: `pocketflow-tools/pattern_analyzer.py` line ~237
**Add to `_load_pattern_indicators()` method:**

```python
# HYBRID Pattern Indicators
PatternIndicator(
    pattern=PatternType.HYBRID,
    keywords=[
        "combine", "mixed", "composite", "hybrid", "integrated", 
        "multi-pattern", "fusion", "blend", "merge", "unified",
        "cross-pattern", "heterogeneous", "compound", "layered"
    ],
    weight=1.1,  # Slightly higher due to complexity
    context_multipliers={
        "complex": 1.3,
        "multiple": 1.2,
        "combined": 1.4,
        "integrated": 1.2,
        "advanced": 1.2
    }
)
```

## Phase 2: Add Auxiliary Pattern Support

### Target: New method in `PatternAnalyzer` class
**Add `_load_auxiliary_pattern_indicators()` method:**

```python
def _load_auxiliary_pattern_indicators(self) -> List[PatternIndicator]:
    """Load auxiliary pattern indicators for simple patterns."""
    return [
        # SIMPLE_WORKFLOW indicators
        PatternIndicator(
            pattern="SIMPLE_WORKFLOW",  # String-based pseudo-enum
            keywords=["simple", "basic", "straightforward", "linear", "sequential"],
            weight=0.8,  # Lower weight for simplicity
            context_multipliers={"crud": 1.3, "form": 1.2}
        ),
        # BASIC_API indicators  
        PatternIndicator(
            pattern="BASIC_API",
            keywords=["api", "endpoint", "request", "response", "service"],
            weight=0.9,
            context_multipliers={"rest": 1.2, "json": 1.1}
        ),
        # SIMPLE_ETL indicators
        PatternIndicator(
            pattern="SIMPLE_ETL", 
            keywords=["extract", "transform", "load", "etl", "data pipeline"],
            weight=0.9,
            context_multipliers={"data": 1.2, "pipeline": 1.3}
        )
    ]
```

### Modify `__init__()` method:
```python
def __init__(self):
    self.pattern_indicators = self._load_pattern_indicators()
    self.auxiliary_indicators = self._load_auxiliary_pattern_indicators()  # NEW
    self.context_rules = self._load_context_rules()
    # ... rest unchanged
```

## Phase 3: Dynamic Pattern Combination Detection

### Add new methods to `PatternAnalyzer` class:

```python
def detect_pattern_combinations(self, pattern_scores: List[PatternScore]) -> Dict[str, Any]:
    """Detect when multiple patterns should be combined into HYBRID."""
    
    # Define combination rules
    combinations = {
        "intelligent_rag": {"patterns": [PatternType.RAG, PatternType.AGENT], "threshold": 0.7},
        "integration_workflow": {"patterns": [PatternType.TOOL, PatternType.WORKFLOW], "threshold": 0.6},
        "smart_processing": {"patterns": [PatternType.MAPREDUCE, PatternType.AGENT], "threshold": 0.7}
    }
    
    # Detection logic here
    detected = {}
    for combo_name, combo_def in combinations.items():
        scores = {p: 0 for p in combo_def["patterns"]}
        for score in pattern_scores:
            if score.pattern in combo_def["patterns"]:
                scores[score.pattern] = score.total_score
        
        if all(score >= combo_def["threshold"] for score in scores.values()):
            detected[combo_name] = {
                "patterns": combo_def["patterns"],
                "combined_score": sum(scores.values()) * 0.8  # Slight penalty for complexity
            }
    
    return detected
```

## Phase 4: Enhanced Scoring and Recommendation

### Modify `score_patterns()` method:
- Add auxiliary pattern scoring alongside main patterns
- Include combination detection logic
- Return both individual and combination scores

### Modify `generate_recommendation()` method:
- Check for detected combinations first
- Set HYBRID as primary when combination detected
- Enhanced rationale explaining combination choice

## Phase 5: Testing

### Add test cases to `pocketflow-tools/test-generator.py`:
```python
def test_hybrid_pattern_detection():
    analyzer = PatternAnalyzer()
    
    # Test HYBRID keywords
    hybrid_req = "I need a combined RAG and agent system with integrated search"
    result = analyzer.analyze_and_recommend(hybrid_req)
    assert result.primary_pattern == PatternType.HYBRID
    
    # Test auxiliary patterns
    simple_req = "Basic CRUD operations with simple form processing"
    result = analyzer.analyze_and_recommend(simple_req)
    # Should detect SIMPLE_WORKFLOW auxiliary pattern
```

## Implementation Checklist

- [ ] **Phase 1**: Add HYBRID PatternIndicator to `_load_pattern_indicators()`
- [ ] **Phase 2**: Create `_load_auxiliary_pattern_indicators()` method
- [ ] **Phase 2**: Modify `__init__()` to load auxiliary indicators  
- [ ] **Phase 2**: Update `score_patterns()` to handle auxiliary patterns
- [ ] **Phase 3**: Add `detect_pattern_combinations()` method
- [ ] **Phase 3**: Add combination logic to scoring pipeline
- [ ] **Phase 4**: Update `generate_recommendation()` for combination handling
- [ ] **Phase 4**: Enhance rationale generation for combinations
- [ ] **Phase 5**: Add comprehensive test cases
- [ ] **Phase 5**: Test with real requirements examples

## Expected Results

✅ **100% Pattern Coverage**: All PocketFlow patterns properly detected  
✅ **Smart Combinations**: RAG+Agent, Tool+Workflow automatically detected as HYBRID  
✅ **Auxiliary Support**: Simple patterns (SIMPLE_WORKFLOW, etc.) properly scored  
✅ **Better Recommendations**: More nuanced selection for complex requirements  

## Files Modified
- `pocketflow-tools/pattern_analyzer.py` (primary implementation)
- `pocketflow-tools/test-generator.py` (testing)
- Documentation updates as needed

## Progress Tracking

Use this checklist to track implementation progress:

### Phase 1 Progress
- [ ] Research current HYBRID enum definition
- [ ] Add HYBRID PatternIndicator with comprehensive keywords
- [ ] Test HYBRID pattern detection with sample requirements
- [ ] Verify HYBRID appears in pattern recommendations

### Phase 2 Progress  
- [ ] Create auxiliary pattern indicators method
- [ ] Integrate auxiliary patterns into scoring pipeline
- [ ] Test auxiliary pattern detection
- [ ] Verify auxiliary patterns work with existing complexity mapping

### Phase 3 Progress
- [ ] Design combination detection rules
- [ ] Implement combination detection logic
- [ ] Test combination scenarios
- [ ] Verify HYBRID selection for detected combinations

### Phase 4 Progress
- [ ] Enhance recommendation generation for combinations
- [ ] Update rationale generation with combination explanations
- [ ] Test end-to-end recommendation pipeline
- [ ] Verify template customizations work with HYBRID

### Phase 5 Progress
- [ ] Write comprehensive test cases
- [ ] Test with real-world requirements
- [ ] Performance testing with enhanced analyzer
- [ ] Documentation updates

## Notes

- Maintain backward compatibility throughout implementation
- Focus on incremental improvements that can be tested independently
- Keep performance impact minimal with efficient scoring algorithms
- Ensure comprehensive logging for debugging complex pattern detection