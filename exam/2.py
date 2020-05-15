#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:2.py
@TIME:2020/5/13 19:52
@DES:
'''
#
bus = list(map(int,input().strip().split(',')))
deng = list(map(int,input().strip().split(',')))
# print(bus)
# print(deng)

# bus = [2,6,9]
# deng = [3,7]

bus.sort()
deng.sort()
near_dist = []
# print(bus)
# print(deng)

for b in bus:
    dist = [abs(b-d) for d in deng]
    near_dist.append(min(dist))

print(max(near_dist))


