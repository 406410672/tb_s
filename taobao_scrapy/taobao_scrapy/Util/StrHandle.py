#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/7 15:35
# @Author  : HT
# @Site    : 
# @File    : StrHandle.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

def convert_unicodestr2str(str):
    return str.encode('latin-1').decode('unicode_escape')