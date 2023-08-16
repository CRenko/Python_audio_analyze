
from scipy.io import wavfile
import matplotlib.pyplot as plt
from Timefeature import *
import numpy as np

fs, data = wavfile.read('恋音と雨空鼓点.wav')

inc = 1000
# 窗口长度
wlen = 1000
# 取一个长度为wlen的汉明窗
win = w = np.hanning(wlen)
# 实际数据的总长度
N = len(data)
# 用窗口分割后的数据总长度
time = [i / fs for i in range(N)]
# 短时能量数组
EN = STEn(data[:, 0], wlen, inc)

frameTime = FrameTimeC(len(EN), wlen, inc, fs)
a = frameTime[EN > (np.max(EN) * 0.4)]
data = open("data.txt", 'w+')

# value设置阈值,name设置导出的数据的组名
value = 0.3
name = "\"song1\""
# 最小有效短时能量
minEN = np.max(EN) * value
start = EN[0]

count = 0
n = 1
print("{%s:[" % (name), file=data)
for en in EN:
    if en >= minEN:
        count += 1
    elif count < 5:
        start = en
        count = 0
    else:
        print("{\"time\":%.1ff, \"length\":%d, \"track\":%d}," % (frameTime[np.where(EN==start)], 1 + (count - 5) // 5, n),
              file=data)
        n += 1
        if n > 6:
            n = 1

print("]}", file=data)
data.close()

# 画图的
# fig = plt.figure(figsize=(40, 10))
#
# plt.subplot(1, 1, 1)
# plt.plot(frameTime, EN)
# plt.savefig('energy.png')
