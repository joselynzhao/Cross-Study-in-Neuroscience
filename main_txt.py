#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:main_txt.py
@TIME:2020/5/14 10:08
@DES:
'''
import matplotlib.pyplot as plt

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

# print(time)
# print(ca3)
# print(egg)


plt.figure(figsize=(1000,1),dpi=300)
plt.plot(time,ca3,label='Ca',linewidth=0.5)
plt.plot(time,emg,label='EMG',linewidth=0.5)
plt.plot(time,egg,label='EGG',linewidth=0.5)
plt.legend()
plt.show()
plt.savefig('fig_100*1')

