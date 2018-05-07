#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 17:30
# @Author  : HT
# @Site    : 
# @File    : TaobaoParse.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues
from taobao_scrapy.Util.StrHandle import *
import json, re
from taobao_scrapy.Exceptions.ParserException import TaoBaoItemParserException
from lxml import etree

class TaobaoParse(object):
    @classmethod
    def get_page_config(cls, text):
        '''
        解析 HTML，并且返回一个字典
        :param text:
        :return:
        '''
        assert text is not None and len(text) > 0 ,'text must not None'
        c = re.findall(u'g_page_config = ({.*})', text)[0]
        return json.loads(c)

class TaobaoItemDetailParse(object):

    @classmethod
    def _get_field_name(cls, regex, content):
        result = re.findall(regex, content)
        if len(result) > 0:
            return result[0]
        else:
            return ''

    @classmethod
    def get_item_config(cls, html):
        g_config = re.findall(r'g_config =([\s\S]*?};)', html)
        valItemInfo = re.findall(r'valItemInfo\s*:([\s\S]*?)}\);', html)
        if len(g_config) == 0 and len(valItemInfo) == 0:
            raise TaoBaoItemParserException()

        item_config = dict()
        if len(g_config) > 0:
            content = g_config[0]
            sibUrl = re.findall(r"sibUrl\s*?:\s'(.*)',", content)[0]
            descUrl = cls._get_field_name(r"descUrl\s*?:\s(.*)',", content)
            counterApi = cls._get_field_name(r"counterApi\s*:\s'(.*)',", content)
            rateCounterApi = cls._get_field_name(r"rateCounterApi\s*:\s'(.*)',", content)
            shopName = cls._get_field_name(r"shopName\s*?:\s'(.*)',", content)
            shopName = convert_unicodestr2str(shopName)
            title = cls._get_field_name(r"title\s*?:\s'(.*)',", content)
            title = convert_unicodestr2str(title)
            itemId = cls._get_field_name(r"itemId\s*?:\s'(.*)',", content)
            item_config['descUrl'] = descUrl
            item_config['sibUrl'] = sibUrl
            item_config['counterApi'] = counterApi
            item_config['rateCounterApi'] = rateCounterApi
            item_config['shopName'] = shopName
            item_config['title'] = title
            item_config['itemId'] = itemId

        try:
            if len(valItemInfo) > 0:
                tree = etree.HTML(html)
                content = valItemInfo[0]
                skuMap = cls._get_field_name(r"skuMap\s*:\s(.*)", content)
                skuMap = json.loads(skuMap)
                propertyMemoMap = cls._get_field_name(r"propertyMemoMap[\s\S]*:\s(.*)", content)
                item_config['skuMap'] = skuMap
                item_config['propertyMemoMap'] = json.loads(propertyMemoMap)

                for data_id, info in skuMap.items():
                    try:
                        data_id = data_id.replace(';', '')
                        xpath = '//*[@data-value="{}"]'.format(data_id)
                        elements = tree.xpath(xpath)
                        if len(elements) > 0:
                            element = elements[0]
                            info['title'] = element.xpath('.//span/text()')[0]
                            info['background'] = element.xpath('./a/@style')[0]
                    except Exception as error:
                        print('子类图片与文字解析出错')
                print('有子类')
                print('子类数量,', len(skuMap))
        except Exception as error:
            print('没有子类或者解析出错',error)
        return item_config



if __name__ == '__main__':

    f = open('../../t.txt','r',encoding='utf-8')
    # category_list = []
    # def parser_category():
    #     tree = etree.HTML(f.read())
    #     e_tree = tree.xpath('//*[text()="家电办公" or text()="手机数码" or text()="护肤彩妆"]')
    #
    #     # global category_list = []
    #     for element in e_tree:
    #         sub_elements = element.xpath('../ul/li')
    #         for sub_element in sub_elements:
    #             p_category_name = sub_element.xpath('./a/text()')[0]
    #
    #             category_names_result = sub_element.xpath('./div/*[@class="category-name"]/text()')
    #             category_urls_result = sub_element.xpath('./div/*[@class="category-name"]/@href')
    #
    #             for i in range(len(category_urls_result)):
    #                 category_name = category_names_result[i]
    #                 url = category_urls_result[i]
    #                 complate_category_name = '{}:{}'.format(p_category_name, category_name)
    #                 category_list.append({'category_name': complate_category_name, 'category_url': url})
    #
    #     for item in category_list:
    #         print(item)
    # parser_category()
    # print(len(category_list))
    res = TaobaoParse.get_page_config(f.read())
    print(json.dumps(res))
    from scrapy.command import ScrapyCommand
    # print(category_list)