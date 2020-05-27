#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:daitonglvbo.py
@TIME:2020/5/27 16:48
@DES:
'''

import matplotlib.pyplot as plt
from scipy import signal

import numpy as np
file = open('ado_6_2.txt','r')
time = []
ca4 = []
ca3 = []
emg = []
eeg = []
info = file.readlines()
print(len(info))
info = info[int(len(info)*0.08):] # 百分之5-10丢掉
info = info[:20000]
print(len(info))

data_array = []
for line in info:
    data = list(map(float,line.strip().split()))
    data_array.append(data)

data_array = np.array(data_array)
time = data_array[:,0]
ca4 = data_array[:,2]
ca3 = data_array[:,3]
emg = data_array[:,4]
egg = data_array[:,5]

bo=[(1,4),(5,7),(8,10),(12,18),(21,27),(34,46),(70,90)]

def show(data,bo,dataRange=(10000,15000),sf = 512, lvjie = 8, isSource = False):
    '''
    :param dataRange:  数据长度太大，只能取部分数据端进行显示
    :param hzRange:  带通滤波的hz范围
    :param data:   信号
    :return:
    '''
    y = data[dataRange[0]:dataRange[1]]
    x = np.array(range(dataRange[0], dataRange[1]))
    lensubfig=len(bo)+1
    plt.figure(figsize=(15,12))
    plt.suptitle('signal')
    i=1
    plt.subplot(lensubfig,1,i)
    plt.plot(x,y,label='source')
    for wave in bo:
        i+=1
        plt.subplot(lensubfig,1,i)
        w1 = 2 * wave[0] / sf
        w2 = 2 * wave[1] / sf
        b, a = signal.butter(lvjie, [w1, w2], 'bandstop')  # 配置滤波器 8 表示滤波器的阶数
        filtedData = signal.filtfilt(b, a, y)  # data为要过滤的信号
        plt.plot(x, filtedData,label='({}hz-{}hz)'.format(wave[0], wave[1]))
        # plt.title()

    plt.legend()

    plt.show()

show(egg,bo,lvjie=8)


