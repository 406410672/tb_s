#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 17:30
# @Author  : HT
# @Site    : 
# @File    : TaobaoParse.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues
try:
    import platform
    if platform.python_version()[0] == 2:
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
except Exception as error:
    print('setdefaultencoding error:{}'.format(error))

import json, re
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

    # print(category_list)