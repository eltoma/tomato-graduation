import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import cluster_afterCluster
import forecast_mapCaller
import forecast_speedCurve
import recognize

sns.set()

matplotlib.style.use("seaborn-whitegrid")
matplotlib.rcParams["axes.facecolor"] = "#ffffff"  # 绘图区颜色
matplotlib.rcParams["axes.edgecolor"] = "#000000"  # 绘图边缘颜色
matplotlib.rcParams["axes.spines.top"] = False  # 控制绘图四周的坐标轴显示
matplotlib.rcParams["axes.spines.right"] = False
matplotlib.rcParams["axes.spines.bottom"] = True
matplotlib.rcParams["font.family"] = "STSong"  # 中文字体样式

gaodeMapKey = "4a6d7fc937cfd3d38a6ef3e8e259fbb5"
googleMapKey = "AIzaSyATW2zfFWbHLlRoNMYs7Sa33iRpyjZOjAU"

# # 1.获取起点和终点的经纬度坐标
# 上新街到重邮
# origin = "106.596622,29.554773"
# destination = "106.604632,29.534505"

# 上新街到难上植物园
# origin = "106.596886,29.555189"
# destination = "106.62447,29.55484"

#三峡广场到大学城地铁站
# origin = "106.463636,29.55864"
# destination = "106.308908,29.60735"
# print("起点：" + origin)
# print("终点：" + destination)
# # # 2.根据起点和终点经纬度坐标，调用高德地图获取路径信息
# steps = forecast_mapCaller.queryRoute(origin, destination, gaodeMapKey)
# route = forecast_mapCaller.analyseRoute(steps)
# print("解析之后的路径：")
# print(route)
# # #
# # # # 3.生成车速曲线
# eleCentroids = pd.read_csv(open("./output/FCM/海拔聚类中心.csv"))
# eleCentroids = eleCentroids["0"].values
# # # # print(eleCentroids)
# speedCurve = forecast_speedCurve.generateSpeedCurve1(route,eleCentroids,googleMapKey)
# print("速度曲线长度：" + str(len(speedCurve)))
# print(speedCurve)
# # speedCurve = speedCurve[0:500]
# plt.grid(linestyle="--")
# plt.plot(speedCurve,linewidth=1.0,alpha=1)
# plt.ylabel("速度(km/h)")
# plt.xlabel("时间(s)")
# plt.savefig("./output/forecast/预测的车速曲线.png", bbox_inches="tight")
# # #
# features,sum = recognize.getFeature(speedCurve,120)
# centroids = pd.read_csv(open("./output/FCM/各类别SOC平均消耗量C=20.csv"))
# # cens1 = centroids.ix[0:1]
# # cens2 = centroids.ix[4:5]
# # cens = cens1.append(cens2)
# cen = centroids[["Vm","Pi","Pa","Pc"]].values
# SOC = centroids[["SOC"]].values
#
# DSOC = 0
# for feature in features:
#     four = feature[0:4]
#     label = cluster_afterCluster.categoryRecognize(four,cen)
#     print("label:" + str(label))
#     tmp = float(SOC[label])
#     DSOC = DSOC + tmp
# print("考虑拥堵：" + str(DSOC))
#
# # 不考虑拥堵
# speedCurve2 = forecast_speedCurve.generateSpeedCurve2(route,eleCentroids,googleMapKey)
# features2,sum2 = recognize.getFeature(speedCurve2,120)
#
# DSOC2 = 0
# for feature2 in features2:
#     four = feature2[0:4]
#     label = cluster_afterCluster.categoryRecognize(four,cen)
#     print("label:" + str(label))
#     tmp = float(SOC[label])
#     DSOC2 = DSOC2 + tmp
# print("不考虑拥堵：" + str(DSOC2))

# 里程耗电量估计
# 输入参数：origin----起点经纬度
#         destination----终点经纬度
# 返回：resultInJam-----考虑拥堵时的耗电量
#      resultNoTam-----不考虑拥堵时的耗电量
def powerConsumptionEstn(origin,destination):
    print("起点：" + origin)
    print("终点：" + destination)
    #1.根据起点和终点经纬度坐标，调用高德地图获取路径信息
    steps = forecast_mapCaller.queryRoute(origin, destination, gaodeMapKey)
    route = forecast_mapCaller.analyseRoute(steps)
    print("解析之后的路径：")
    print(route)
    #2.生成车速曲线
    eleCentroids = pd.read_csv(open("./output/FCM/海拔聚类中心.csv"))
    eleCentroids = eleCentroids["0"].values
    curveInJam = forecast_speedCurve.speedCurveInJam(route, eleCentroids, googleMapKey)
    curveNoJam = forecast_speedCurve.speedCurveNoJam(route, eleCentroids, googleMapKey)
    print("考虑拥堵速度曲线长度：" + str(len(curveInJam)))
    print("不考虑拥堵速度曲线长度：" + str(len(curveNoJam)))
    # 3.绘图
    plt.grid(linestyle="--")
    plt.plot(curveInJam, linewidth=1.0, alpha=1)
    plt.ylabel("速度(km/h)")
    plt.xlabel("时间(s)")
    title1 = "./output/forecast/" + str(origin) + str(destination) + "考虑拥堵" + ".png"
    plt.savefig(title1, bbox_inches="tight")
    plt.close()
    plt.plot(curveNoJam, linewidth=1.0, alpha=1)
    title2 = "./output/forecast/"+str(origin)+str(destination)+"不考虑拥堵"+".png"
    plt.savefig(title2, bbox_inches="tight")
    # 分段，计算耗电量
    centroids = pd.read_csv(open("./output/FCM/各类别SOC平均消耗量C=20.csv"))
    cen = centroids[["Vm", "Pi", "Pa", "Pc"]].values
    SOC = centroids[["SOC"]].values
    features1, sum1 = recognize.getFeature(curveInJam, 120)
    features2, sum2 = recognize.getFeature(curveNoJam, 120)
    dSOCInJam = 0
    for feature1 in features1:
        four = feature1[0:4]
        label = cluster_afterCluster.categoryRecognize(four, cen)
        print("label:" + str(label))
        tmp = float(SOC[label])
        dSOCInJam = dSOCInJam + tmp
    print("考虑拥堵：" + str(dSOCInJam))
    dSOCNoJam = 0
    for feature2 in features2:
        four = feature2[0:4]
        label = cluster_afterCluster.categoryRecognize(four, cen)
        print("label:" + str(label))
        tmp = float(SOC[label])
        dSOCNoJam = dSOCNoJam + tmp
    print("不考虑拥堵：" + str(dSOCNoJam))
    return dSOCInJam,dSOCNoJam

# powerConsumptionEstn(origin,destination)
