#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/7 10:30
# @Author  : HT
# @Site    : 
# @File    : w.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues
from scrapy.utils.project import get_project_settings
#
settings = get_project_settings()
# print(dir(settings))
# print(type(settings))

# for k,v in settings.items():
#     print(k,v)
import os
# print(os.environ.items())
for k,v in os.environ.items():
    print(k,v)