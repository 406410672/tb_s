from multiprocessing import Process
import os
from multiprocessing import Pool

# 子进程要执行的代码


import re
import json
import requests
# file = open('price.html')
# content = file.read()
from taobao_scrapy.BaseModule.TaobaoParse import TaobaoItemDetailParse

def get_field_name(regex, content):
    result = re.findall(regex, content)
    if len(result) > 0:
        return result[0]
    else:
        return ''

def convert_unicodestr2str(str):
    return str.encode('latin-1').decode('unicode_escape')

def get_item_config(html):
    g_config = re.findall(r'g_config =([\s\S]*?};)', html)
    valItemInfo = re.findall(r'valItemInfo\s*:([\s\S]*?)}\);', html)

    item_config = dict()
    if len(g_config) > 0:
        content = g_config[0]

        sibUrl = re.findall(r"sibUrl\s*?:\s'(.*)',", content)[0]

        descUrl = get_field_name(r"descUrl\s*?:\s(.*)',", content)
        counterApi = get_field_name(r"counterApi\s*:\s'(.*)',", content)
        rateCounterApi = get_field_name(r"rateCounterApi\s*:\s'(.*)',", content)
        shopName = get_field_name(r"shopName\s*?:\s'(.*)',", content)
        shopName = convert_unicodestr2str(shopName)
        title = get_field_name(r"title\s*?:\s'(.*)',", content)
        title = convert_unicodestr2str(title)
        itemId = get_field_name(r"itemId\s*?:\s'(.*)',", content)

        item_config['descUrl'] = descUrl
        item_config['counterApi'] = counterApi
        item_config['rateCounterApi'] = rateCounterApi
        item_config['shopName'] = shopName
        item_config['title'] = title
        item_config['itemId'] = itemId
    if len(valItemInfo) > 0:
        content = valItemInfo[0]
        skuMap = get_field_name(r"skuMap\s*:\s(.*)", content)
        propertyMemoMap = get_field_name(r"propertyMemoMap[\s\S]*:\s(.*)", content)
        item_config['skuMap'] = json.loads(skuMap)
        item_config['propertyMemoMap'] = json.loads(propertyMemoMap)
    return item_config

def get_item_info(content, config):
    pass

# item_config = get_item_config(content)
#
# print(json.dumps(item_config))


if __name__ == '__main__':
    # print(os.path.realpath(os.path.dirname(__file__)))
    files = os.listdir('..\..\web')
    print(len(files))
    for file_name in files:
        print(file_name)
        # if file_name == '14335602945':
        #     filer = open(os.path.join('..\..\web', file_name), encoding='unicode_escape')
        #     content = filer.read()
        #     # print(content)
        #     # print(content)
        #     result = TaobaoItemDetailParse.get_item_config(content)
        #     print(json.dumps(result))
        #     break
        file_name = '14653435847'
        filer = open(os.path.join('..\..\web', file_name), encoding='unicode_escape')
        content = filer.read()
        # print(content)
        # print(content)
        result = TaobaoItemDetailParse.get_item_config(content)
        print(json.dumps(result))
        # print(content)
        break