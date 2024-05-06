# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     selenium_exception.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/28
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
import typing as t
from functools import wraps
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from web_ui_helper.common.log import logger


class ElementFindException(object):

    def __init__(self, is_ignore: bool = True, is_log_output: bool = True) -> None:
        self.__is_ignore = is_ignore
        self.__is_log_output = is_log_output

    def __call__(self, func: t.Callable) -> t.Any:
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except (NoSuchElementException,):
                if self.__is_log_output is True:
                    logger.error("Element Not Found")
                if self.__is_ignore is False:
                    raise NoSuchElementException()
            except (TimeoutException,):
                if self.__is_log_output is True:
                    logger.error("Element found timeout")
                if self.__is_ignore is False:
                    raise TimeoutException()
            except Exception as e:
                if self.__is_log_output is True:
                    logger.error(e)
                if self.__is_ignore is False:
                    raise OverflowError("Element found failed, reason: {}".format(e))

        return wrapper


def element_find_exception(func: t.Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_ignore = kwargs.pop('is_ignore', True)
        is_log_output = kwargs.pop('is_log_output', True)
        try:
            result = func(*args, **kwargs)
            return result
        except (NoSuchElementException,):
            if is_log_output is True:
                logger.error("Element Not Found")
            if is_ignore is False:
                raise NoSuchElementException()
        except (TimeoutException,):
            if is_log_output is True:
                logger.error("Element found timeout")
            if is_ignore is False:
                raise TimeoutException()
        except Exception as e:
            if is_log_output is True:
                logger.error(e)
            if is_ignore is False:
                raise OverflowError("Element found failed, reason: {}".format(e))

    return wrapper


def loop_find_element(func: t.Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = kwargs.pop('loop', 3)
        interval = kwargs.pop('interval', 0)
        is_ignore = kwargs.pop('is_ignore', True)
        is_log_output = kwargs.pop('is_log_output', True)
        result = None
        for i in range(loop):
            try:
                result = func(*args, **kwargs)
                if result:
                    break
            except (NoSuchElementException,):
                if is_log_output is True:
                    logger.error("Element Not Found")
                if is_ignore is False:
                    raise NoSuchElementException()
            except (TimeoutException,):
                if is_log_output is True:
                    logger.error("Element found timeout")
                if is_ignore is False:
                    raise TimeoutException()
            except Exception as e:
                if is_log_output is True:
                    logger.error(e)
                if is_ignore is False:
                    raise OverflowError("Element found failed, reason: {}".format(e))
            if interval > 0:
                time.sleep(interval)
        return result

    return wrapper
