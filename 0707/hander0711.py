import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.pyplot import MultipleLocator
import math
import inspect


# 从堆栈第3层开始查找返回变量名称
def retrieve_name(var):
    for fi in inspect.stack()[2:]:
        for item in fi.frame.f_locals.items():
            if (var is item[1]):
                return item[0]
    return ""


import numpy as np

file = open('samples.txt', 'r')
info = file.readlines()
print(len(info))
# info_cut=[2000,11000]
# info = info[info_cut[0]:info_cut[1]]
# print(len(info))

data_array = []
for line in info:
    data = list(map(float, line.strip().split()))
    data_array.append(data)

data_array = np.array(data_array)
time = list(data_array[:, 0])
cab = list(data_array[:, 1])
ca = list(data_array[:, 2])


# print('llwleghwoe ')

class Hander_index():
    def __init__(self, info, info_name, weaken_length):
        self.info = info
        self.info_name = info_name
        self.lowerest = min(info)
        # self.get_baseline(weaken_length)

        self.lower1 = min(self.info[0:weaken_length])
        self.lower2 = min(self.info[-weaken_length - 1:-1])
        self.x1 = math.ceil(weaken_length / 2)
        self.x2 = len(self.info) - math.ceil(weaken_length / 2)

        print("len of info is {}, and the lowerest is y = {}".format(len(info), self.lowerest))

    def get_baseline(self, x):
        return (x - self.x1) * (self.lower1 - self.lower2) / (self.x1 - self.x2) + self.lower1

    def full_signal(self):
        plt.figure(figsize=(40, 3), dpi=300)
        x = range(len(self.info))
        plt.plot(x, self.info)
        plt.plot(x, [self.get_baseline(i) for i in range(len(x))])
        plt.xlabel(u"Index(S)")
        # x_major_locator=MultipleLocator(1)
        # plt.xlim(-0.5,25)
        plt.xticks(np.arange(0, len(self.info), 5000))
        plt.title(u'{}'.format(self.info_name))
        plt.savefig('{}'.format(self.info_name))

    def get_paras_for_mountain(self, p1, p2):
        # amp = self.Amp(p1,p2)
        time_s = time[p1]
        time_e = time[p2]
        top_value = max(self.info[p1:p2])
        top_index = self.info[p1:p2].index(top_value) + p1
        amp = top_value - self.get_baseline(top_index)
        auc = sum(self.info[p1:p2])
        half_top = self.get_baseline(top_index) + amp / 2
        half_right = top_index
        for i in range(top_index,p2):
            if self.info[i]<half_top:
                half_right = i
                break
        half_left = top_index
        for i in range(top_index,p1,-1):
            if  self.info[i]<half_top:
                half_left = i
                break
        # half_right = self.info[top_index:p2].index(half_top)
        # half_left = self.info[p1:top_index].index(half_top)
        t_half = time[half_right] - time[half_left]

        right_blow_value = min(self.info[top_index:p2])
        right_blow_index = self.info[top_index:p2].index(right_blow_value)+top_index
        right_amp = top_value - right_blow_value
        right_amp_90 = right_blow_value + right_amp * 0.9
        right_amp_10 = right_blow_value + right_amp * 0.1
        right_amp_90_index = self.info[top_index:right_blow_index].index(right_amp_90)
        right_amp_10_index = self.info[top_index:right_blow_index].index(right_amp_10)
        slope_90_10 = (right_amp_90 - right_amp_10) / (time[right_amp_90_index] - time[right_amp_10_index])

        print(
            "for [{}:{}]/[{}:{}], the top-value is {} with index {}, the Amplitude is [], slope is {}, T_half is {}, AUC is {}".format(
                p1, p1, time_s, time_e, top_value, top_index, amp, slope_90_10, t_half, auc))

        plt.figure(figsize=(float(80 * (p2 - p1) / len(self.info)), 3), dpi=300)
        x = range(p1, p2)
        plt.plot(x, self.info[p1:p2])
        plt.plot(x, [self.get_baseline(i) for i in range(len(x))])
        plt.vline(top_index, self.get_baseline(top_index), top_value, color = "red")  # 竖线
        plt.xlabel(u"Index(S)")
        plt.title(u'{}_[{}:{}]'.format(self.info_name, p1, p2))
        plt.savefig(u'{}_[{}:{}]'.format(self.info_name, p1, p2))


    def Amp(self, p1, p2):
        top = max(self.info[p1:p2])
        index = self.info[p1:p2].index(top)
        return top - self.get_bwaseline(index)

    def draw_mountain(self, p1, p2):
        plt.figure(figsize=(float(80 * (p2 - p1) / len(self.info)), 3), dpi=300)
        x = range(p1, p2)
        plt.plot(x, self.info[p1:p2])
        plt.plot(x, [self.get_baseline(i) for i in range(len(x))])
        # plt.vline(, -2, 3, color="red")  # 竖线
        plt.xlabel(u"Index(S)")
        plt.title(u'{}_[{}:{}]'.format(self.info_name, p1, p2))
        plt.savefig(u'{}_[{}:{}]'.format(self.info_name, p1, p2))


hander = Hander_index(ca, 'ca', 4000)
# print(hander.Amp(6800,7200))
hander.get_paras_for_mountain(60100, 62500)
# hander.full_signal()0
# hander.full_signal(ca,'ca')
