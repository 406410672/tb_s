#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 16:47
# @Author  : HT
# @Site    : 
# @File    : items.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

import scrapy


class TaobaoCategoryItem(scrapy.Item):
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    insert_date = scrapy.Field()


class TaoBaoBaseItem(scrapy.Item):
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    insert_date = scrapy.Field()
    request_url = scrapy.Field()
    page_name = scrapy.Field()
    data_info = scrapy.Field()
    data_list = scrapy.Field()

class TaoBaolistsrpItem(TaoBaoBaseItem):
    pass
    # category_name = scrapy.Field()
    # category_url = scrapy.Field()
    # insert_date = scrapy.Field()
    # page_name = scrapy.Field()
    # data_info = scrapy.Field()
    # data_list = scrapy.Field()


class TaoBaospulistItem(TaoBaoBaseItem):
    pass
    # category_name = scrapy.Field()
    # category_url = scrapy.Field()
    # insert_date = scrapy.Field()
    # page_name = scrapy.Field()
    # data_info = scrapy.Field()
    # data_list = scrapy.Field()


class TaoBaomainsrpItem(TaoBaoBaseItem):
    pass
    # category_name = scrapy.Field()
    # category_url = scrapy.Field()
    # insert_date = scrapy.Field()
    # page_name = scrapy.Field()
    # data_info = scrapy.Field()
    # data_list = scrapy.Field()


class TaoBaospudetailItem(TaoBaoBaseItem):
    # category_name = scrapy.Field()
    category_name_level_2 = scrapy.Field()
    # category_url = scrapy.Field()
    # insert_date = scrapy.Field()
    # page_name = scrapy.Field()
    # data_info = scrapy.Field()
    # data_list = scrapy.Field()


if __name__ == '__main__':
    # item = TaobaoDetailItem()
    # item['content'] =' 23'
    pass