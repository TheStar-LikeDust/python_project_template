# coding: utf-8
import os
import sys

# settings item here

SETTING_ITEM_1 = "test_content"
"""docstring here"""
SETTING_ITEM_2 = "test_content"
"""docstring here"""
SETTING_ITEM_3 = "test_content"
"""docstring here"""

# ============================================
# Dynamic config dictionaries (convention: load via env var __)
# Example: define DSPY_API_KEYS = {}, then in .env:
#          DSPY_API_KEYS__STEP_PREPARE=xxx
#          In code: settings.DSPY_API_KEYS['step_prepare']
# ============================================

ROOT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), *['..' for i in range(2)]))
"""Fixed root path. Change the number in range to adjust the path"""


def _setting_initial(dotenv_path):
    import os
    import dotenv

    # TODO: without dotenv
    dotenv.load_dotenv(dotenv_path=dotenv_path)

    # Load normal configs (vars without __)
    for setting_item_name in globals().keys():
        if setting_item_name.isupper() and '__' not in setting_item_name:
            globals()[setting_item_name] = os.environ.get(setting_item_name, globals().get(setting_item_name))

    # Load dynamic configs (env vars with __)
    for key, value in os.environ.items():
        if '__' in key:
            # DSPY_API_KEYS__STEP_PREPARE -> dict_name='DSPY_API_KEYS', sub_key='STEP_PREPARE'
            dict_name, sub_key = key.split('__', 1)

            # Load if the dict variable exists
            if dict_name in globals() and isinstance(globals()[dict_name], dict):
                # Write both keys: lowercased + original
                globals()[dict_name][sub_key.lower()] = value
                globals()[dict_name][sub_key] = value


# Default action
# 1. load .env
_setting_initial(os.environ.get('ENV_PATH'))

# 2. add root path
sys.path.append(ROOT_PATH)
