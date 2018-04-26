#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 18:02
# @Author  : HT
# @Site    : 
# @File    : DBManager.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

import pymongo

from pymongo.errors import DuplicateKeyError
import os, sys
ROOT_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.pardir)
sys.path.append(ROOT_PATH)
from taobao_scrapy.BaseModule.Configloader import Configloader
from taobao_scrapy.BaseModule.SignalRegister import SignalRegister
class DBManager(object):
    def __init__(self):
        try:
            # Python 3.x
            from urllib.parse import quote_plus
        except ImportError:
            # Python 2.x
            from urllib import quote_plus

        configloader = Configloader()
        uri = "mongodb://%s:%s@%s" % (quote_plus(configloader.mongodb_user()), quote_plus(configloader.mongodb_password()), configloader.mongodb_host())
        self.mgdbManager = pymongo.MongoClient(uri)
        self.db = self.mgdbManager.taobao

        self.category_info_list = []
        self.data_list = []
        self.spu_list = []
        SignalRegister.registe(self.handle_signal)

        if self.db.taobao_item.count() is 0:
            self.db.taobao_item.create_index([("insert_time",pymongo.ASCENDING)])
        if self.db.taobao_crawl_log.count() is 0:
            self.db.taobao_crawl_log.create_index([("insert_time",pymongo.ASCENDING)])
        if self.db.taobao_spu.count() is 0:
            self.db.taobao_spu.create_index([("insert_time",pymongo.ASCENDING)])

    def insert_category_info(self, obj):
        print('mongodb 正在处理 category_info 数据 len:{}'.format(len(obj)))
        print('category_info len:{}'.format(len(self.category_info_list)))
        self.category_info_list.append(obj)
        if len(self.category_info_list) > 50:
            self.db.taobao_crawl_log.insert_many(self.category_info_list)
            del self.category_info_list[:]

    def insert_data_list(self, objs):
        print('mongodb 正在处理 data_list 数据 len:{}'.format(len(objs)))

        print('data_list len:{}'.format(len(self.data_list)))
        self.data_list.extend(objs)
        if len(self.data_list) >= 2000:
            try:
                #去重
                # for data in range(len(self.data_list)):

                self.db.taobao_item.insert_many(self.data_list)
            except DuplicateKeyError as error:
                print('data_list数据操作报错 有重复的nid error_info:{}'.format(error))
            except Exception as error:
                print('data_list数据操作报错 error_info:{}'.format(error))
            finally:
                del self.data_list[:]

    def insert_spu_list(self, objs):
        print('mongodb 正在处理 spu_list数据 len:{}'.format(len(objs)))
        print('spu_list len:{}'.format(len(self.spu_list)))
        self.spu_list.extend(objs)
        if len(self.spu_list) >= 500 :
            try:
                self.db.taobao_spu.insert_many(self.spu_list)
            except DuplicateKeyError as error:
                print('spu数据操作报错 有重复的nid error_info:{}'.format(error))
            except Exception as error:
                print('spu数据操作报错 error_info:{}'.format(error))
            finally:
                del self.spu_list[:]

    def handle_signal(self, signum, frame):
        print('处理信号')
        try:
            self.db.taobao_spu.insert_many(self.spu_list)
        finally:
            del self.spu_list[:]
        try:
            self.db.taobao_crawl_log.insert_many(self.category_info_list)
        finally:
            del self.category_info_list[:]
        try:
            self.db.taobao_item.insert_many(self.data_list)
        finally:
            del self.data_list[:]
        quit()

if __name__ == '__main__':
    db = DBManager()
    records = db.db.taobao_category.find()
    count = 0
    for record in records:
        c_i = record.get('category_info')
        page_name = record.get('page_name')
        if page_name == 'spulist':
            if c_i:
                count += c_i.get('totalCount')

    print(count)
