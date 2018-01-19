#-*_coding:utf8-*-
# __author__ = 'k.'
import json
import os
import datetime
import time
import re
import pylab as pl
import xlwt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
effect = 'com.yourpackage.com'
'''读取json配置文件函数'''
def rejson(file):
    with open(file, "r") as f:
        data = json.load(f)
        f.close()
        return data
'''时间控制函数'''
def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec
'''启动指定APP命令'''
def start(file):
    startcmd = rejson(file)['startcmd']
    os.system(startcmd)

'''获取指定数据函数'''
def run(file):
    meminfocmd = rejson(file)['meminfocmd']
    cpuinfocmd1 = rejson(file)['cpuinfocmd']
    str2 = ' "com.yourpackage.com"'
    cpuinfocmd = str(cpuinfocmd1) + str2
    tempinfocmd = rejson(file)['tempinfocmd']
    t = int(rejson(file)['time'])
    second = sleeptime(0, 0, 1)
    temp = []
    cpu = []
    mem = []
    for i in range(t*20):
        time.sleep(second)
        print("本次性能测试共计%s分钟" % t)
        print("第%s秒(第%.2f分钟)：测试中->->->->->->->->->->->->->->->->" % ((i*3+1), ((i*3+1)/60)))
        tempnew = os.popen(tempinfocmd).read()
        temp.append(tempnew)
        cpunew = os.popen(cpuinfocmd).read()
        cpu.append(cpunew)
        memnew = os.popen(meminfocmd).read()
        mem.append(memnew)
    templast = re.findall('temperature: (\d+)', str(temp))
    templast2 = [float(i)*(0.1) for i in templast]
    templast3 = [round(i, 1) for i in templast2]
    m = re.findall('(\d+)+%', str(cpu))
    cpulast = []
    for i in range(len(m)):
        if i%3 == 0:
            cpulast.append(int(m[i]))
    memlast1 = re.findall('TOTAL\s+(\d+)', str(mem))
    memlast2 = [float(i)/2048 for i in memlast1]
    memlast3 = [round(i, 2) for i in memlast2]
    return memlast3, templast3, cpulast
'''画图函数'''
def drawpic(mem,tem,cpu):
    t = datetime.datetime.now()
    tlast = str(t.month) + str(t.day) + \
            str(t.hour) + str(t.minute) + \
            str(t.second) + '_' + str(len(mem)*3)
    fig1 = pl.figure(1)
    xmem = range(1, len(mem)+1)
    xmemlast = [i*3 for i in xmem]
    pl.ylim(min(mem)*(0.5), max(mem)*(1.5))
    pl.plot(xmemlast, mem, 'r')
    pl.scatter(xmemlast, mem, s=10, color='b')
    pl.title('APP内存占比图', fontproperties=font)
    pl.xlabel('时间:(秒)', fontproperties=font)
    pl.ylabel('内存:(MB)', fontproperties=font)
    fig1.savefig('%s_mem%s.png' % (effect, tlast))

    fig2 = pl.figure(2)
    ytemlast = tem
    xtem = range(1, len(mem)+1)
    xtemlast = [i * 3 for i in xtem]
    pl.ylim(min(tem)*(0.5), max(mem)*(1.5))
    pl.plot(xtemlast, ytemlast, 'r')
    pl.title('电池温度图', fontproperties=font)
    pl.xlabel('时间:(秒)', fontproperties=font)
    pl.ylabel('温度:(°C)', fontproperties=font)
    fig2.savefig('%s_tem%s.png' % (effect, tlast))

    fig3 = pl.figure(3)
    ycpulast = cpu
    xcpu = range(1, len(ycpulast)+1)
    xcpulast = [i * 3 for i in xcpu]
    pl.ylim(int(min(cpu)*(0.5)), int(max(cpu)*(1.5)))
    pl.plot(xcpulast, ycpulast, 'r')
    pl.title('CPU占比图', fontproperties=font)
    pl.xlabel('时间:(秒)', fontproperties=font)
    pl.ylabel('CPU:(%)', fontproperties=font)
    fig3.savefig('%s_cpu%s.png' % (effect, tlast))
'''输出Excel文档'''
def wtoexcel(mem, temp, cpu):
    '''将结果写入excel文档'''
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('testresult', cell_overwrite_ok=True)
    '''列名'''
    column0 = [u'memory(MB)', u'temp(°C)', u'CPU(%)']
    '''for循环取出每行对应结果值'''
    t = datetime.datetime.now()
    tlast = str(t.month) + str(t.day) + \
            str(t.hour) + str(t.minute) + \
            str(t.second) + '_' + str(len(mem) * 3)
    for i in range(0, len(column0)):
        sheet1.write(0, i, column0[i])
    for j in range(0, len(mem)):
        sheet1.write(j + 1, 0, mem[j])
    for h in range(0, len(temp)):
        sheet1.write(h + 1, 1, temp[h])
    for k in range(0, len(cpu)):
        sheet1.write(k + 1, 2, cpu[k])
    workbook.save('%s_Result_%s.xls' % (effect, tlast))


if __name__ == '__main__':

    #start('cmd.json')  如果没有手动启动待测apk，则需要运行此函数
    # size_str = os.popen('adb shell wm size').read()
    # print(size_str)
    a = run('cmd.json')
    drawpic(*a)
    wtoexcel(*a)












