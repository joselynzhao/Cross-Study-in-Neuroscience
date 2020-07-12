import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.pyplot import MultipleLocator
import math
import inspect


#从堆栈第3层开始查找返回变量名称
def retrieve_name(var):
    for fi in inspect.stack()[2:]:
        for item in fi.frame.f_locals.items():
            if (var is item[1]):
                return item[0]
    return ""



import  numpy as np
file = open('samples.txt','r')
info  = file.readlines()
print(len(info))
# info_cut=[2000,11000]
# info = info[info_cut[0]:info_cut[1]]
# print(len(info))

data_array = []
for line in info:
    data = list(map(float,line.strip().split()))
    data_array.append(data)

data_array = np.array(data_array)
time = list(data_array[:,0])
cab = list(data_array[:,1])
ca = list(data_array[:,2])

# print('llwleghwoe ')

class Hander_index():
    def __init__(self,info,info_name,weaken_length):
        self.info = info
        self.info_name = info_name
        self.lowerest = min(info)
        # self.get_baseline(weaken_length)

        self.lower1 = min(self.info[0:weaken_length])
        self.lower2 = min(self.info[-weaken_length - 1:-1])
        self.x1 = math.ceil(weaken_length / 2)
        self.x2 = len(self.info) - math.ceil(weaken_length / 2)

        print("len of info is {}, and the lowerest is y = {}".format(len(info),self.lowerest))

    def get_baseline(self,x):
        return (x-self.x1)*(self.lower1-self.lower2)/(self.x1-self.x2)+self.lower1

    def full_signal(self):
        plt.figure(figsize=(40, 3), dpi=300)
        x = range(len(self.info))
        plt.plot(x, self.info)
        plt.plot(x,[self.get_baseline(i) for i in range(len(x))])
        plt.xlabel(u"Index(S)")
        # x_major_locator=MultipleLocator(1)
        # plt.xlim(-0.5,25)
        plt.xticks(np.arange(0, len(self.info), 5000))
        plt.title(u'{}'.format(self.info_name))
        plt.savefig('{}'.format(self.info_name))

    def Amp(self,p1,p2):
        top = max(self.info[p1:p2])
        index = self.info[p1:p2].index(top)
        return top - self.get_baseline(index)

    def draw_mountain(self,p1,p2):
        plt.figure(figsize=(float(80*(p2-p1)/len(self.info)),3),dpi=300)
        x  = range(p1,p2)
        plt.plot(x,self.info[p1:p2])
        plt.plot(x,[self.get_baseline(i) for i in range(len(x))])
        plt.xlabel(u"Index(S)")
        plt.title(u'{}_[{}:{}]'.format(self.info_name,p1,p2))
        plt.savefig(u'{}_[{}:{}]'.format(self.info_name,p1,p2))






hander = Hander_index(ca,'ca',4000)
# print(hander.Amp(6800,7200))
hander.draw_mountain(60000,62000)
# hander.full_signal()0
# hander.full_signal(ca,'ca')
