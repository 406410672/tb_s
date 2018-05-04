import requests

# url = 'https://s.taobao.com/list?spm=a21bo.7723600.8559.3.6ad85ec9p7NmhF&seller_type=taobao&q=%E5%8D%B8%E5%A6%86&pvid=f329390a-d387-43e6-9f6a-43ea7810f1bc&scm=1007.11287.5866.10020030000000&ppath=20000:34005155;413:800001041;10206993:32072;3364156:3510571;1628059:3259965&s=120'
# rseponse = requests.get(url=url)
# print(rseponse.text)

from PIL import Image
import numpy as np
photo = Image.open('yw_1222.jpg')
print(np.array(photo))
print(dir(photo))
import cv2
img = cv2.imread('yw_1222.jpg')
print(img)