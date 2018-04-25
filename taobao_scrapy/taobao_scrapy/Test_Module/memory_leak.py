#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 11:25
# @Author  : HT
# @Site    : 
# @File    : memory_leak.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

def memory_usage_psutil():
    # return the memory usage in MB
    import psutil,os
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem
