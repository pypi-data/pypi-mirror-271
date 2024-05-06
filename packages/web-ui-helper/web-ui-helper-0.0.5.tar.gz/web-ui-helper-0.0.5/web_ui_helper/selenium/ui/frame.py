# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     frame.py
# Description:  页面数据框架
# Author:       GIGABYTE
# CreateDate:   2024/04/28
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time

from selenium import webdriver
from web_ui_helper.decorators.selenium_exception import element_find_exception
from web_ui_helper.selenium.frame.browser import scroll_to_bottom, get_elements


class ListFrame(object):

    @classmethod
    @element_find_exception
    def get_all_elements(
            cls, driver: webdriver, url: str, locator: str, regx: str, list_key: str, timeout: int = 1
    ) -> dict:
        """
        爬取页面的主函数
        """
        # 打开网页
        driver.get(url)
        time.sleep(5)
        flag = True
        parsed_data = dict()
        while flag:
            scroll_to_bottom(driver=driver)
            elements = get_elements(driver=driver, locator=locator, regx=regx, timeout=timeout, loop=60)
            new_elements = {element.get_attribute(list_key): element for element in elements if
                            element.get_attribute(list_key) not in list(parsed_data.keys())}
            if new_elements:
                parsed_data.update(new_elements)
            else:
                flag = False
        return parsed_data
