# Testing Framework Guide

A lightweight testing structure following the TDD workflow: **examples → integrations → unittests**.

## Overview

This testing framework emphasizes simplicity, determinism, and reusability. Each layer serves a specific purpose in the development cycle.

### Three-Layer Structure

```
tests/
├── examples/       # Runnable demos that generate baseline outputs
├── integrations/   # Integration tests comparing against baselines
├── unittests/      # Unit tests for isolated functions
└── test_tools.py   # Shared testing utilities
```

## Layer Details

### 1. Examples (`examples/`)

**Purpose**: Runnable code demonstrating functionality while generating test baselines.

**Key Characteristics**:
- Each file is a standalone script with CLI support
- Generates deterministic outputs (via seeds or mocks)
- Saves JSON snapshots as baselines for integration tests
- Doubles as documentation and demo code

**Minimal Structure**:
```python
# id: examples/01_basic_example
# title: Basic functionality demo
# level: basic
# purpose: demo|test-input
# deterministic: true
# outputs: tests/data/example_output/01_baseline.json

import argparse
import json

def core_logic(input_data, seed=None):
    """Core function implementing the feature"""
    return {"result": "processed"}

def run(mode="demo", seed=None, output_dir=None, save_output=True):
    """Main execution with configurable output"""
    result = core_logic({}, seed)
    assert "result" in result  # Basic validation
    
    if save_output and output_dir:
        with open(f"{output_dir}/output.json", "w") as f:
            json.dump(result, f)
    
    print("=== Result ===")
    print(result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="demo")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--save-output", action="store_true")
    args = parser.parse_args()
    
    run(args.mode, args.seed, args.output_dir, args.save_output)
```

**CLI Requirements**:
- `--mode`: Execution mode (demo, ci_fast, smoke)
- `--seed`: Random seed for determinism
- `--output-dir`: Where to save outputs
- `--save-output`: Flag to enable saving

### 2. Integrations (`integrations/`)

**Purpose**: Verify examples produce expected outputs by comparing against baselines.

**Pattern**:
```python
import subprocess
import json
from tests.test_tools import load_baseline, compare_json_outputs

def test_example_01_baseline():
    """Run example and verify against baseline"""
    result = subprocess.run([
        "python", "tests/examples/01_basic_example.py",
        "--mode", "ci_fast",
        "--seed", "42"
    ], capture_output=True, text=True)
    
    output = json.loads(result.stdout)
    baseline = load_baseline("01_baseline.json")
    
    assert compare_json_outputs(output, baseline, tolerance=0.01)
```

**Best Practices**:
- Use `ci_fast` mode for speed
- Always set `--seed` for determinism
- Use fuzzy comparison for numeric/LLM outputs
- Keep tests independent

### 3. Unittests (`unittests/`)

**Purpose**: Test individual functions in isolation with edge cases.

**Pattern**:
```python
import pytest
from tests.examples.01_basic_example import core_logic

def test_core_logic_basic():
    """Test normal case"""
    result = core_logic({"input": "data"})
    assert "result" in result

def test_core_logic_empty():
    """Test edge case: empty input"""
    result = core_logic({})
    assert result is not None

def test_core_logic_deterministic():
    """Test determinism with seed"""
    result1 = core_logic({}, seed=42)
    result2 = core_logic({}, seed=42)
    assert result1 == result2
```

**Focus Areas**:
- Boundary conditions
- Error handling (when appropriate)
- Determinism verification
- Type validation

## Shared Tools (`test_tools.py`)

Common utilities for all test layers:
- Baseline loading/saving
- Output comparison (strict, fuzzy, field-based)
- Mock data helpers
- Determinism validators

## TDD Workflow

### Step 1: Write Example
```bash
# Create example with baseline generation
python tests/examples/01_example.py --mode demo --seed 42 \
    --output-dir tests/data/example_output --save-output
```

### Step 2: Create Integration Test
```python
# Reference the baseline from step 1
def test_example_01():
    baseline = load_baseline("01_baseline.json")
    # ... comparison logic
```

### Step 3: Extract Unit Tests
```python
# Test core functions from the example
from tests.examples.01_example import core_logic

def test_core_logic():
    # ... unit test logic
```

## Determinism Strategies

### For Randomness
Use `random.seed()` and `--seed` argument:
```python
import random

def run(seed=None):
    if seed:
        random.seed(seed)
    # ... rest of logic
```

### For LLM Outputs
Three approaches (in priority order):
1. **Mock** (preferred): Use pre-saved responses
2. **Seeded**: Use temperature=0 and fixed prompts
3. **Live**: Only for local debugging, skip in CI

### For External APIs
Mock responses during testing:
```python
# tests/data/mocks/api_response.json
{"status": "ok", "data": {...}}
```

## Output Validation

### Strict Comparison
For deterministic outputs:
```python
assert output == baseline
```

### Fuzzy Comparison
For numeric/similarity checks:
```python
from tests.test_tools import compare_with_tolerance

assert compare_with_tolerance(output, baseline, threshold=0.95)
```

### Field-Based Validation
For LLM outputs:
```python
# Check structure, not exact content
assert "response" in output
assert "timestamp" in output
assert len(output["items"]) > 0
```

## Key Principles

1. **KISS**: Simple, readable code over clever optimizations
2. **Single Responsibility**: One example = one concept
3. **Determinism**: Always reproducible with same seed/mock
4. **Modularity**: Small functions, minimal dependencies
5. **Let It Fail**: Don't hide errors, make them obvious

## File Naming

- Examples: `01_feature_name.py`, `02_another_feature.py`
- Integrations: `test_example_01.py`, `test_example_02.py`
- Unittests: `test_feature_name.py`
- Baselines: `01_feature_name_baseline.json`

## Common Patterns

### Metadata Block
```python
# id: examples/01_example
# title: Example title
# level: basic|intermediate|advanced
# purpose: demo|test-input
# deterministic: true|false
# mock_data: tests/data/mocks/example.json
# outputs: tests/data/example_output/01_baseline.json
# run_modes: [demo, ci_fast, smoke]
```

### Print Sections
```python
print("=== Part 1: Setup ===")
# ... code
print("=== Part 2: Processing ===")
# ... code
print("=== Part 3: Results ===")
# ... code
```

### Minimal Validation
```python
# Not this:
if not isinstance(data, dict):
    raise ValueError("Data must be dict")
if "key" not in data:
    raise KeyError("Missing key")

# This:
result = data["key"]  # Let it fail naturally
```

## Next Steps

1. Review example templates in `examples/`
2. Check `test_tools.py` for available utilities
3. Follow the TDD cycle for new features
4. Keep it simple and readable
