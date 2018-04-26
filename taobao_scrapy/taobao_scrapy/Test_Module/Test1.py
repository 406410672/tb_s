from multiprocessing import Process
import os
from multiprocessing import Pool

# 子进程要执行的代码
from gevent import monkey; monkey.patch_socket()
import gevent
import requests
import urllib.request


d = set()

d.add('123')
d.add('213')
d.add('1rqr')
# print(d)
url = 'www.http213.com'
for d in d:
    print(d in url)