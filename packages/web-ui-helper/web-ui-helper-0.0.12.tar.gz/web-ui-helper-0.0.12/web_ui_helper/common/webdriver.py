# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     webdriver.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/28
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from selenium.webdriver.common.by import By
from web_ui_helper.common.metaclass import EnumMetaClass


class Locator(EnumMetaClass):
    id = By.ID
    name = By.NAME
    xpath = By.XPATH
    tag_name = By.TAG_NAME
    link_text = By.LINK_TEXT
    class_name = By.CLASS_NAME
    css_selector = By.CSS_SELECTOR
    partial_link_text = By.PARTIAL_LINK_TEXT
