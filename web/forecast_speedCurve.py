import numpy as np
import math
import pandas as pd
import auxiliaryFunc
import forecast_mapCaller
import forecast_KDE
import cluster_afterCluster


# 找到与生成的x最相近的x_d的index
# x:随机生成的x    x_d：KDE代码中的采样序列（横轴）
def findMax(x, x_d):
    index = 0
    for i in range(0, len(x_d)):
        if x >= x_d[i] and x <= x_d[i + 1]:
            index = i
            return index
            break


# 舍选抽样法生成随机数
# x_d:采样序列（横轴）   fx:各海拔下速度的概率密度序列（纵轴）
# n:生成的随机数的个数
def acRej(x_d, fx, n):
    xmin = min(x_d)
    xmax = max(x_d)
    ymin = min(fx)
    ymax = max(fx)
    accepted = 0
    samples = np.zeros(n)
    count = 0
    # generation l oop
    while (accepted < n):
        x = np.random.uniform(xmin, xmax)
        # print(x)
        # pick a uniform number on [0, ymax)
        y = np.random.uniform(ymin, ymax)
        index = findMax(x, x_d)
        px = fx[index]
        # Do the accept/reject comparison
        if y < px:
            samples[accepted] = x
            accepted += 1
            count += 1
    return samples

# 生成车速曲线:考虑当前拥堵
# route：解析之后的路径经纬度、拥堵序列
# eleCentroids：海拔聚类中心
def speedCurveInJam(route,eleCentroids,googleMapKey):
    # 把route以1000米为周期分组
    groups = []
    dis = 0
    tmp = []
    for data in route:
        tmp.append(data)
        dis += int(data['distance'])
        if (dis > 1000):
            print("大片段内距离：" + str(dis))
            groups.append(tmp)
            tmp = []
            dis = 0
    print("groups长度：" + str(len(groups)))
    print("groups:")
    print(groups)
    # 得到不同类别海拔下的fx
    x_d = np.linspace(0, 110, 2000)
    file0 = pd.read_csv(open("./output/FCM/第0类海拔下的片段.csv"))
    avgSpeed0 = file0["0"].values
    row0 = avgSpeed0.shape[0]
    avgSpeed0.shape = (row0, 1)
    fx0 = forecast_KDE.KDE(avgSpeed0, 3.94, x_d)

    file1 = pd.read_csv(open("./output/FCM/第1类海拔下的片段.csv"))
    avgSpeed1 = file1["0"].values
    row1 = avgSpeed1.shape[0]
    avgSpeed1.shape = (row1, 1)
    fx1 = forecast_KDE.KDE(avgSpeed1, 3.43, x_d)

    file2 = pd.read_csv(open("./output/FCM/第2类海拔下的片段.csv"))
    avgSpeed2 = file2["0"].values
    row2 = avgSpeed2.shape[0]
    avgSpeed2.shape = (row2, 1)
    fx2 = forecast_KDE.KDE(avgSpeed2, 2.15, x_d)

    file3 = pd.read_csv(open("./output/FCM/第3类海拔下的片段.csv"))
    avgSpeed3 = file3["0"].values
    row3 = avgSpeed3.shape[0]
    avgSpeed3.shape = (row3, 1)
    fx3 = forecast_KDE.KDE(avgSpeed3, 4.98, x_d)

    file4 = pd.read_csv(open("./output/FCM/第4类海拔下的片段.csv"))
    avgSpeed4 = file4["0"].values
    row4 = avgSpeed4.shape[0]
    avgSpeed4.shape = (row4, 1)
    fx4 = forecast_KDE.KDE(avgSpeed4, 3.13, x_d)

    # 遍历groups，生成车速曲线
    speedCurve = [0]
    for group in groups:
        origin = group[0]["head"]
        destination = group[-1]["tail"]
        elevation1 = forecast_mapCaller.getElevation(origin, googleMapKey)
        elevation2 = forecast_mapCaller.getElevation(destination, googleMapKey)
        dElevation = elevation2 - elevation1
        label = cluster_afterCluster.categoryRecognize(dElevation,eleCentroids)
        if label == 0:
            print("第0类海拔:" + str(dElevation))
            fx = fx0
        elif label == 1:
            print("第1类海拔:" + str(dElevation))
            fx = fx1
        elif label == 2:
            print("第2类海拔:" + str(dElevation))
            fx = fx2
        elif label == 3:
            print("第3类海拔:" + str(dElevation))
            fx = fx3
        else:
            print("第4类海拔:" + str(dElevation))
            fx = fx4
        for item in group:
            status = item["status"]
            print(status)
            dist = int(item["distance"])
            speedIntegrate = 0
            while (speedIntegrate < dist):
                speed = acRej(x_d, fx, 1)  # 单位：km/h
                # print("假设:" + str(speed))
                if status == "畅通":
                    if not (speed <= 60):
                        # print("畅通,速度应该speed >= 30")
                        continue
                elif status == "缓行":
                    if not (speed <= 30):
                        # print("缓行,速度应该speed <30")
                        continue
                elif status == "拥堵":
                    if not (speed <= 20):
                        # print("拥堵,速度应该speed < 20")
                        continue
                elif status == "严重拥堵":
                    if not (speed <= 10):
                        # print("严重拥堵,速度应该speed < 10")
                        continue
                # print("接受：" + str(speed))
                speedCurve.extend(speed)
                # 把速度转换为m/s,1000/3600 = 0.278
                mileSpeed = speed * 0.278
                speedIntegrate = speedIntegrate + mileSpeed
    return speedCurve

