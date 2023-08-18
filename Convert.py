import io
import numpy as np
import numpy.matlib
from scipy.io import wavfile
import matplotlib.pyplot as plt

def enframe(x,win,inc=None):
    nx = len(x)
    if isinstance(win, list):
        nwin = len(win)
        nlen = nwin  # 帧长=窗长
    elif isinstance(win, int):
        nwin = 1
        nlen = win  # 设置为帧长
    if inc is None:
        inc = nlen
    nf = (nx - nlen + inc) // inc
    frameout = np.zeros((nf, nlen))
    indf = np.multiply(inc, np.array([i for i in range(nf)]))
    for i in range(nf):
        frameout[i, :] = x[indf[i]:indf[i] + nlen]
    if isinstance(win, list):
        frameout = np.multiply(frameout, np.array(win))
    return frameout

def STEn(x, win, inc):
    X = enframe(x, win, inc)
    s = np.multiply(X, X)
    return np.sum(s, axis=1)

def FrameTimeC(frameNum, frameLen, inc, fs):
    ll = np.array([i for i in range(frameNum)])
    return ((ll - 1) * inc + frameLen / 2) / fs

fs,data = wavfile.read('恋音と雨空.wav')

inc = 1000
wlen = 1000                       # 窗口长度
win = w = np.hanning(wlen)        # 取一个长度为wlen的汉明窗
N = len(data)                     # 实际数据的总长度
time = [i / fs for i in range(N)] # 用窗口分割后的数据总长度
EN = STEn(data[:,0], wlen, inc)   # 短时能量数组

frameTime = FrameTimeC(len(EN), wlen, inc, fs)
data=open("data.json",'w+')

value = 0.30                      # value设置阈值
name = "\"song1\""                # name设置导出的数据的组名
print("{%s:[" %(name),file=data)




t = [[EN[i],frameTime[i]] for i in range(len(EN))]     #原始数据列表
A = np.mat(t)                                          #原始数据矩阵
B = np.matlib.rand((2,len(EN)))                        #随机矩阵1
C = B*A                            
D = np.matlib.rand((3,2))                              #随机矩阵2
E = D*C
F = np.matlib.rand((2,200))                            #随机矩阵3
G = E*F                                                #谱面信息矩阵
print(G)



n = 1

def Renko(i):
    global n
    lst = []
    lst1 = []
    while EN[i] >= np.max(EN) * value:
        lst.append(frameTime[i])
        lst1.append(EN[i])
        if i < len(EN)-1:
            i += 1
    if len(lst) >= 5:
        print("{\"time\":%.1f, \"length\":%d, \"track\":%d}," %(lst[0],len(lst)/5,n),file=data)

        
        count = 0
        for j in lst1:
            if j >= np.max(EN) * 0.5:
                count += 1
        if count >= len(lst)/2:
            print("{\"time\":%.1f, \"length\":%d, \"track\":%d}," %(lst[0],len(lst)/5,7-n),file=data)

            
        n += 1
        if n > 6:
            n = 1
    return lst

i = 0

while i < len(EN):
    i += len(Renko(i)) + 1
	  
print("{\"time\":%.1f, \"length\":%d, \"track\":%d}]}" %(frameTime[len(frameTime)-1],0,0),file=data)
data.close()



#画图的
#fig = plt.figure(figsize=(40, 10))

#plt.subplot(1, 1, 1)
#plt.plot(frameTime, EN)
#plt.savefig('Energy.png')
