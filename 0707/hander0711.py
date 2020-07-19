# %%
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
from scipy import signal, fftpack

class Hander_index():
    def __init__(self, time, info, info_name, weaken_length,out_file=None):
        self.time = time
        self.info = info
        self.info_name = info_name
        self.lowerest = min(info)
        # self.get_baseline(weaken_length)

        self.lower1 = min(self.info[0:weaken_length])
        self.lower2 = min(self.info[-weaken_length - 1:-1])
        self.x1 = math.ceil(weaken_length / 2)
        self.x2 = len(self.info) - math.ceil(weaken_length / 2)
        self.out_file =out_file

        print("len of info is {}, and the lowerest is y = {}".format(len(info), self.lowerest))

    def get_baseline(self, x):
        return (x - self.x1) * (self.lower1 - self.lower2) / (self.x1 - self.x2) + self.lower1

    def full_signal(self):
        plt.figure(figsize=(40, 3), dpi=300)
        x = range(len(self.info))
        info_s = signal.savgol_filter(self.info, window_length=333, polyorder=1)
        plt.plot(x, self.info, label='signal')
        plt.plot(x,info_s,label='signal_smooth')
        plt.plot(x, [self.get_baseline(i) for i in range(len(x))],label='baseline')
        plt.xlabel(u"Index(S)")
        plt.legend()
        # x_major_locator=MultipleLocator(1)
        # plt.xlim(-0.5,25)
        plt.xticks(np.arange(0, len(self.info), 5000))
        plt.title(u'{}'.format(self.info_name))
        plt.savefig(file_No+'/{}'.format(self.info_name))

    def __get_near_index(self, value, left, right):
        init = self.info[left] - value  # 若果>0, 则下降, 如果<0,则上升.
        for i in range(left, right, 1):  # left<right
            if (self.info[i] - value) * init < 0:  # 异号
                return int(i)

    def __get_near_index1(self, value, left, right):
        min = 100
        min_index = left
        for i in range(left, right, 1):
            if abs(self.info[i] - value) < min:
                min = abs(self.info[i] - value)
                min_index = i
        return min_index

    def __get_tau(self, x, a, b, c):
        return a - b * np.exp(-c * x)

    def get_paras_for_mountain(self, p1, p2):
        # amp = self.Amp(p1,p2)
        time_s = self.time[p1]
        time_e = self.time[p2]
        top_value = max(self.info[p1:p2])
        top_index = self.info[p1:p2].index(top_value) + p1
        amp = top_value - self.get_baseline(top_index)
        auc = sum(self.info[p1:p2])
        half_top = self.get_baseline(top_index) + amp / 2
        half_left = self.__get_near_index1(half_top, p1, top_index)
        half_right = self.__get_near_index1(half_top, top_index, p2)
        t_half = self.time[half_right] - self.time[half_left]

        right_blow_value = min(self.info[top_index:p2])
        right_blow_index = self.info[top_index:p2].index(right_blow_value) + top_index
        right_amp = top_value - right_blow_value
        right_amp_90 = right_blow_value + right_amp * 0.9
        right_amp_10 = right_blow_value + right_amp * 0.1
        right_amp_90_index = self.__get_near_index1(right_amp_90, top_index, right_blow_index)
        right_amp_10_index = self.__get_near_index1(right_amp_10, top_index, right_blow_index)
        # right_amp_90_index = self.info[top_index:right_blow_index].index(right_amp_90)
        # right_amp_10_index = self.info[top_index:right_blow_index].index(right_amp_10)
        right_slope = (right_amp_90 - right_amp_10) / (self.time[right_amp_90_index] - self.time[right_amp_10_index])
        
        left_blow_value  = min(self.info[p1:top_index])
        left_blow_index = self.info[p1:top_index].index(left_blow_value)+p1
        left_amp = top_value - left_blow_value
        left_amp_90 = left_blow_value +left_amp * 0.9
        left_amp_10 = left_blow_value + left_amp * 0.1
        left_amp_90_index = self.__get_near_index1(left_amp_90, left_blow_index, top_index)
        left_amp_10_index = self.__get_near_index1(left_amp_10, left_blow_index, top_index)
        left_slope = (left_amp_90 - left_amp_10)/(self.time[left_amp_90_index] - self.time[left_amp_10_index])

        

        # https://blog.csdn.net/cxu123321/article/details/101000604
        # x = np.array(range(right_amp_90_index-top_index,right_amp_10_index-top_index,10))
        # y = np.array([self.info[i] for i in x])

        # 要拟合的是从峰顶到峰尾的数据
        x = np.arange(top_index, p2)
        y = np.array([self.info[i] for i in x])
        print(len(x))
        from scipy.optimize import curve_fit
        def fit(func, x, y):
            (a, b, c), _ = curve_fit(func, x, y, maxfev=5000)
            return a, b, c

        print(top_index, x.shape, y.shape)
        # 拟合时要把index平移到原点
        a, b, c = fit(self.__get_tau, x - top_index, y)
        print(a, b, c)
        # plt.plot(x,y)

        self.out_file.write(' '.join(
            map(str, [p1, p2, time_s, time_e, top_value, top_index, amp, left_slope, right_slope, t_half, auc, a, b, c])) + '\n')
        # print(
        #     "for [{}:{}]/[{}:{}], the top-value is {} with index {}, the Amplitude is {}, slope is {}, T_half is {}, AUC is {}, a = {}. b={}.c={}".format(
        #         p1, p1, time_s, time_e, top_value, top_index, amp, slope_90_10, t_half, auc,a,b,c))

        plt.figure(figsize=(float(800 * (p2 - p1) / len(self.info)), 3), dpi=300)
        x = range(p1, p2)
        plt.plot(x, self.info[p1:p2])
        plt.plot(x, [self.get_baseline(i) for i in range(p1, p2)])
        # x2 = range(right_amp_90_index,right_amp_10_index,1)

        # 绘制拟合曲线
        x2 = range(top_index, p2)
        plt.plot(x2, [self.__get_tau(i - top_index, a, b, c) for i in x2])  # 曲线的输入也应该平移到0

        plt.vlines(top_index, self.get_baseline(top_index), top_value, color='red')  # 竖线
        plt.hlines(half_top, half_left, half_right, color='green')
        plt.xlabel(u"Index(S)")
        plt.title(u'{}_[{}:{}]'.format(self.info_name, p1, p2))
        plt.savefig(file_No+u'/{}_[{}:{}]'.format(self.info_name, p1, p2))





