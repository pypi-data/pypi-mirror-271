# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     date_extend.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/29
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from datetime import datetime, timedelta

standard_date_format = "%Y-%m-%d %H:%M:%S"


def get_current_datetime_int_str() -> str:
    current_time = datetime.now()
    # 将当前时间格式化为字符串，精确到毫秒
    time_string = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    return "{}{}{}{}{}{}{}".format(
        time_string[0:4], time_string[5:7], time_string[8:10],
        time_string[11:13], time_string[14:16], time_string[17:19], time_string[20:23]
    )


def get_datetime_area(date_str: str) -> tuple:
    if len(date_str) == 16:
        date_str = "{}:00".format(date_str)
    dt = datetime.strptime(date_str, standard_date_format)
    # 获取当天的0点时间
    first_time = datetime(dt.year, dt.month, dt.day, 0, 0, 0)
    six_time = datetime(dt.year, dt.month, dt.day, 6, 0, 0)
    twelve_time = datetime(dt.year, dt.month, dt.day, 12, 0, 0)
    eighteen_time = datetime(dt.year, dt.month, dt.day, 18, 0, 0)
    # end_time = datetime(dt.year, dt.month, dt.day, 23, 59, 59)
    if first_time <= dt < six_time:
        return 1, "凌晨 0~6点"
    elif six_time <= dt < twelve_time:
        return 2, "上午 6~12点"
    elif twelve_time <= dt < eighteen_time:
        return 3, "下午 12~18点"
    else:
        return 4, "晚上 18~24点"


def iso_to_standard_datestr(datestr: str, time_zone_step: int) -> str:
    """iso(2024-04-21T04:20:00Z)格式转 标准的时间格式(2024-01-01 00:00:00)"""
    dt_str = "{} {}".format(datestr[:10], datestr[11:-1])
    dt = datetime.strptime(dt_str, standard_date_format)
    dt_step = dt + timedelta(hours=time_zone_step)
    return dt_step.strftime(standard_date_format)
