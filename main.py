#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:main.py
@TIME:2020/5/13 15:34
@DES:
'''
import scipy.io  as scio

import matplotlib.pyplot as plt
import h5py

data = h5py.File("ado_6_2.mat",'r')  #获取的是字典
x = list(data.keys())
# print(type(data))
# one = data[x[0]]
# data2 = [data[element[0]][:] for element in data[x]]
# m = scio.loadmat("ado_6_2.mat")
# print(data2)
# print(y)
# print(data)
# data.visit(data[x[0]])
def prtname(name):
    print(name)


data.visit(prtname)
ca1 = data['Ca']['values']
eeg = data['EEG']['values']
emg = data['EMG']['values']
time = data['Keyboard']['times']
# print(ca1.value

plt.figure()
plt.plot(time[:100],ca1[:100])
plt.show()