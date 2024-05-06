# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     airtest_exception.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/28
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import typing as t
from functools import wraps
from airtest.core.error import *
from web_ui_helper.common.log import logger


def runtime_exception(func: t.Callable):
    """
    airtest测试框架运行时异常
    :param func:
    :return:
    """

    @wraps(func)
    def _deco(*args, **kwargs):
        is_ignore = kwargs.pop('is_ignore', True)
        is_log_output = kwargs.pop('is_log_output', True)
        try:
            result = func(*args, **kwargs)
            return result
        except (AdbError, AdbShellError) as e:
            result = (e.stdout + e.stderr).decode()
            if is_log_output is True:
                logger.error(result)
            if is_ignore is False:
                raise AdbError(stdout=result, stderr=result)
        except AirtestError as e:
            result = e.value
            if is_log_output is True:
                logger.error(result)
            if is_ignore is False:
                raise AirtestError(value=result)
        except DeviceConnectionError as e:
            result = e.DEVICE_CONNECTION_ERROR
            if e.value:
                result = result + ", " + e.value
            if is_log_output is True:
                logger.error(result)
            if is_ignore is False:
                raise DeviceConnectionError(value=result)

    return _deco


def element_find_exception(func: t.Callable):
    """
    airtest测试框架元素查找异常
    :param func:
    :return:
    """

    @wraps(func)
    def _deco(*args, **kwargs):
        is_ignore = kwargs.pop('is_ignore', True)
        is_log_output = kwargs.pop('is_log_output', True)
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            if is_log_output is True:
                logger.error(str(e))
            if is_ignore is False:
                raise Exception(str(e))

    return _deco
