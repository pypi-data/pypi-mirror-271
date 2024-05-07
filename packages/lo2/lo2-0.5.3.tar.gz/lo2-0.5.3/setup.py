#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Setup script.

Authors: zhangte01(zhangte01@baidu.com)
Date:    2024/03/26 18:54:14
"""
from setuptools import setup, find_packages

try:
   import pypandoc
   README = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
   README = open('README.md').read()

setup(
    name='lo2',
    version='0.5.3',
    #url='none',
    author='DUHP BSP Team',
    author_email='zhangte01@baidu.com',
    description='lo2 - Log Oracle, an Oracle test language for log description and analysis',
    long_description_content_type="text/markdown",
    long_description=README,
    packages=find_packages(),    
    install_requires=[
                        "Jinja2==3.1.2",
                        "ply>=3",
                        "chardet>=2.0",
                        "matplotlib>=3.5",
                    ],
)
