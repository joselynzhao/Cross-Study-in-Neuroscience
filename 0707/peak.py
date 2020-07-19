'''
@Author: y@yml.red
@Date: 2020-07-13 18:56:24
@LastEditTime: 2020-07-14 08:32:07
@FilePath: \zj\mountains.py
@Description: index of mountains
'''
# %%

file_No = '003'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fftpack
data = pd.read_csv('samples-'+file_No+'.txt', '\t', header=None, names=['a', 'b', 'c'])
data.head()
# %%


def plot(xs):
    plt.figure(figsize=(20, 3))
    plt.axvline(1000, lw=0.1)
    for i, x in enumerate(xs):
        plt.plot(x, lw=0.1, label=i)
    plt.legend()

# %%
x = data['c']
plot([x])
# %%
# window_length:窗口大小，太大会导致峰值迟滞，太小起不到平滑的作用
# polyorder: 越高阶越平滑
xs = signal.savgol_filter(x, window_length=333, polyorder=3)
# height: 波峰的最小高度
# distance: 波峰之间的最小距离
peaks, _ = signal.find_peaks(x, height=1.35, distance=50)
left = np.zeros_like(peaks, dtype='int')
right = np.zeros_like(peaks, dtype='int')

threshold = 300 # 波峰的最小宽度/2
for i, idx in enumerate(peaks):
    j = idx - threshold
    while xs[j] < xs[j+1]:
        j -= 1
    left[i] = j
    j = idx + threshold
    while xs[j] < xs[j-1]:
        j += 1

    right[i] = j

plt.figure(figsize=(20, 3))
for i, idx in enumerate(peaks):
    # plt.axvline(idx, lw=0.1, c='red')
    plt.axvline(left[i], lw=0.1, c='green')
    plt.axvline(right[i], lw=0.1, c='blue')


plt.plot(x, lw=0.1, label='raw')
plt.plot(xs, lw=0.1, label='smooth')
plt.legend(loc='upper left')
plt.show()
# %%
pd.DataFrame([left,right]).transpose().to_csv('peak-'+file_No+'.txt',sep=' ',header=None,index=None)

# %%
