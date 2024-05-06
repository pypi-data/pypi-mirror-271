# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     ctrip_flight.py
# Description:  解析携程航班
# Author:       mfkifhss2023
# CreateDate:   2024/05/05
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from decimal import Decimal
from selenium import webdriver
from pandas import DataFrame, set_option

from web_ui_helper.common.webdriver import Locator
from web_ui_helper.selenium.frame.browser import get_sub_element

"""
display.max_rows:     设置要显示的最大行数
display.max_columns:  设置要显示的最大列数
display.width:        设置显示的宽度，以字符数为单位
display.precision:    设置浮点数的精度
display.max_colwidth: 设置要显示的列的最大宽度，以字符数为单位
"""

# 设置要显示的最大行数和列数
set_option('display.width', 65535)
set_option('display.max_rows', 50)
set_option('display.max_columns', 1024)
set_option('display.max_colwidth', 100)
# 设置打印格式，使列头和行内容对齐
set_option('display.unicode.east_asian_width', True)


class DesktopFlight:

    @classmethod
    def parse_data(cls, driver: webdriver, elements_data: dict) -> DataFrame:
        index_regx = './/div[@index="{}"]'
        price_regx = './/span[@class="price"]'
        airline_regx = './/div[@class="flight-airline"]/div[@class="airline-name"]'
        plane_no_regx_1 = './/div[@class="plane"]/div[@class="plane"]/span'
        plane_no_regx_2 = './/div[@class="flight-airline"]/div[@class="plane"]'
        depart_time_regx = './/div[@class="depart-box"]/div[@class="time"]'
        depart_airport_regx = './/div[@class="depart-box"]/div[@class="airport"]/span'
        arrive_time_regx = './/div[@class="arrive-box"]/div[@class="time"]'
        arrive_airport_regx = './/div[@class="arrive-box"]/div[@class="airport"]/span'
        columns = [
            "index", "plane_no", "airline", "plane_type", "price", "price_uint",
            "depart_time", "depart_airport", "arrive_time", "cross_days", "arrive_airport"
        ]
        df = DataFrame(columns=columns)
        for index, element in elements_data.items():
            element = driver.find_element(Locator.get("xpath"), index_regx.format(index))
            # print(element.get_attribute('outerHTML'))
            price = get_sub_element(element=element, locator="xpath", regx=price_regx, interval=1, loop=3).text.strip()
            airline = get_sub_element(
                element=element, locator="xpath", regx=airline_regx, interval=1, loop=3
            ).text.strip()
            plane_no = get_sub_element(element=element, locator="xpath", regx=plane_no_regx_1, interval=1, loop=3)
            if plane_no:
                plane_no_slice = plane_no.text.strip().split()
                plane_no = plane_no_slice[0].strip()
                plane_type = plane_no_slice[1].strip()
            else:
                plane_no = element.find_element(Locator.get("xpath"), plane_no_regx_2)
                plane_no = plane_no.get_attribute('id').split("_")[0].split("-")[1].strip()
                plane_type = ""
            depart_time = get_sub_element(
                element=element, locator="xpath", regx=depart_time_regx, interval=1, loop=3
            ).text.strip()
            arrive_time_slice = get_sub_element(
                element=element, locator="xpath", regx=arrive_time_regx, interval=1, loop=3
            ).text.strip().split("\n")
            depart_airport = get_sub_element(
                element=element, locator="xpath", regx=depart_airport_regx, interval=1, loop=3
            ).text.strip()
            arrive_airport = get_sub_element(
                element=element, locator="xpath", regx=arrive_airport_regx, interval=1, loop=3
            ).text.strip()
            # 逐行添加数据
            new_row = dict(
                index=index, airline=airline, plane_no=plane_no, plane_type=plane_type,
                arrive_time=arrive_time_slice[0], cross_days=arrive_time_slice[1] if len(arrive_time_slice) > 1 else "",
                depart_time=depart_time, price=Decimal(price[1:]), price_uint=price[:1], depart_airport=depart_airport,
                arrive_airport=arrive_airport
            )
            # 添加新行数据
            df.loc[len(df)] = new_row
        # 打印DataFrame
        print(df.to_string(justify='left', index=False))
        return df
