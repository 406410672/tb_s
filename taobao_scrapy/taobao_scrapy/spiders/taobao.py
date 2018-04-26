#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 16:43
# @Author  : HT
# @Site    : 
# @File    : taobao.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues
import sys
import os
import scrapy
ROOT_PATH = os.path.join(os.path.realpath(__file__), os.pardir)
sys.path.append(ROOT_PATH)
import re

from lxml import etree
from datetime import datetime
from scrapy.http import Request

from taobao_scrapy.MyItems.items import (TaobaoCategoryItem,
                                         TaoBaolistsrpItem, TaoBaospulistItem, TaoBaomainsrpItem, TaoBaospudetailItem)

from taobao_scrapy.BaseModule.TaobaoParse import TaobaoParse
from taobao_scrapy.BaseModule.HTLogger import HTLogger


class TaobaoSpider(scrapy.Spider):
    name = 'TaobaoSpider'
    allowed_domains = ['taobao.com']
    root_url = 'https://www.taobao.com/markets/tbhome/market-list'
    logger = HTLogger('taobao.log')
    nav_cat_key_set = set()


    def start_requests(self):
        yield Request(self.root_url, self.parse)
        return

    def parse(self, response):
        print(response.url)
        tree = etree.HTML(response.text)
        # x = '//*[text()="家电办公" or text()="手机数码" or text()="护肤彩妆"]'
        # xpath_list = ['//*[text()="家电办公"]', '//*[text()="手机数码"]', '//*[text()="护肤彩妆"]']
        # xpath_list = ['//*[text()="手机数码"]']
        xpath_dict = {'手机数码': '//*[text()="手机数码"]',
                      '家电办公': '//*[text()="家电办公"]',
                      '护肤彩妆': '//*[text()="护肤彩妆"]',
                      }
        xpath_dict = {
            # '手机数码': '//*[text()="手机数码"]',
            #           '家电办公': '//*[text()="家电办公"]',
            # '珠宝配饰' : '//*[text()="珠宝配饰"]',
                      '护肤彩妆': '//*[text()="护肤彩妆"]',
                      }
        for k,v in xpath_dict.items():
            e_tree = tree.xpath(v)
            category_list = list()

            for element in e_tree:
                sub_elements = element.xpath('../ul/li')
                for sub_element in sub_elements:
                    p_category_name = sub_element.xpath('./a/text()')[0]

                    category_names_result = sub_element.xpath('./div/*[@class="category-name"]/text()')
                    category_urls_result = sub_element.xpath('./div/*[@class="category-name"]/@href')

                    for i in range(len(category_urls_result)):
                        category_name = category_names_result[i]
                        url = category_urls_result[i]
                        complate_category_name = '{}:{}:{}'.format(k, p_category_name, category_name)
                        category_list.append({'category_name': complate_category_name, 'category_url': url})
            i = 0
            for category in category_list:
                i += 1
                item = TaobaoCategoryItem()
                c_n = category['category_name']
                c_url = category['category_url']
                insert_date = datetime.now()
                item['category_name'] = c_n
                item['category_url'] = c_url
                item['insert_date'] = insert_date
                yield item
                url = 'https:' + c_url
                if 'kuaicai' in url:
                    pass
                else:
                    # test_url = 'https://s.taobao.com/list?spm=a21bo.7723600.8559.21.47bb5ec9LPA7Ds&seller_type=taobao&q=BB%E9%9C%9C&pvid=f329390a-d387-43e6-9f6a-43ea7810f1bc&scm=1007.11287.5866.100200300000000'
                    # yield Request(url=test_url, callback=self.parse_content, meta={'category_name': c_n, 'category_url':c_url})
                    yield Request(url='https:' + c_url, callback=self.parse_content,
                                  meta={'category_name': c_n, 'category_url': c_url})
                    # if i == 1:
                    #     return

    def parse_content(self, response):
        meta = response.meta
        category_name = meta['category_name']
        category_url = meta['category_url']
        content = response.text
        request_url = response.url
        g_page_config = TaobaoParse.get_page_config(content)
        page_name = g_page_config.get('pageName')
        insert_date = datetime.now()
        data_info = g_page_config.get('mods').get('sortbar').get('data').get('pager')

        if page_name == 'spudetail':
            data_list = g_page_config.get('mods').get('itemlist').get('data').get('auctions')
            item = TaoBaospudetailItem()
            category_name_level_2 = meta.get('category_name_level_2')
            item['category_name_level_2'] = category_name_level_2
            item['category_name'] = category_name
            item['category_url'] = category_url
            item['insert_date'] = insert_date
            item['request_url'] = request_url
            item['page_name'] = page_name
            item['data_info'] = data_info
            item['data_list'] = data_list
            yield item
            if data_info != None:
                page_size = data_info.get('pageSize')
                totalCount = data_info.get('totalCount')
                current_page = data_info.get('currentPage')
                print('category_name:{}'.format(category_name))
                print('category_name_level_2:{}'.format(category_name_level_2))
                print('page_name:{}'.format(page_name))
                print('page_size:{}'.format(page_size))
                print('totalCount:{}'.format(totalCount))
                print('current_page:{}'.format(current_page))
                if int(current_page) * int(page_size) < int(totalCount):
                    og_url = response.url
                    s_value_list = re.findall('&(s=\d*)', og_url)
                    if len(s_value_list) == 0 and int(current_page) == 1:
                        new_url = og_url+'&s=60'
                    else:
                        new_url = og_url.replace(s_value_list[0], 's=%d'%(int(page_size)*int(current_page)))
                    print('新的url:{}'.format(new_url))
                    yield Request(url=new_url, callback=self.parse_content, meta={'category_name': category_name, 'category_url':category_url, 'category_name_level_2': category_name_level_2})

        elif page_name == 'mainsrp':
            data_list = g_page_config.get('mods').get('itemlist').get('data').get('auctions')
            item = TaoBaomainsrpItem()
            item['category_name'] = category_name
            item['category_url'] = category_url
            item['insert_date'] = insert_date
            item['request_url'] = request_url
            item['page_name'] = page_name
            item['data_info'] = data_info
            item['data_list'] = data_list
            yield item

            og_url = response.url
            #先进行分类，再进行分页
            #取sub数量最最大的分类列表
            #判断如果URL中存在key则不进行插入参数

            allow_add_cat = True
            for cat_key in self.nav_cat_key_set:
                if cat_key in og_url:
                    allow_add_cat = False
                    break
            if allow_add_cat == True:
                print('需要添加分类')
                try:
                    nav_category_list = g_page_config.get('mods').get('nav').get('data').get('common')
                    max_category_item = None

                    for nav_category in nav_category_list:
                        if max_category_item == None:
                            max_category_item = nav_category
                        else:
                            if len(max_category_item.get('sub')) < len(nav_category.get('sub')):
                                max_category_item = nav_category
                    if max_category_item != None:
                        max_category_subs = max_category_item.get('sub')
                        for category_sub in max_category_subs:
                            key = category_sub['key']
                            value = category_sub['value']
                            self.nav_cat_key_set.add(key)
                            new_url = og_url+'&{}={}'.format(key, value)
                            print('新的分类url:{}'.format(new_url))
                            print('cat_key_set:{}'.format(self.nav_cat_key_set))
                            yield Request(url=new_url, callback=self.parse_content, meta={'category_name': category_name, 'category_url': category_url})
                    #增加完分类后不进行下面的操作
                    return
                except Exception as error:
                    print('获取分类失败 ：{}'.format(error))

            if data_info != None:
                page_size = data_info.get('pageSize')
                totalCount = data_info.get('totalCount')
                current_page = data_info.get('currentPage')
                print('category_name:{}'.format(category_name))
                print('page_name:{}'.format(page_name))
                print('page_size:{}'.format(page_size))
                print('totalCount:{}'.format(totalCount))
                print('current_page:{}'.format(current_page))
                if int(current_page) * int(page_size) < int(totalCount):
                    og_url = response.url
                    s_value_list = re.findall('&(s=\d*)', og_url)
                    if len(s_value_list) == 0 and int(current_page) == 1:
                        new_url = og_url+'&s=60'
                    else:
                        new_url = og_url.replace(s_value_list[0], 's=%d'%(int(page_size)*int(current_page)))
                    print('新的页面url:{}'.format(new_url))
                    yield Request(url=new_url, callback=self.parse_content, meta={'category_name': category_name, 'category_url':category_url})

        elif page_name == 'listsrp':
            data_list = g_page_config.get('mods').get('itemlist').get('data').get('auctions')
            item = TaoBaolistsrpItem()
            item['category_name'] = category_name
            item['category_url'] = category_url
            item['insert_date'] = insert_date
            item['request_url'] = request_url
            item['page_name'] = page_name
            item['data_info'] = data_info
            item['data_list'] = data_list
            yield item

            og_url = response.url
            #先进行分类，再进行分页
            #取sub数量最最大的分类列表
            #判断如果URL中存在key则不进行插入参数

            allow_add_cat = True
            for cat_key in self.nav_cat_key_set:
                if cat_key in og_url:
                    allow_add_cat = False
                    break
            if allow_add_cat == True:
                print('需要添加分类')
                try:
                    nav_category_list = g_page_config.get('mods').get('nav').get('data').get('common')
                    max_category_item = None

                    for nav_category in nav_category_list:
                        if max_category_item == None:
                            max_category_item = nav_category
                        else:
                            if len(max_category_item.get('sub')) < len(nav_category.get('sub')):
                                max_category_item = nav_category
                    if max_category_item != None:
                        max_category_subs = max_category_item.get('sub')
                        for category_sub in max_category_subs:
                            key = category_sub['key']
                            value = category_sub['value']
                            self.nav_cat_key_set.add(key)
                            new_url = og_url+'&{}={}'.format(key, value)
                            print('新的分类url:{}'.format(new_url))
                            print('cat_key_set:{}'.format(self.nav_cat_key_set))
                            yield Request(url=new_url, callback=self.parse_content, meta={'category_name': category_name, 'category_url': category_url})
                    #增加完分类后不进行下面的操作
                    return
                except Exception as error:
                    print('获取分类失败 ：{}'.format(error))

            if data_info != None:
                page_size = data_info.get('pageSize')
                totalCount = data_info.get('totalCount')
                current_page = data_info.get('currentPage')
                print('category_name:{}'.format(category_name))
                print('page_name:{}'.format(page_name))
                print('page_size:{}'.format(page_size))
                print('totalCount:{}'.format(totalCount))
                print('current_page:{}'.format(current_page))
                if int(current_page) * int(page_size) < int(totalCount):
                    og_url = response.url
                    s_value_list = re.findall('&(s=\d*)', og_url)
                    if len(s_value_list) == 0 and int(current_page) == 1:
                        new_url = og_url+'&s=60'
                    else:
                        new_url = og_url.replace(s_value_list[0], 's=%d'%(int(page_size)*int(current_page)))
                    print('新的页面url:{}'.format(new_url))
                    yield Request(url=new_url, callback=self.parse_content, meta={'category_name': category_name, 'category_url':category_url})


        elif page_name == 'spulist':
            data_list = g_page_config.get('mods').get('grid').get('data').get('spus')
            item = TaoBaospulistItem()
            item['category_name'] = category_name
            item['category_url'] = category_url
            item['insert_date'] = insert_date
            item['request_url'] = request_url
            item['page_name'] = page_name
            item['data_info'] = data_info
            item['data_list'] = data_list
            yield item
            #请求spu下的所有分页
            if data_info != None:
                page_size = data_info.get('pageSize')
                totalCount = data_info.get('totalCount')
                current_page = data_info.get('currentPage')
                print('category_name:{}'.format(category_name))
                print('page_name:{}'.format(page_name))
                print('page_size:{}'.format(page_size))
                print('totalCount:{}'.format(totalCount))
                print('current_page:{}'.format(current_page))
                if int(current_page) * int(page_size) < int(totalCount):
                    og_url = response.url
                    s_value_list = re.findall('&(s=\d*)', og_url)
                    if len(s_value_list) == 0 and int(current_page) == 1:
                        new_url = og_url+'&s=50'
                    else:
                        new_url = og_url.replace(s_value_list[0], 's=%d'%(int(page_size)*int(current_page)))
                    print('新的分页url:{}'.format(new_url))
                    yield Request(url=new_url, callback=self.parse_content, meta={'category_name': category_name, 'category_url':category_url})
            #每个产品下的所有销售
            for data in data_list:
                new_url = data.get('url')
                new_url = 'https:'+new_url
                print('spulist 下的新请求的url:{}'.format(new_url))
                yield Request(url=new_url, callback=self.parse_content, meta={'category_name': category_name,'category_name_level_2': data.get('title'), 'category_url':category_url})
        return
