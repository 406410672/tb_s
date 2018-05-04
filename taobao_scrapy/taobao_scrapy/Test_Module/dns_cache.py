#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 10:19
# @Author  : HT
# @Site    : 
# @File    : dns_cache.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

import socket
# def memory_usage_psutil():
#     # return the memory usage in MB
#     import psutil,os
#     process = psutil.Process(os.getpid())
#     mem = process.memory_info()[0] / float(2 ** 20)
#     return mem
# print(memory_usage_psutil())

import re
re_regex = "&({}=.*)&|&({}=.*)$".format('ppath', 'ppath')

re_regex = "&({}=[^&]*)".format('ppath')
# re_regex = "[t]+"
# url = 'https://s.taobao.com/list?spm=a21bo.7723600.8559.3.6ad85ec9p7NmhF&seller_type=taobao&q=%E5%8D%B8%E5%A6%86&pvid=f329390a-d387-43e6-9f6a-43ea7810f1bc&scm=1007.11287.5866.10020030000000&ppath=20000:34005155;413:800001041;10206993:32072;3364156:3510571;1628059:3259965&s=425&s=42'
url = 'https://s.taobao.com/list?spm=a21bo.7723600.8559.3.6ad85ec9p7NmhF&seller_type=taobao&q=%E5%8D%B8%E5%A6%86&pvid=f329390a-d387-43e6-9f6a-43ea7810f1bc&scm=1007.11287.5866.10020030000000&ppath=20000:34005155;413:800001041;10206993:32072;3364156:3510571;1628059:3259965'


find_parm = re.findall(re_regex, url)
print(len(find_parm))
print(find_parm)
# print(find_parm[0])
# print(url.replace(find_parm,'大腿也得'))