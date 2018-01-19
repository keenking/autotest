# -*- coding: utf-8 -*-
# __author__ = 'k.'

import urllib.request
import os
import socket

file = input('请输入下载文件路径：')
socket.setdefaulttimeout(30)
#
# item = 'http://ustickers.faceu.mobi/effect/5000160_1514011590.zip'
urllist = []
def cbk(a,b,c):
    '''''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per=100.0*a*b/c

    if per>100:
        print('100.00%\n-------已经完成下载-------')
        return
    print('%.2f%%' % per )

with open(file, 'r')as f:
    files = f.readlines()
    for item in files:
        urllist.append(item)
def auto_down(url,filename):
    try:
        urllib.request.urlretrieve(url, filename, cbk)
    except urllib.error.ContentTooShortError:
        print ('Network conditions is not good.Reloading.')
        auto_down(url, filename)

for url in urllist:
    if url.endswith("zip\n"):
        filename = url.split('/')[-1]
        file = str(filename).split('\n')[0]
        dir = os.path.abspath('.')
        work = os.path.join(dir, 'download')
        filelast = work + '\\' +file
        auto_down(url, filelast)


