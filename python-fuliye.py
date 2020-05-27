#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:python-fuliye.py
@TIME:2020/5/27 15:49
@DES:
'''

import numpy as np
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from scipy import signal

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus'] = False


# 采样点选择1400个，因为设置的信号频率分量最高为600赫兹，根据采样定理知采样频率要大于信号频率2倍，所以这里设置采样频率为1400赫兹（即一秒内有1400个采样点，一样意思的）
x = np.linspace(0, 1, 1400)

# 设置需要采样的信号，频率分量有200，400和600
y = 7 * np.sin(2 * np.pi * 200 * x) + 5 * np.sin(2 * np.pi * 400 * x) + 3 * np.sin(2 * np.pi * 600 * x)

plt.figure()
plt.plot(x, y)


plt.title('原始波形')


b, a = signal.butter(8, [0.2,0.8], 'bandpass')   #配置滤波器 8 表示滤波器的阶数
filtedData = signal.filtfilt(b, a, y)  #data为要过滤的信号

print('len of filtedData is {}'.format(len(filtedData)))




plt.figure()

plt.plot(x[0:50], y[0:50])
plt.title('原始部分波形（前50组样本）')
plt.show()


plt.figure()
plt.plot(x[:50], filtedData[0:50])

plt.title('滤波后效果')


fft_y=fft(y)                          #快速傅里叶变换
print(len(fft_y))  # 变换之后的长度还是1400
print(fft_y[0:5])

N = 1400
x = np.arange(N)  # 频率个数

abs_y = np.abs(fft_y)  # 取复数的绝对值，即复数的模(双边频谱)

angle_y = np.angle(fft_y)  # 取复数的角度
print('len of abs_y :{}'.format(len(abs_y)))
print('len of angel_y :{}'.format(len(angle_y)))

plt.figure()
plt.plot(x, abs_y)
plt.title('双边振幅谱（未归一化）')

plt.figure()
plt.plot(x, angle_y)
plt.title('双边相位谱（未归一化）')
plt.show()


# 将振幅谱进行归一化和取半处理
normalization_y=abs_y/N            #归一化处理（双边频谱）
plt.figure()
plt.plot(x,normalization_y,'g')
plt.title('双边频谱(归一化)',fontsize=9,color='green')
plt.show()

 # 接下来进行取半处理：
half_x = x[range(int(N/2))]                                  #取一半区间
normalization_half_y = normalization_y[range(int(N/2))]      #由于对称性，只取一半区间（单边频谱）
plt.figure()
plt.plot(half_x,normalization_half_y,'b')
plt.title('单边频谱(归一化)',fontsize=9,color='blue')
plt.show()