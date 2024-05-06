# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     setup.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/28
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from setuptools import setup, find_packages

setup(
    name='web-ui-helper',
    version='0.0.2',
    description='This is my web ui helper package',
    long_description='This is my web ui helper package',
    author='ckf10000',
    author_email='ckf10000@sina.com',
    url='https://github.com/ckf10000/web-ui-helper',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.20.0',
        'pandas>=2.2.2',
        'blinker>=1.7.0',
        'airtest>=1.3.3',
        'pocoui>=1.0.94',
        'requests>=2.31.0',
        'selenium-wire>=5.1.0',
        'webdriver-manager>=4.0.1',
        'ddddocr>=1.4.11'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
