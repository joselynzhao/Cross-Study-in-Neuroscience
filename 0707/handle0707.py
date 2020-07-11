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
from matplotlib.pyplot import MultipleLocator
import math

import numpy as np
file = open('samples.txt','r')
time = []
ca4 = []
ca3 = []
emg = []
eeg = []
info = file.readlines()
print(len(info))
# info = info[int(len(info)*0.08):] # 百分之5-10丢掉
# info_cut=[2000,11000]
# info = info[info_cut[0]:info_cut[1]]
# print(len(info))


data_array = []
for line in info:
    data = list(map(float,line.strip().split()))
    data_array.append(data)

data_array = np.array(data_array)
time = list(data_array[:,0])
CaB = list(data_array[:,1])
Ca = list(data_array[:,2])
# EMG = data_array[:,4]
# EEG = data_array[:,5]

bo=[(1,4),(5,7),(8,10),(12,18),(21,27),(34,46),(70,90)]
range = [0,-1]

plt.figure(figsize=(40,3),dpi=300)
plt.plot(time[range[0]:range[1]],CaB[range[0]:range[1]])
plt.xlabel(u"Time(S)")
# x_major_locator=MultipleLocator(1)
# plt.xlim(-0.5,25)
plt.xticks(np.arange(time[0],time[info_cut[1]-info_cut[0]-1],0.2))
plt.title(u"cab")
plt.savefig("cab")
plt.show()


print(Ca)


class HANDER():
    def __init__(self):
        pass
    def Amp(self,t1,t2,info):
        left =time.index(t1)
        right = time.index(t2)
        print(left,right)
        max = np.max(info[left:right])
        min = np.min(info[left:right])
        return max-min

    def draw_line(self,t1,t2,info):
        left = time.index(t1)
        right = time.index(t2)
        plt.figure(figsize=(10, 3), dpi=300)
        plt.plot(time[left:right], info[left:right])
        plt.xlabel(u"Time(S)")
        # x_major_locator=MultipleLocator(1)
        # plt.xlim(-0.5,25)
        plt.xticks(np.arange(time[left], time[right], 0.2))
        plt.title(u"cab")
        plt.savefig("baseline")
        plt.show()


class HANDER_index():  # 横坐标就取index
    def __init__(self):
        pass

    def Amp(self, p1, p2, info):
        # left = time.index(t1)
        # right = time.index(t2)
        # print(left, right)
        max = np.max(info[p1:p2])
        min = np.min(info[p1:p2])
        return max - min

    def draw_line(self, t1, t2, info):
        left = time.index(t1)
        right = time.index(t2)
        plt.figure(figsize=(10, 3), dpi=300)
        plt.plot(time[left:right], info[left:right])
        plt.xlabel(u"Time(S)")
        # x_major_locator=MultipleLocator(1)
        # plt.xlim(-0.5,25)
        plt.xticks(np.arange(time[left], time[right], 0.2))
        plt.title(u"cab")
        plt.savefig("baseline")
        plt.show()


hander =  HANDER()
print(hander.Amp(27.3,29,CaB))
hander.draw_line(27,29,CaB)


