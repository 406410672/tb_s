#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 16:46
# @Author  : HT
# @Site    : 
# @File    : pipelines.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues
import sys
import os

ROOT_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.pardir)
sys.path.append(ROOT_PATH)
print(ROOT_PATH)
# sys.path.append(ROOT_PATH)
from datetime import datetime
from taobao_scrapy.MyItems.items import (TaobaoCategoryItem,
                                         TaoBaolistsrpItem, TaoBaospulistItem, TaoBaomainsrpItem, TaoBaospudetailItem)

from DB.DBManager import DBManager


TYPE_LISTSRP = 'TYPE_LISTSRP'
TYPE_SPULIST = 'TYPE_SPULIST'
TYPE_SPUDETAIL = 'TYPE_SPUDETAIL'
TYPE_MAINSRP = 'TYPE_MAINSRP'
class TaobaoScrapyPipeline(object):
    dbmanager = DBManager()

    # fil = open('t.txt', mode='w')
    #
    category_file = open('category.txt', mode='w')
    # items_file = open('items.txt', mode='w')

    def process_item(self, item, spider):
        print('piplelines accept data :{}'.format(type(item)))
        if isinstance(item, TaobaoCategoryItem):
            category_name = item['category_name']
            category_url = item['category_url']
            insert_date = item['insert_date']
            self.category_file.write('category_name:{} url:{} insert_date:{}\n'.format(category_name, category_url, insert_date))
            print('处理商品一级分类')
        elif isinstance(item, TaoBaolistsrpItem):
            self.process_taobao_item(TYPE_LISTSRP, item)

        elif isinstance(item, TaoBaospulistItem):
            self.process_taobao_item(TYPE_SPULIST, item)

        elif isinstance(item, TaoBaomainsrpItem):
            self.process_taobao_item(TYPE_MAINSRP, item)

        elif isinstance(item, TaoBaospudetailItem):
            self.process_taobao_item(TYPE_SPUDETAIL, item)


    def process_taobao_item(self, type, item):
        category_name = item['category_name']
        category_url = item['category_url']
        insert_date = item['insert_date']
        request_url = item['request_url']
        page_name = item['page_name']
        data_info = item['data_info']
        data_list = item['data_list']

        data_info_insert = {
            'category_name': category_name,
            'category_url': category_url,
            'page_name': page_name,
            'category_info': data_info,
            'request_url': request_url
        }
        if type == TYPE_LISTSRP:
            for data_item in data_list:
                data_item['category_name'] = category_name
                data_item['category_url'] = category_url
                data_item['insert_time'] = datetime.now()
                data_item['_id'] = data_item.get('nid')
            self.dbmanager.insert_category_info(data_info_insert)
            self.dbmanager.insert_data_list(data_list)
        elif type == TYPE_MAINSRP:
            self.dbmanager.insert_category_info(data_info_insert)
            self.dbmanager.insert_data_list(data_list)
        elif type == TYPE_SPULIST:
            for data_item in data_list:
                data_item['category_name'] = category_name
                data_item['category_url'] = category_url
                data_item['insert_time'] = datetime.now()
            self.dbmanager.insert_category_info(data_info_insert)
            self.dbmanager.insert_spu_list(data_list)
        elif type == TYPE_SPUDETAIL:
            category_name_level_2 = item['category_name_level_2']
            data_info_insert['category_name_level_2'] = category_name_level_2
            for data_item in data_list:
                data_item['category_name'] = category_name
                data_item['category_url'] = category_url
                data_item['insert_time'] = datetime.now()
                data_item['_id'] = data_item.get('nid')
                data_item['category_name_level_2'] = category_name_level_2
            self.dbmanager.insert_category_info(data_info_insert)
            self.dbmanager.insert_data_list(data_list)
        print('type:{} 数据处理完毕'.format(type))