# 生成车速曲线:不考虑当前拥堵
def speedCurveNoJam(route,eleCentroids,googleMapKey):
    # 把route以500米为周期分组
    groups = []
    dis = 0
    tmp = []
    for data in route:
        tmp.append(data)
        dis += int(data['distance'])
        if (dis > 1000):
            print("大片段内距离：" + str(dis))
            groups.append(tmp)
            tmp = []
            dis = 0
    print("groups长度：" + str(len(groups)))
    # print("groups:")
    # print(groups)
    # 得到不同类别海拔下的fx
    x_d = np.linspace(0, 110, 2000)
    file0 = pd.read_csv(open("./output/FCM/第0类海拔下的片段.csv"))
    avgSpeed0 = file0["0"].values
    row0 = avgSpeed0.shape[0]
    avgSpeed0.shape = (row0, 1)
    fx0 = forecast_KDE.KDE(avgSpeed0, 3.94, x_d)

    file1 = pd.read_csv(open("./output/FCM/第1类海拔下的片段.csv"))
    avgSpeed1 = file1["0"].values
    row1 = avgSpeed1.shape[0]
    avgSpeed1.shape = (row1, 1)
    fx1 = forecast_KDE.KDE(avgSpeed1, 3.43, x_d)

    file2 = pd.read_csv(open("./output/FCM/第2类海拔下的片段.csv"))
    avgSpeed2 = file2["0"].values
    row2 = avgSpeed2.shape[0]
    avgSpeed2.shape = (row2, 1)
    fx2 = forecast_KDE.KDE(avgSpeed2, 2.15, x_d)

    file3 = pd.read_csv(open("./output/FCM/第3类海拔下的片段.csv"))
    avgSpeed3 = file3["0"].values
    row3 = avgSpeed3.shape[0]
    avgSpeed3.shape = (row3, 1)
    fx3 = forecast_KDE.KDE(avgSpeed3, 4.98, x_d)

    file4 = pd.read_csv(open("./output/FCM/第4类海拔下的片段.csv"))
    avgSpeed4 = file4["0"].values
    row4 = avgSpeed4.shape[0]
    avgSpeed4.shape = (row4, 1)
    fx4 = forecast_KDE.KDE(avgSpeed4, 3.13, x_d)

    # 遍历groups，生成车速曲线
    speedCurve = [0]
    for group in groups:
        origin = group[0]["head"]
        destination = group[-1]["tail"]
        elevation1 = forecast_mapCaller.getElevation(origin, googleMapKey)
        elevation2 = forecast_mapCaller.getElevation(destination, googleMapKey)
        dElevation = elevation2 - elevation1
        label = cluster_afterCluster.categoryRecognize(dElevation,eleCentroids)
        if label == 0:
            print("第0类海拔:" + str(dElevation))
            fx = fx0
        elif label == 1:
            print("第1类海拔:" + str(dElevation))
            fx = fx1
        elif label == 2:
            print("第2类海拔:" + str(dElevation))
            fx = fx2
        elif label == 3:
            print("第3类海拔:" + str(dElevation))
            fx = fx3
        else:
            print("第4类海拔:" + str(dElevation))
            fx = fx4
        for item in group:
            # status = item["status"]
            dist = int(item["distance"])
            speedIntegrate = 0
            while (speedIntegrate < dist):
                speed = acRej(x_d, fx, 1)  # 单位：km/h
                # print("假设:" + str(speed))
                index = len(speedCurve)-1
                if math.fabs(speed-speedCurve[index])>8:
                    continue
                speedCurve.extend(speed)
                # 把速度转换为m/s,1000/3600 = 0.278
                mileSpeed = speed * 0.278
                speedIntegrate = speedIntegrate + mileSpeed
    return speedCurve