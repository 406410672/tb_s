from multiprocessing import Process
import os
from multiprocessing import Pool

# 子进程要执行的代码
from gevent import monkey; monkey.patch_socket()
import gevent
import requests
import urllib.request

def f(url):
    print('GET: %s' % url)
    resp = requests.get(url)
    data = resp.text
    print('%d bytes received from %s.' % (len(data), url))

# f('https://www.python.org/')
gevent.joinall([
        gevent.spawn(f, 'https://www.python.org/'),
        gevent.spawn(f, 'https://www.yahoo.com/'),
        gevent.spawn(f, 'https://www.baidu.com/'),
])
