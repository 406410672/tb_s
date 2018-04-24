#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 16:50
# @Author  : HT
# @Site    : 
# @File    : entrypoint.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

import sys

from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'TaobaoSpider'])