#

# hander.full_signal(ca,'ca')

if __name__ == '__main__':
    file_No = '003'
    func = 3


    file = open('samples-' + file_No + '.txt', 'r')
    info = file.readlines()
    print(len(info))

    data_array = []
    for line in info:
        data = list(map(float, line.strip().split()))
        data_array.append(data)

    data_array = np.array(data_array)
    time = list(data_array[:, 0])
    cab = list(data_array[:, 1])
    ca = list(data_array[:, 2])


    if func == 1:  ##提取参数信息
        outfile = open('res-' + file_No + '.txt', 'w')
        outfile.write('p1 p2 time1 time2 top_value top_index amp slope_left slope_right t_half auc a b c\n')
        hander = Hander_index(time, ca, 'ca', 4000, outfile)
        segfile = open('peak-' + file_No + '.txt', 'r')
        seg_data = segfile.readlines()
        for line in seg_data:
            left, right = map(int, line.strip().split())
            print('[{}:{}]'.format(left, right))
            hander.get_paras_for_mountain(left, right)

    elif func == 2:
        hander = Hander_index(time, ca, 'ca', 4000)
        hander.full_signal() #绘制全局曲线.


    elif func == 3: #指定起始位, 提出参数
        spe_file = open('res_spe-'+file_No+'.txt','a')
        spe_file.write('p1 p2 time1 time2 top_value top_index amp slope_left slope_right t_half auc a b c\n')
        hander = Hander_index(time, ca, 'ca', 4000, spe_file)
        # 手动输入起止点的index
        left = 7248
        right = 7996
        hander.get_paras_for_mountain(left,right)











# %%
