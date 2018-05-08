# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 09:57:21 2018

@author: Tomato
"""
# ==============================================================================
# 核密度估计（kernel density estimation）是非参数统计检验中的重要方法之一，
# 常用于估计未知的密度函数。本节将向大家介绍在 Python 中如何利用 Scikit-Learn 库中的相关工具
# ，对数据集的样本分布进行核密度估计。
# ==============================================================================

import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import LeaveOneOut

# 导入可视化库：

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

import forecast_speedCurve

sns.set()


matplotlib.style.use("seaborn-whitegrid")
matplotlib.rcParams["axes.facecolor"] = "#ffffff"  # 绘图区颜色
matplotlib.rcParams["axes.edgecolor"] = "#000000"  # 绘图边缘颜色
matplotlib.rcParams["axes.spines.top"] = False  # 控制绘图四周的坐标轴显示
matplotlib.rcParams["axes.spines.right"] = False
matplotlib.rcParams["axes.spines.bottom"] = True
matplotlib.rcParams["font.family"] = "STSong"  # 中文字体样式
matplotlib.rcParams["font.size"] = 20


# 计算最佳带宽
# data：数据
def calBestBandwidth(data):
    bandwidths = 10 ** np.linspace(-1, 1, 100)
    grid = GridSearchCV(KernelDensity(kernel="gaussian"),
                        {"bandwidth": bandwidths},
                        cv=LeaveOneOut(len(data)))
    grid.fit(data[:, None])
    ban = grid.best_params_.get("bandwidth")
    return ban


# 进行核密度估计并绘图
# avgSpeeds:平均车速序列
# ban:带宽
def KDE(avgSpeeds, ban, x_d):
    avgSpeeds.sort()
    kde = KernelDensity(bandwidth=ban, kernel="gaussian")
    kde.fit(avgSpeeds)
    # 运用 score_samples 函数来获得概率密度函数的对数
    logprob = kde.score_samples(x_d[:, None])
    # plt.grid(linestyle="--")
    # plt.xticks(fontsize=15)
    # plt.yticks(fontsize=15)
    # plt.plot(x_d, np.exp(logprob), "#DB4520", alpha=1, label="KDE")
    # # a=min(np.exp(logprob))
    # # print(a)
    # plt.hist(avgSpeeds, 20, normed=1, histtype="bar", facecolor="#000000", alpha=0.6, label="直方图估计")
    # plt.legend(loc="upper right", frameon=True, edgecolor="#000000",fontsize=15)
    return np.exp(logprob)


if __name__ == "__main__":
    # 这个主函数主要是为了绘制论文需要的图片
    file0 = pd.read_csv(open("./output/FCM/第0类海拔下的片段.csv"))
    avgSpeed0 = file0["0"].values

    file1 = pd.read_csv(open("./output/FCM/第1类海拔下的片段.csv"))
    avgSpeed1 = file1["0"].values

    file2 = pd.read_csv(open("./output/FCM/第2类海拔下的片段.csv"))
    avgSpeed2 = file2["0"].values

    file3 = pd.read_csv(open("./output/FCM/第3类海拔下的片段.csv"))
    avgSpeed3 = file3["0"].values

    file4 = pd.read_csv(open("./output/FCM/第4类海拔下的片段.csv"))
    avgSpeed4 = file4["0"].values
    print(avgSpeed0)
    print("=========================")
    # 2.计算最佳带宽
    # ban0 = calBestBandwidth(avgSpeed0)
    # print(ban0) #3.94
    # ban1 = calBestBandwidth(avgSpeed1)
    #     # print(ban1) #3.43
    #     # ban2 = calBestBandwidth(avgSpeed2)
    #     # print(ban2) #2.15
    #     # ban3 = calBestBandwidth(avgSpeed3)
    #     # print(ban3) #4.98
    #     # ban4 = calBestBandwidth(avgSpeed4)
    #     # print(ban4) #3.13

    # 3.核密度估计并绘图
    x_d = np.linspace(0, 110, 2000)
    #
    # row0 = avgSpeed0.shape[0]
    # avgSpeed0.shape = (row0, 1)
    # fx0 = KDE(avgSpeed0, 3.94, x_d)
    # strBan0 = str(round(3.94,2))
    # plt.ylabel("$f(x)$",fontsize = 15)
    # plt.xlabel("x",fontsize = 15)
    # plt.title("第3类海拔下速度的密度估计（bandwidth=%s）" % strBan0,fontsize = 15)
    # plt.savefig("./output/KDE/第3类海拔下速度的密度估计（bandwidth=%s）.png" % strBan0, bbox_inches="tight")

    # plt.figure(2)
    # row1 = avgSpeed1.shape[0]
    # avgSpeed1.shape = (row1, 1)
    # fx1 = KDE(avgSpeed1, 3.43, x_d)
    # strBan1 = str(round(3.43,2))
    # plt.ylabel("$f(x)$",fontsize = 15)
    # plt.xlabel("x",fontsize = 15)
    # plt.title("第0类海拔下速度的密度估计（bandwidth=%s）" % strBan1,fontsize = 15)
    # plt.savefig("./output/KDE/第0类海拔下速度的密度估计（bandwidth=%s）.png" % strBan1, bbox_inches="tight")

    # plt.figure(3)
    row2 = avgSpeed2.shape[0]
    avgSpeed2.shape = (row2, 1)
    fx2 = KDE(avgSpeed2, 2.15, x_d)
    # strBan2 = str(round(2.15,2))
    # plt.ylabel("$f(x)$",fontsize = 15)
    # plt.xlabel("x",fontsize = 15)
    # plt.title("第4类海拔下速度的密度估计（bandwidth=%s）" % strBan2,fontsize = 15)
    # plt.savefig("./output/KDE/第4类海拔下速度的密度估计（bandwidth=%s）.png" % strBan2, bbox_inches="tight")
    #
    # plt.figure(4)
    # row3 = avgSpeed3.shape[0]
    # avgSpeed3.shape = (row3, 1)
    # fx3 = KDE(avgSpeed3, 4.98, x_d)
    # strBan3 = str(round(4.98,2))
    # plt.ylabel("$f(x)$",fontsize = 15)
    # plt.xlabel("x",fontsize = 15)
    # plt.title("第1类海拔下速度的密度估计（bandwidth=%s）" % strBan3,fontsize = 15)
    # plt.savefig("./output/KDE/第1类海拔下速度的密度估计（bandwidth=%s）.png" % strBan3, bbox_inches="tight")
    #
    # plt.figure(5)
    # row4 = avgSpeed4.shape[0]
    # avgSpeed4.shape = (row4, 1)
    # fx4 = KDE(avgSpeed4, 3.13, x_d)
    # strBan4 = str(round(3.13,2))
    # plt.ylabel("$f(x)$",fontsize = 15)
    # plt.xlabel("x",fontsize = 15)
    # plt.title("第2类海拔下速度的密度估计（bandwidth=%s）" % strBan4,fontsize = 15)
    # plt.savefig("./output/KDE/第2类海拔下速度的密度估计（bandwidth=%s）.png" % strBan4, bbox_inches="tight")

    plt.figure(6)
    randoms = forecast_speedCurve.acRej(x_d,fx2,2000)
    print(randoms)
    # randomBan = calBestBandwidth(randoms)
    # print(randomBan) #1.35
    randomRow = randoms.shape[0]
    randoms.shape = (randomRow, 1)
    randomFx = KDE(randoms,1.35,x_d)
    plt.grid(linestyle="--")
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.plot(x_d, randomFx, "r", alpha=1, label="生成的随机数的概率密度")
    plt.plot(x_d, fx2, "k--", alpha=1, label="原始概率密度")
    plt.legend(loc="upper right", frameon=True, edgecolor="#000000")
    plt.ylabel("$f(x)$",fontsize = 15)
    plt.xlabel("x",fontsize = 15)
    plt.title("生成的随机数的概率密度与原始概率密度对比图",fontsize = 15)
    plt.savefig("./output/KDE/生成的随机数的概率密度与原始概率密度对比图.png", bbox_inches="tight")

