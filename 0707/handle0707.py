#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:handle0707.py
@TIME:2020/7/7 20:29
@DES:
'''

import matplotlib.pyplot as plt
from scipy import signal

import numpy as np
file = open('samples.txt','r')
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
CaB = data_array[:,1]
Ca = data_array[:,2]
# EMG = data_array[:,4]
# EEG = data_array[:,5]

bo=[(1,4),(5,7),(8,10),(12,18),(21,27),(34,46),(70,90)]
range = [0,-1]

plt.figure(figsize=(40,3),dpi=300)
plt.plot(time[range[0]:range[1]],CaB[range[0]:range[1]])
plt.xlabel(u"Time(S)")
plt.title(u"ca")
plt.savefig("cab")
plt.show()