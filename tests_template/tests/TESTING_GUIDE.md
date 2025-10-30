# Testing Framework Guide

Simple three-layer TDD workflow: **Examples → Integrations → Unittests**

## TDD Development Flow

### Step 1: Write Example (Executable Demo)
Create runnable code in `examples/` that demonstrates the feature.

### Step 2: Integration Test (Verify Output)
Write integration tests to verify example outputs match expectations.

### Step 3: Unit Tests (Edge Cases)
Extract and test individual functions with boundary conditions.

---

## Directory Structure

```
tests/
├── data_input/         # Git-tracked standard inputs
├── data_input_local/   # Your local input overrides (not tracked)
├── data_output/        # Auto-generated outputs (not tracked)
├── examples/           # Runnable demos
├── integrations/       # Integration tests
├── unittests/          # Unit tests
└── test_tools.py       # Shared utilities
```

---

## Example Template

Minimal structure for `examples/01_my_feature.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.test_tools import load, save


def my_feature_main():
    input_data = load()
    
    # Step 1: Process data
    result = process(input_data)
    
    # Step 2: Generate output
    output_data = {"result": result, "status": "ok"}
    
    save(output_data)


if __name__ == "__main__":
    my_feature_main()
```

### Key Points
- **Function name matches module** - `01_my_feature.py` → `my_feature_main()`
- **No docstrings needed** - code speaks for itself
- **Use `load()` and `save()`** - handles paths automatically
- **Step comments** - mark logical sections

---

## Test Tools (`test_tools.py`)

### Basic Functions

**`load(filename="data.json", input_data_path=None)`**
- Searches in priority order:
  1. `data_input_local/{package}/{module}/{filename}` (your overrides)
  2. `data_input/{package}/{module}/{filename}` (standard)
  3. `--input-data` CLI argument (JSON string)

**`save(data, filename=None, save_data_path=None)`**
- Auto-generates path: `data_output/{package}_{module}_{timestamp}.json`
- Uses `--output` CLI arg if provided, else module name

### Path Priority

```
Load Priority:
  data_input_local/  ← Your modifications (overrides everything)
        ↓
  data_input/        ← Standard inputs (git tracked)
        ↓
  --input-data       ← CLI JSON string (fallback)

Save Location:
  data_output/       ← Auto-generated with timestamp
```

### CLI Arguments

```bash
# Use JSON string input
python example.py --input-data '{"key": "value"}'

# Custom output filename
python example.py --output my_result

# Combined
python example.py --input-data '{"test": 1}' --output result
```

---

## Integration & Unit Tests

### Integration Tests
Verify examples produce expected outputs. Use `pytest` to run examples and compare results.

```python
# tests/integrations/test_example_01.py
def test_example_output():
    # Run example and verify output structure
    pass
```

### Unit Tests
Test individual functions with edge cases.

```python
# tests/unittests/test_feature.py
def test_function_edge_case():
    # Test boundary conditions
    pass
```

Keep tests simple and focused. Detailed patterns available in code examples.

---

## Key Principles

1. **KISS** - Simple code over clever code
2. **Let it fail** - Don't over-validate, let natural errors show
3. **Modularity** - Small functions, clear purposes
4. **Determinism** - Reproducible results with seeds/mocks
