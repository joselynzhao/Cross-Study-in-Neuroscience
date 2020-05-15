#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:3.py
@TIME:2020/5/13 20:13
@DES:
'''
#
# num_book = int(input())
# num_reader = int(input())
# requeir_list = []
# for n in range(num_reader):
#     info = list(map(int,input().strip().split()))
#     requeir_list.append(info)
# print(requeir_list)

import numpy as np


num_book = 5
num_reader = 3
requeir_list = [[1, 2], [2], [3, 4]]

def get_max_index(l):
    index = 0
    max = l[0]
    for i in range(1,len(l)):
        if l[i]>max:
            index = i
            max = l[i]
    return index

def updata_remain(num_book,requeir_list):
    temp = []
    for i in range(num_book):
        temp.append(sum(requeir_list[:,i]))
    return temp

# ag_requeir_list = []
for requeir in requeir_list:
    for i in range(1,num_book+1):
        if i not in requeir:
            requeir.insert(i-1,0)
        else:
            requeir[i-1]=1
    # print(requeir)
# print(requeir_list)
requeir_list = np.array(requeir_list)
remain_req = updata_remain(num_book,requeir_list)


satifi_list = np.ones(num_reader)
buy_book = []
while(sum(satifi_list)!=0):
    # print('-----------------')
    # print(requeir_list)
    # print(remain_req)
    # print(satifi_list)

    # print(remain_req)
    index = get_max_index(remain_req)
    buy_book.append(index+1)
    for i in range(num_reader):
        if requeir_list[i][index]==1:
            #需求已满足
            satifi_list[i]=0
            requeir_list[i]= 0
            remain_req = updata_remain(num_book,requeir_list)
    # print(requeir_list)

# print('-----------------')
print(len(buy_book))


