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

# import numpy as np
# import pandas as pd
#from pandas import Series,DataFrame
# import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
# %%

#
# def plot(xs):
#     plt.figure(figsize=(80, 3))
#     plt.axvline(1000, lw=0.1)
#     for i, x in enumerate(xs):
#         plt.plot(x, lw=0.1, label=i)
#     plt.legend()
#
# # %%
# x = data['c']
# plot([x])
class peak_fetcher():
    def __init__(self,time,info,block_len  = 1000):
        self.time = time
        self.info = info
        self.block_len = block_len


    def find_peaks(self,window_length=333, polyorder=2): # 可能会人为的peak割断
        peaks = []
        total_num = len(self.info)
        for i in range(int(total_num/self.block_len)):
            x = self.time[i*self.block_len:(i+1)*self.block_len]
            y = self.info[i*self.block_len:(i+1)*self.block_len]
            peaks_x, peaks_y = find_peaks(y, distance=100)  # peaks_y 是什么
            peaks_time = x[peaks_x]
            peaks_value = y[peaks_x]
            plt.plot(x, y)
            plt.scatter(peaks_time, peaks_value, marker="x", c="g",label ='Raw data')
            filtered_y = savgol_filter(y,window_length,polyorder)
            filtered_peaks_x, filtered_peaks_y = find_peaks(filtered_y, distance=1)
            filtered_peaks_time = x[filtered_peaks_x]
            filtered_peaks_value = filtered_y[filtered_peaks_x]
            plt.plot(x, filtered_y)
            plt.scatter(filtered_peaks_time, filtered_peaks_value, marker="x", c="r",label='savgol_filter')
            plt.title("savgol_filter(y, {},{})".format(window_length,polyorder))
            plt.savefig('images/savgol_filter(y, {},{})'.format(window_length,polyorder))
            plt.show()
            peaks.append(filtered_peaks_x)
        return peaks

    def find_peak_all(self, window_length=299, polyorder=2,distance = 1,height = 0.61):
        x = self.time
        y  = self.info
        plt.figure(figsize=(80, 3), dpi=300)
        filtered_y = savgol_filter(y, window_length, polyorder)
        filtered_peaks_x, filtered_peaks_y = find_peaks(filtered_y, height=height,distance=distance)
        filtered_peaks_time = x[filtered_peaks_x]
        filtered_peaks_value = filtered_y[filtered_peaks_x]
        line2 = plt.plot(x, filtered_y)
        plt.setp(line2, linewidth=1.0)
        plt.scatter(filtered_peaks_time, filtered_peaks_value, marker="x", c="r", label='savgol_filter')
        plt.title("{}-savgol_filter(y, {},{})".format(file_No,window_length, polyorder))
        plt.savefig('images/{}-savgol_filter(y, {},{})'.format(file_No,window_length, polyorder))
        plt.show()
        return filtered_y, filtered_peaks_x

    def show_raw_data(self):
        x = self.time
        y = self.info
        peaks_x, peaks_y = find_peaks(y, distance=100)  # peaks_y 是什么
        peaks_time = x[peaks_x]
        peaks_value = y[peaks_x]
        plt.figure(figsize=(80, 3), dpi=300)
        line1 = plt.plot(x, y)
        plt.setp(line1, linewidth=1.0)
        plt.scatter(peaks_time, peaks_value, marker="x", c="g", label='Raw data')
        plt.title("{}-raw data".format(file_No))
        plt.savefig('images/{}-raw_data {}'.format(file_No))


    def find_start_end(self,y, peaks):
        left = np.zeros_like(peaks, dtype='int')
        right = np.zeros_like(peaks, dtype='int')
        threshold = 300  # 波峰的最小宽度/2
        for i,idx in enumerate(peaks):
            j = idx-threshold
            while y[j] < y[j + 1]  and j > 0 and j < len(y) - 1:
                j -= 1
            left[i] = j
            j = idx+threshold
            while y[j] < y[j - 1]  and j > 0 and j < len(y) - 1:
                j += 1
            right[i] = j
        plt.figure(figsize=(80, 3), dpi=300)
        for i, idx in enumerate(peaks):
            # plt.axvline(idx, lw=0.1, c='red')
            plt.axvline(left[i], lw=0.1, c='green')
            plt.axvline(right[i], lw=0.1, c='blue')
        # plt.plot(x, lw=0.1, label='raw')
        plt.plot(range(len(y)),y, lw=0.1, label='smooth')
        plt.legend(loc='upper left')
        plt.savefig('seg-{}'.format(file_No))
        plt.show()
        pd.DataFrame([left, right]).transpose().to_csv('peak-' + file_No + '.txt', sep=' ', header=None, index=None)



peaker  = peak_fetcher(data['a'],data['c'])
# peaker.show_raw_data()
filtered_y, peaks = peaker.find_peak_all(window_length=899,distance = 1)
print(len(peaks))
peaker.find_start_end(filtered_y,peaks)
# print(peaker.find_peak_all())
