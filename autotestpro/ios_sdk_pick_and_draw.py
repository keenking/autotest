# -*_coding:utf8-*-

import os
import re
import pylab as pl
import xlwt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='C:\Windows\Fonts\simkai.ttf')

def getinfo(file, pattern, pos):
    info = []
    with open(file, 'r') as f:
        for line in f.readlines():
            m = re.search(pattern, line)
            if m:
                info.append((m.group(pos)))
    return info


if __name__ == '__main__':
    path = 'D:\\pycharm_keenking\\autotest\data'
    a = os.listdir(path)
    os.chdir(path)
    for item in a:
        if item.endswith('.txt'):
            effect = re.findall('(.*).txt', item)
            print(effect)
            print(item)
            meminfo1 = getinfo(item, r'.*memoryUseage:(\d+)+\.', 1)
            cpuinfo1 = getinfo(item, r'.*cpuUsage:(\d+)+\s', 1)
            batespinfo1 = getinfo(item, r'.*fps:(\d+)', 1)
            meminfo = []
            for item in meminfo1:
                meminfo.append(int(item))
            cpuinfo = []
            for item in cpuinfo1:
                cpuinfo.append(int(item))
            batespinfo = []
            for item in batespinfo1:
                batespinfo.append(int(item))

            '''将结果写入excel文档'''
            workbook = xlwt.Workbook()
            sheet1 = workbook.add_sheet('testresult', cell_overwrite_ok=True)
            '''列名'''
            column0 = [u'memory(MB)', u'CPU(%)', u'fps']
            '''for循环取出每行对应结果值'''
            for i in range(0, len(column0)):
                sheet1.write(0, i, column0[i])
            for j in range(0, len(meminfo)):
                sheet1.write(j + 1, 0, meminfo[j])
            for h in range(0, len(cpuinfo)):
                sheet1.write(h + 1, 1, cpuinfo[h])
            for k in range(0, len(batespinfo)):
                sheet1.write(k + 1, 2, batespinfo[k])
            workbook.save('%s.xls' % effect)
            fig1 = pl.figure(1)
            xmem = range(1, len(meminfo) + 1)
            xmemlast = [i * 3 for i in xmem]
            pl.ylim(min(meminfo) * (0.5), max(meminfo) * (1.5))
            pl.plot(xmemlast, meminfo, 'r')
            pl.scatter(xmemlast, meminfo, s=10, color='b')
            pl.title('SDK4.0.1内存占比图', fontproperties=font)
            pl.xlabel('时间:(秒)', fontproperties=font)
            pl.ylabel('内存:(MB)', fontproperties=font)
            fig1.savefig('%s_mem.png' % effect)

            fig2 = pl.figure(2)
            ytemlast = cpuinfo
            xtem = range(1, len(cpuinfo) + 1)
            xtemlast = [i * 3 for i in xtem]
            pl.ylim(min(cpuinfo) * (0.5), max(cpuinfo) * (1.5))
            pl.plot(xtemlast, ytemlast, 'r')
            pl.title('SDK4.0.1CPU占比图', fontproperties=font)
            pl.xlabel('时间:(秒)', fontproperties=font)
            pl.ylabel('CPU:(%)', fontproperties=font)
            fig2.savefig('%s_tem.png' % effect)

            fig3 = pl.figure(3)
            ycpulast = batespinfo
            xcpu = range(1, len(ycpulast) + 1)
            xcpulast = [i * 3 for i in xcpu]
            pl.ylim(min(batespinfo) * (0.5), max(batespinfo) * (1.5))
            pl.plot(xcpulast, ycpulast, 'r')
            pl.title('fps图', fontproperties=font)
            pl.xlabel('时间:(秒)', fontproperties=font)
            pl.ylabel('FPS', fontproperties=font)
            fig3.savefig('%s_cpu.png' % effect)
