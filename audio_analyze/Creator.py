from scipy.io import wavfile
import matplotlib.pyplot as plt
from Timefeature import *
import numpy as np

def creator(file):
    fs, datas = wavfile.read(file)
    # 窗口长度
    wlen = 1000
    inc = wlen
    # 取一个长度为wlen的汉明窗
    win = w = np.hanning(wlen)
    # 实际数据的总长度
    N = len(datas)
    # 用窗口分割后的数据总长度
    time = [i / fs for i in range(N)]
    # 短时能量数组
    EN = STEn(datas[:,0], wlen, inc)

    frameTime = FrameTimeC(len(EN), wlen, inc, fs)
    a = frameTime[EN > (np.max(EN) * 0.4)]
    # value设置阈值,name设置导出的数据的组名
    value = 0.3
    name = "\""+file+"\""
    # 最小有效短时能量
    minEN = np.max(EN) * value
    printers = []
    start = EN[0]
    count = 0
    doubles = 0
    n = 1
    for en in EN:
        if en >= minEN:
            count += 1
            if en >= minEN * (5.0 / 3):
                doubles += 1
        elif count < 5:
            start = en
            count = 0
        elif doubles <= count / 2:
            printers.append([frameTime[np.where(EN == start)], 1 + (count - 5) // 5, n])
            n += 1
            if n > 6:
                n = 1
            count = 0
            start = en
        else:
            printers.append([frameTime[np.where(EN == start)], 1 + (count - 5) // 5, n])
            printers.append([frameTime[np.where(EN == start)], 1 + (count - 5) // 5, 7 - n])
            n += 1
            if n > 6:
                n = 1
            count = 0
            start = en
    data = open("data/data.txt", 'w+')
    print("{%s:[" % name, file=data)
    for printer in printers:
        if printer != printers[-1]:
            print("{\"time\":%.1f, \"length\":%d, \"track\":%d}," % (
                printer[0], printer[1], printer[2]),
                  file=data)
        else:
            print("{\"time\":%.1f, \"length\":%d, \"track\":%d}" % (
                printer[0], printer[1], printer[2]),
                  file=data)

    print("]}", file=data)
    data.close()

# 画图的
# fig = plt.figure(figsize=(40, 10))
#
# plt.subplot(1, 1, 1)
# plt.plot(frameTime, EN)
# plt.savefig('energy.png')
