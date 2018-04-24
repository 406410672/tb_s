#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 11:08
# @Author  : HT
# @Site    : 
# @File    : t.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

import re

#统计category数据
def count():
    fil = open('items.txt')
    content = fil.read()

    result = re.findall('page_name:([a-zA-Z]*)\s', content)
    # print(result)
    count = {}
    for c_type in result:
        if c_type in count.keys():
            count[c_type] = count[c_type] + 1
        else:
            count[c_type] = 1

    print(count)
    '''
    {'spulist': 36, 'spudetail': 1, 'mainsrp': 38, 'listsrp': 105}
     二级分类                         列表            列表
    '''

def reText():
    dd = '''
    /* 1 */
{
    "_id" : "_id",
    "value" : null
}

/* 2 */
{
    "_id" : "category",
    "value" : null
}

/* 3 */
{
    "_id" : "category_name",
    "value" : null
}

/* 4 */
{
    "_id" : "comment_count",
    "value" : null
}

/* 5 */
{
    "_id" : "comment_url",
    "value" : null
}

/* 6 */
{
    "_id" : "detail_url",
    "value" : null
}

/* 7 */
{
    "_id" : "i2iTags",
    "value" : null
}

/* 8 */
{
    "_id" : "icon",
    "value" : null
}

/* 9 */
{
    "_id" : "insert_time",
    "value" : null
}

/* 10 */
{
    "_id" : "isHideIM",
    "value" : null
}

/* 11 */
{
    "_id" : "isHideNick",
    "value" : null
}

/* 12 */
{
    "_id" : "item_loc",
    "value" : null
}

/* 13 */
{
    "_id" : "nick",
    "value" : null
}

/* 14 */
{
    "_id" : "nid",
    "value" : null
}

/* 15 */
{
    "_id" : "p4p",
    "value" : null
}

/* 16 */
{
    "_id" : "p4pSameHeight",
    "value" : null
}

/* 17 */
{
    "_id" : "p4pTags",
    "value" : null
}

/* 18 */
{
    "_id" : "pic_url",
    "value" : null
}

/* 19 */
{
    "_id" : "pid",
    "value" : null
}

/* 20 */
{
    "_id" : "raw_title",
    "value" : null
}

/* 21 */
{
    "_id" : "risk",
    "value" : null
}

/* 22 */
{
    "_id" : "shopLink",
    "value" : null
}

/* 23 */
{
    "_id" : "shopcard",
    "value" : null
}

/* 24 */
{
    "_id" : "title",
    "value" : null
}

/* 25 */
{
    "_id" : "url",
    "value" : null
}

/* 26 */
{
    "_id" : "user_id",
    "value" : null
}

/* 27 */
{
    "_id" : "view_fee",
    "value" : null
}

/* 28 */
{
    "_id" : "view_price",
    "value" : null
}

/* 29 */
{
    "_id" : "view_sales",
    "value" : null
}'''
    result = re.findall('"_id" : "(.*)",',dd)
    print(len(result))
    print(result)
if __name__ == '__main__':
    # u = '''https://s.taobao.com/list?spm=a217h.1099669.a214da9-static.40.f3xmvy&q=cpu&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&initiative_id=tbindexz_20140904&seller_type=taobao&bcoffset=12&s=60'''
    # print(re.findall('&(s=\d*)', u))
    reText()