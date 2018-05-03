#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 18:14
# @Author  : HT
# @Site    : 
# @File    : SignalRegister.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues
import signal
import time


class SignalRegister(object):

    @classmethod
    def registe(cls, handler):
        # signal.signal(signal.SIGHUP, handler)  # 1
        signal.signal(signal.SIGINT, handler)  # 2
        # signal.signal(signal.SIGQUIT, handler)  # 3
        # signal.signal(signal.SIGALRM, handler)  # 14
        signal.signal(signal.SIGTERM, handler)  # 15
        # signal.signal(signal.SIGBREAK, handler)  # 15
        # signal.signal(signal.SIGCONT, handler)  # 18


def d(s,a):
    print('signal:%s %s'%(s, a))

if __name__ == '__main__':
    # print(getattr(signal, 'SIGINT'))
    SignalRegister.registe(d)