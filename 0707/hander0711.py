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
info_cut=[2000,11000]
info = info[info_cut[0]:info_cut[1]]
print(len(info))

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
    def __init__(self):
        pass
    def full_signal(self,info,info_name):
        plt.figure(figsize=(40, 3), dpi=300)
        x = range(len(info))
        plt.plot(x, info)
        plt.xlabel(u"Index(S)")
        # x_major_locator=MultipleLocator(1)
        # plt.xlim(-0.5,25)
        plt.xticks(np.arange(0, len(info), 500))
        plt.title(u'{}'.format(info_name))
        plt.savefig('{}'.format(info_name))

hander = Hander_index()
# hander.full_signal(cab,'cab')
hander.full_signal(ca,'ca')
