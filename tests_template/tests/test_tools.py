"""
Shared testing utilities

Provides basic file operations with smart paths:
- data_input: Git-tracked standard inputs
- data_input_local: User-modified inputs (overrides data_input, not tracked)
- data_output: Auto-generated outputs with timestamps

Auto-detects caller module for organized file structure

File Naming Convention:
- Example files: example_{feature}.py
- Function name: {feature}_main()
- Input template: data_input/example_{feature}.json.template
- Local input: data_input_local/example_{feature}.json
- Output: data_output/example_{feature}_{timestamp}.json

Test Data Convention:
- Template files use .json.template suffix (git tracked)
- Template contains empty/placeholder values
- Local files are .json (git ignored, user fills actual values)
- All JSON files use 2-space indentation
- Keep test data minimal and focused
"""

import argparse
import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple


# Module level anchor to tests directory
TESTS_ROOT = Path(__file__).parent
INPUT_DIR = TESTS_ROOT / "data_input"
INPUT_LOCAL_DIR = TESTS_ROOT / "data_input_local"
OUTPUT_DIR = TESTS_ROOT / "data_output"

# Module level argument cache
_parsed_args = None


def _get_cli_args() -> argparse.Namespace:
    """
    Get parsed CLI arguments (cached)
    
    Returns parsed arguments with:
    - input_data: JSON string input
    - output: Output filename
    """
    global _parsed_args
    if _parsed_args is None:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--input-data", type=str, default=None)
        parser.add_argument("--output", type=str, default=None)
        _parsed_args, _ = parser.parse_known_args()
    return _parsed_args


def _get_caller_info() -> str:
    """
    Get caller module name from call stack
    
    Returns:
        module_name e.g., "example_action_studio_login"
    """
    frame = inspect.currentframe()
    caller_frame = frame.f_back.f_back
    caller_file = caller_frame.f_globals.get("__file__", "")
    
    caller_path = Path(caller_file)
    return caller_path.stem


def _get_input_path(filename: str) -> Path:
    """
    Get input file path with input_local override support
    
    Priority:
    1. tests/data_input_local/{module}.json
    2. tests/data_input/{module}.json
    """
    module_name = _get_caller_info()
    
    local_path = INPUT_LOCAL_DIR / f"{module_name}.json"
    if local_path.exists():
        return local_path
    
    return INPUT_DIR / f"{module_name}.json"


def _get_output_path(filename: str) -> Path:
    """
    Generate output file path with timestamp
    
    Format: tests/data_output/{module}_{timestamp}.json
    """
    module_name = _get_caller_info()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    base_name = Path(filename).stem
    ext = Path(filename).suffix or ".json"
    
    output_filename = f"{module_name}_{timestamp}{ext}"
    return OUTPUT_DIR / output_filename


def load(filename: str = "data.json", input_data_path: str = None) -> Any:
    """
    Load JSON with priority:
    1. tests/data_input_local/{module}.json
    2. tests/data_input/{module}.json
    3. --input-data CLI argument (JSON string)
    4. Error if none found
    
    Args:
        filename: Not used, kept for compatibility
        input_data_path: Manual override path (absolute or relative to TESTS_ROOT)
    """
    if input_data_path:
        filepath = Path(input_data_path) if Path(input_data_path).is_absolute() else TESTS_ROOT / input_data_path
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    
    module_name = _get_caller_info()
    local_path = INPUT_LOCAL_DIR / f"{module_name}.json"
    standard_path = INPUT_DIR / f"{module_name}.json"
    
    if local_path.exists():
        with open(local_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    if standard_path.exists():
        with open(standard_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    args = _get_cli_args()
    if args.input_data:
        return json.loads(args.input_data)
    
    raise FileNotFoundError(
        f"No input found:\n"
        f"  - {local_path}\n"
        f"  - {standard_path}\n"
        f"  - --input-data CLI argument"
    )


def save(data: Any, filename: str = None, save_data_path: str = None) -> None:
    """
    Save JSON to tests/data_output/ with auto-generated name
    Uses --output CLI argument if provided, otherwise defaults to module name
    
    Args:
        data: Data to save
        filename: Base filename for auto-generated path (default: None, uses --output or module name)
        save_data_path: Manual override path (absolute or relative to TESTS_ROOT)
    """
    if save_data_path:
        filepath = Path(save_data_path) if Path(save_data_path).is_absolute() else TESTS_ROOT / save_data_path
    else:
        if filename is None:
            args = _get_cli_args()
            if args.output:
                filename = args.output
            else:
                filename = _get_caller_info()
        
        if not filename.endswith('.json'):
            filename = f"{filename}.json"
        
        filepath = _get_output_path(filename)
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
