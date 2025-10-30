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

## Naming Conventions

### File Names
- Example files: `example_{feature}.py`
- Function name: `{feature}_main()`
- Input template: `data_input/example_{feature}.json.template`
- Local input: `data_input_local/example_{feature}.json`
- Output: `data_output/example_{feature}_{timestamp}.json`

### Test Data
- Templates use `.json.template` suffix (git tracked, empty values)
- Local files use `.json` (git ignored, actual values)
- All JSON use 2-space indentation
- Keep data minimal and focused
- No sensitive data in templates

---

## Directory Structure

```
tests/
├── data_input/              # Git-tracked standard inputs
│   └── {module}.json        # Input templates (use .template suffix)
├── data_input_local/        # Your local input overrides (not tracked)
│   └── {module}.json        # Your modified inputs
├── data_output/             # Auto-generated outputs (not tracked)
│   └── {module}_{timestamp}.json
├── examples/                # Runnable demos
├── integrations/            # Integration tests
├── unittests/               # Unit tests
└── test_tools.py            # Shared utilities
```

---

## Example Template

Minimal structure for `examples/example_feature.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.test_tools import load, save


def feature_main():
    input_data = load()
    
    # Step 1: Process data
    result = process(input_data)
    
    # Step 2: Generate output
    output_data = {"result": result}
    
    save(output_data)


if __name__ == "__main__":
    feature_main()
```

### Input Template

Create `data_input/example_feature.json.template`:

```json
{
  "param1": "",
  "param2": ""
}
```

### Key Points
- **Function name matches module** - `example_feature.py` → `feature_main()`
- **No docstrings needed** - code speaks for itself
- **Use `load()` and `save()`** - handles paths automatically
- **Step comments** - mark logical sections
- **No logging** - keep examples simple and fast

---

## Test Tools (`test_tools.py`)

### Basic Functions

**`load(filename="data.json", input_data_path=None)`**
- Searches in priority order:
  1. `data_input_local/{module}.json` (your overrides)
  2. `data_input/{module}.json` (standard)
  3. `--input-data` CLI argument (JSON string)

**`save(data, filename=None, save_data_path=None)`**
- Auto-generates path: `data_output/{module}_{timestamp}.json`
- Uses `--output` CLI arg if provided, else module name

### Path Priority

```
Load Priority:
  data_input_local/{module}.json  ← Your modifications (overrides everything)
        ↓
  data_input/{module}.json        ← Standard inputs (git tracked)
        ↓
  --input-data                    ← CLI JSON string (fallback)

Save Location:
  data_output/{module}_{timestamp}.json  ← Auto-generated with timestamp
```

### CLI Arguments

```bash
# Use JSON string input
python tests/examples/example_feature.py --input-data '{"key": "value"}'

# Custom output filename
python tests/examples/example_feature.py --output my_result

# Combined
python tests/examples/example_feature.py --input-data '{"test": 1}' --output result
```

### Setup Workflow

```bash
# 1. Copy template to local
cp tests/data_input/example_feature.json.template tests/data_input_local/example_feature.json

# 2. Edit local file with actual values
# vim/nano/editor tests/data_input_local/example_feature.json

# 3. Run example
python tests/examples/example_feature.py

# 4. Check output
ls tests/data_output/
```

---

## Integration & Unit Tests

### Integration Tests
Verify examples produce expected outputs. Use `pytest` to run examples and compare results.

```python
# tests/integrations/test_example_feature.py
def test_feature_output():
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

Keep tests simple and focused.

---

## Key Principles

1. **KISS** - Simple code over clever code
2. **Let it fail** - Don't over-validate, let natural errors show
3. **Modularity** - Small functions, clear purposes
4. **Determinism** - Reproducible results with seeds/mocks
