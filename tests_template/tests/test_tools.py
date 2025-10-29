"""
Shared testing utilities

Provides basic file operations for test data under tests/data/
Auto-detects caller module for smart input/output paths
"""

import inspect
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Tuple


# Module level anchor to tests directory
TESTS_ROOT = Path(__file__).parent
DATA_DIR = TESTS_ROOT / "data"


def _get_caller_info() -> Tuple[str, str]:
    """
    Get caller module info from call stack
    
    Returns:
        (package_name, module_name) e.g., ("examples", "01_basic_example")
    """
    frame = inspect.currentframe()
    caller_frame = frame.f_back.f_back
    caller_file = caller_frame.f_globals.get("__file__", "")
    
    caller_path = Path(caller_file)
    module_name = caller_path.stem
    
    package_name = caller_path.parent.name
    
    return package_name, module_name


def _get_input_path(filename: str) -> Path:
    """
    Get input file path with input_local override support
    
    Priority:
    1. tests/data/input_local/{package}/{module}/{filename}
    2. tests/data/input/{package}/{module}/{filename}
    """
    package_name, module_name = _get_caller_info()
    
    local_path = DATA_DIR / "input_local" / package_name / module_name / filename
    if local_path.exists():
        return local_path
    
    return DATA_DIR / "input" / package_name / module_name / filename


def _get_output_path(filename: str) -> Path:
    """
    Generate output file path with timestamp
    
    Format: tests/data/output/{package}_{module}_{timestamp}.json
    """
    package_name, module_name = _get_caller_info()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    base_name = Path(filename).stem
    ext = Path(filename).suffix or ".json"
    
    output_filename = f"{package_name}_{module_name}_{timestamp}{ext}"
    return DATA_DIR / "output" / output_filename


def load(filename: str = "data.json", input_data_path: str = None) -> Any:
    """
    Load JSON from tests/data/input/{package}/{module}/
    Falls back to input_local if exists
    
    Args:
        filename: File name under module's input directory (default: "data.json")
        input_data_path: Manual override path (absolute or relative to DATA_DIR)
    """
    if input_data_path:
        filepath = Path(input_data_path) if Path(input_data_path).is_absolute() else DATA_DIR / input_data_path
    else:
        filepath = _get_input_path(filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data: Any, filename: str = "data.json", save_data_path: str = None) -> None:
    """
    Save JSON to tests/data/output/ with auto-generated name
    
    Args:
        data: Data to save
        filename: Base filename for auto-generated path (default: "data.json")
        save_data_path: Manual override path (absolute or relative to DATA_DIR)
    """
    if save_data_path:
        filepath = Path(save_data_path) if Path(save_data_path).is_absolute() else DATA_DIR / save_data_path
    else:
        filepath = _get_output_path(filename)
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
