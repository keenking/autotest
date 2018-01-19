# -*- coding: utf-8 -*-
# __author__ = 'k.'
import re
import json
from PIL import Image, ImageDraw

# file = input('请输入文本文件路径地址：')
file = r'C:\Users\keenking\Desktop\a.txt'
with open(file, 'r') as f:
    b = f.read()
    # print(b)
    # print(b["data"])
    # a = b["data"]["items"]
    # for item in a:
    #     print(item["streamurl"])
    a = re.findall(r'"streamurl":"(.*?)"', b)
    for i in a:
        print(i.replace('\\', ''))