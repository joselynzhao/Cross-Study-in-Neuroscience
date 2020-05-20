#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@AUTHOR:Joselyn Zhao
@CONTACT:zhaojing17@foxmail.com
@HOME_PAGE:joselynzhao.top
@SOFTWERE:PyCharm
@FILE:MNE.py
@TIME:2020/5/15 15:43
@DES:
'''

# 导入必要的包
import os.path as op

import numpy as np
import matplotlib.pyplot as plt

import mne
from mne.datasets import somato
from mne.baseline import rescale
from mne.stats import bootstrap_confidence_interval

# 设置参数
data_path = somato.data_path()
subject = '01'
task = 'somato'
raw_fname = op.join(data_path, 'sub-{}'.format(subject), 'meg',
                    'sub-{}_task-{}_meg.fif'.format(subject, task))

# 设置4种不同波段的频率范围
iter_freqs = [
    ('Theta', 4, 7),
    ('Alpha', 8, 12),
    ('Beta', 13, 25),
    ('Gamma', 30, 45)
]

###############################################################################
# 创建每一个频段的时间功率谱

# 设置epoch的相关参数，这里分析event_id为1的事件，事件时间范围[-1, 3]
event_id, tmin, tmax = 1, -1., 3.
baseline = None

# 从源文件中读取事件信息
# raw = mne.io.read_raw
raw = mne.io.read_raw_fif(raw_fname)
events = mne.find_events(raw, stim_channel='STI 014')
# 初始化处理结果字典，frequency_map用于保存各个频段的处理结果
frequency_map = list()

for band, fmin, fmax in iter_freqs:
    # 加载原始数据
    raw = mne.io.read_raw_fif(raw_fname, preload=True)
    # 提取MEG数据，这里使用的是MEG的梯度数据，非EEG数据
    raw.pick_types(meg='grad', eog=True)

    # 设计带通滤波，这里l/h_trans_bandwidth是滤波器的设计参数，会影响滤波器的品质
    raw.filter(fmin, fmax, n_jobs=1, l_trans_bandwidth=1, h_trans_bandwidth=1)

    # 生成epoch格式的数据
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline=baseline,
                        reject=dict(grad=4000e-13, eog=350e-6),
                        preload=True)
    # 去除evoked能量，保留induced部分
    epochs.subtract_evoked()

    # 构建Hilbert解析信号 (包络)
    epochs.apply_hilbert(envelope=True)
    # 保存对应频段的处理结果，epochs的均值代表该频段的（induced）处理结果
    frequency_map.append(((band, fmin, fmax), epochs.average()))
    del epochs
del raw


###############################################################################
# 计算GFP，采用bootstrap方法计算置信区间，与基线比较追踪每一个频段的空间域中事件的出现
# 可以看出主要的反应集中在 Alpha 和 Beta 频段.


# 计算置信GFP置信区间的辅助函数
def stat_fun(x):
    """Return sum of squares."""
    return np.sum(x ** 2, axis=0)


# 构建绘图的fig，由4行1列子图构成，共享x和y轴
fig, axes = plt.subplots(4, 1, figsize=(10, 7), sharex=True, sharey=True)
# 设置绘图颜色
colors = plt.get_cmap('winter_r')(np.linspace(0, 1, 4))
# 开始绘制不同频段对应的处理结果
for ((freq_name, fmin, fmax), average), color, ax in zip(
        frequency_map, colors, axes.ravel()[::-1]):
    # 扩展时间，实际上也就是为例扩展横轴，绘图后横轴会好看些，对于计算没有什么实际意义
    times = average.times * 1e3
    # 计算gfp，这里没有进行正则化处理
    gfp = np.sum(average.data ** 2, axis=0)
    # 重新缩放gfp曲线，根据rescale的源码缩放后是减去均值的
    gfp = mne.baseline.rescale(gfp, times, baseline=(None, 0))
    # 绘制gfp曲线
    ax.plot(times, gfp, label=freq_name, color=color, linewidth=2.5)
    # 绘制0值基线
    ax.axhline(0, linestyle='--', color='grey', linewidth=2)
    # 利用bootstrap计算置信区间
    ci_low, ci_up = bootstrap_confidence_interval(average.data, random_state=0, stat_fun=stat_fun)
    # 对置信区间进行缩放，这里主要的作用是对ci_low/up减去均值
    ci_low = rescale(ci_low, average.times, baseline=(None, 0))
    ci_up = rescale(ci_up, average.times, baseline=(None, 0))
    # 绘制gfp的置信区间
    ax.fill_between(times, gfp + ci_up, gfp - ci_low, color=color, alpha=0.3)
    # 添加网格
    ax.grid(True)
    # 设置y轴名称
    ax.set_ylabel('GFP')
    # 添加图的说明
    ax.annotate('%s (%d-%dHz)' % (freq_name, fmin, fmax),
                xy=(0.95, 0.8),
                horizontalalignment='right',
                xycoords='axes fraction')
    # 设置x轴的坐标范围，这里和上面扩展后的时间保持一致
    ax.set_xlim(-1000, 3000)
# 设置x轴的名称
axes.ravel()[-1].set_xlabel('Time [ms]')
# 绘图显示
plt.show()
