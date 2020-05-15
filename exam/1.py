#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:1.py
@TIME:2020/5/13 18:53
@DES:
'''
days = [31,28,31,30,31,30,31,31,30,31,30,31]
def isrunnian(year):
    if (year%4==0 or year%100==0): #???
        return True
    else:
        return False

def get_old_days(y,m,d):
    if isrunnian(y):
        days[1]=29
        # print(days)
    if m==1:
        return d
    else:
        return d+sum(days[:m-1])


def get_day_dist(y1,m1,d1,y2,m2,d2):
    if y1==y2: #同一年
        return get_old_days(y2,m2,d2)-get_old_days(y1,m1,d1)  # 如果往前推算的话，可能出现负数
    if y1<y2: # 最常规的情况
        this_year = 366 if isrunnian(y1) else 365
        days = this_year-get_old_days(y1,m1,d1)
        for year in range(y1+1,y2):
            days += 366 if isrunnian(year) else 365
        days += get_old_days(y2,m2,d2)
        return days
    if y1>y2:
        this_year = 366 if isrunnian(y2) else 365
        days = this_year - get_old_days(y2, m2, d2)
        for year in [y2 + 1, y1]:
            days += 366 if isrunnian(year) else 365
        days += get_old_days(y1, m1, d1)
        return -days


info = input().strip().split('|')
y1,m1,d1,w1 = map(int,info[0].split())
y2,m2,d2 = map(int,info[1].split())
#
# print(y1,m1,d1,w1)
# print(y2,m2,d2)

# y1  = 1980
# m1 = 1
# d1 = 2
# w1 = 5
# y2 = 1980
# m2 = 1
# d2 = 4

# print(get_old_days(1980,2,2))

distance = get_day_dist(y1,m1,d1,y2,m2,d2)
w = (w1+(7+(distance%7)))%7
if w== 0:
    w = 7
print(w)
