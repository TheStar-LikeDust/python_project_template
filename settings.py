# coding: utf-8
import os
import sys

# settings item

SETTING_ITEM_1 = "test_content"
"""docstring here"""
SETTING_ITEM_2 = "test_content"
"""docstring here"""
SETTING_ITEM_3 = "test_content"
"""docstring here"""

# end settings item
###################

ROOT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), *['..' for i in range(2)]))
"""Fixed root path. Change the number in range to adjust the path"""


def _setting_initial(dotenv_path):
    # TODO: without dotenv
    import dotenv

    dotenv.load_dotenv(dotenv_path=dotenv_path)

    for setting_item_name in globals().keys():
        if setting_item_name.isupper():
            globals()[setting_item_name] = os.environ.get(setting_item_name, globals().get(setting_item_name))


# 1. auto load env
_setting_initial(os.environ.get('ENV_PATH'))

# 2. root path
sys.path.append(ROOT_PATH)
