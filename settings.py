# coding: utf-8


# settings item here

SETTING_ITEM_1 = 'test_content'
""""""
SETTING_ITEM_2 = 'test_content'
""""""
SETTING_ITEM_3 = 'test_content'
""""""


def settings_load_env():
    import os
    import dotenv

    dotenv.load_dotenv()

    for setting_item_name in globals().keys():
        if setting_item_name.isupper():
            globals()[setting_item_name] = os.environ.get(setting_item_name, globals().get(setting_item_name))


# auto load
settings_load_env()
