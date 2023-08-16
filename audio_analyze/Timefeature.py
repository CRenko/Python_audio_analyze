import numpy as np
from Enframe import enframe

def STEn(x, win, inc):

    X = enframe(x, win, inc)
    s = np.multiply(X, X)
    return np.sum(s, axis=1)

def FrameTimeC(frameNum, frameLen, inc, fs):
    ll = np.array([i for i in range(frameNum)])
    return ((ll - 1) * inc + frameLen / 2) / fs