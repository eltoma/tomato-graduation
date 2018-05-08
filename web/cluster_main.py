import numpy as np
import pandas as pd
import auxiliaryFunc
import cluster_PCA
import cluster_fuzzyCMeans
import cluster_afterCluster
from sklearn import preprocessing
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.rcParams["font.family"] = "STSong"


# 第一部分：聚类分析主流程执行文件
# 输入：718个json文件

# =============主成分分析==========================================
print("开始主成分分析")
cluster_PCA.PCAMethod("./input")


# =============聚类分析=============================================
print("开始聚类分析")
# 读取json文件
origData = auxiliaryFunc.readJson("./input")


elevationData = auxiliaryFunc.getColumn(origData,[12])
#绘制海拔抖动图
sns.set(font_scale=1.5,font="STSong") #设置字体大小、字体
sns.utils.axlabel(" ", "海拔(m)") #设置X,Y坐标名
sns.stripplot(data=elevationData, jitter=True)
plt.title("海拔分布抖动图")
plt.savefig("./output/FCM/海拔分布抖动图.png")
plt.close()

# 海拔聚类
print("开始海拔聚类分析")
eleFuzzyMat,eleCentroids,eleLabel = cluster_fuzzyCMeans.FCMMethod(elevationData,5,2,100)

auxiliaryFunc.saveToCsv(eleCentroids,"./output/FCM/海拔聚类中心.csv")

# 绘制海拔聚类效果图
tmpLabel = eleLabel #不直接使用eleLabel，之后的操作会改变其维数
tmpLabel.shape = (1,718)
tmpLabel = np.transpose(tmpLabel)
together = np.hstack((elevationData,tmpLabel))
print(together)
df = pd.DataFrame(together,columns=["海拔","类别"])
sns.set(font_scale=1.5,font="STSong") #设置字体大小、字体
sns.stripplot(x="类别",y="海拔",data=df, jitter=True)
sns.utils.axlabel("类别", "海拔(m)") #设置X,Y坐标名
plt.title("海拔聚类效果图")
plt.savefig("./output/FCM/海拔聚类效果图.png")
plt.close()

# 统计各海拔下的片段数
res = df.groupby("类别")
auxiliaryFunc.saveToCsv(res.count(),"./output/FCM/各类海拔下的片段数.csv")

# 将数据划分到各类海拔下
speedData0,speedData1,speedData2,speedData3,speedData4 = [],[],[],[],[]
speedData = auxiliaryFunc.getColumn(origData,[1,2,9,11])
groups = cluster_afterCluster.diviCategory(speedData,eleLabel)
for group in groups:
    if group[0] == 0:
        speedData0 = auxiliaryFunc.getColumn(np.array(group[1]),[0,1,2,3])
    elif group[0] == 1:
        speedData1 = auxiliaryFunc.getColumn(np.array(group[1]),[0,1,2,3])
    elif group[0] == 2:
        speedData2 = auxiliaryFunc.getColumn(np.array(group[1]),[0,1,2,3])
    elif group[0] == 3:
        speedData3 = auxiliaryFunc.getColumn(np.array(group[1]),[0,1,2,3])
    else:
        speedData4 = auxiliaryFunc.getColumn(np.array(group[1]),[0,1,2,3])
auxiliaryFunc.saveToCsv(speedData0,"./output/FCM/第0类海拔下的片段.csv")
auxiliaryFunc.saveToCsv(speedData1,"./output/FCM/第1类海拔下的片段.csv")
auxiliaryFunc.saveToCsv(speedData2,"./output/FCM/第2类海拔下的片段.csv")
auxiliaryFunc.saveToCsv(speedData3,"./output/FCM/第3类海拔下的片段.csv")
auxiliaryFunc.saveToCsv(speedData4,"./output/FCM/第4类海拔下的片段.csv")

# 各类海拔下的片段的聚类
print("第0类海拔下的片段聚类")
fuzzyMat0,centroids0,label0 = cluster_fuzzyCMeans.FCMMethod(speedData0,4,2,100)
auxiliaryFunc.saveToCsv(centroids0,"./output/FCM/第0类海拔下速度曲线的聚类中心.csv")
print("第1类海拔下的片段聚类")
fuzzyMat1,centroids1,label1 = cluster_fuzzyCMeans.FCMMethod(speedData1,4,2,100)
auxiliaryFunc.saveToCsv(centroids1,"./output/FCM/第1类海拔下速度曲线的聚类中心.csv")
print("第2类海拔下的片段聚类")
fuzzyMat2,centroids2,label2 = cluster_fuzzyCMeans.FCMMethod(speedData2,4,2,100)
auxiliaryFunc.saveToCsv(centroids2,"./output/FCM/第2类海拔下速度曲线的聚类中心.csv")
print("第3类海拔下的片段聚类")
fuzzyMat3,centroids3,label3 = cluster_fuzzyCMeans.FCMMethod(speedData3,4,2,100)
auxiliaryFunc.saveToCsv(centroids3,"./output/FCM/第3类海拔下速度曲线的聚类中心.csv")
print("第4类海拔下的片段聚类")
fuzzyMat4,centroids4,label4 = cluster_fuzzyCMeans.FCMMethod(speedData4,4,2,100)
auxiliaryFunc.saveToCsv(centroids4,"./output/FCM/第4类海拔下速度曲线的聚类中心.csv")

print("所有片段聚类")
fuzzyMatAll,centroidsAll,labelAll = cluster_fuzzyCMeans.FCMMethod(speedData,4,2,100)
auxiliaryFunc.saveToCsv(centroidsAll,"./output/FCM/所有片段速度曲线的聚类中心.csv")

#拼接得到20类工况的聚类中心
pdCentroids0 = pd.DataFrame(centroids0,index=["c0","c1","c2","c3"],columns=["Vm","Pi","Pa","Pc"])
pdCentroids1 = pd.DataFrame(centroids1,index=["c4","c5","c6","c7"],columns=["Vm","Pi","Pa","Pc"])
pdCentroids2 = pd.DataFrame(centroids2,index=["c8","c9","c10","c11"],columns=["Vm","Pi","Pa","Pc"])
pdCentroids3 = pd.DataFrame(centroids3,index=["c12","c13","c14","c15"],columns=["Vm","Pi","Pa","Pc"])
pdCentroids4 = pd.DataFrame(centroids4,index=["c16","c17","c18","c19"],columns=["Vm","Pi","Pa","Pc"])
pdEleCentroids = pd.DataFrame(eleCentroids)
ele0 = pdEleCentroids[0][0]
ele1 = pdEleCentroids[0][1]
ele2 = pdEleCentroids[0][2]
ele3 = pdEleCentroids[0][3]
ele4 = pdEleCentroids[0][4]
pdCentroids0["Dh"] = [ele0,ele0,ele0,ele0]
pdCentroids1["Dh"] = [ele1,ele1,ele1,ele1]
pdCentroids2["Dh"] = [ele2,ele2,ele2,ele2]
pdCentroids3["Dh"] = [ele3,ele3,ele3,ele3]
pdCentroids4["Dh"] = [ele4,ele4,ele4,ele4]
pdcentroids = pdCentroids0.append(pdCentroids1).append(pdCentroids2).append(pdCentroids3).append(pdCentroids4)
# print("20类聚类中心")
auxiliaryFunc.saveToCsv(pdcentroids,"./output/FCM/20类工况的聚类中心.csv")

# 计算所有片段放在一起进行聚类时SOC平均消耗量C=4
centroidsAll = centroidsAll.tolist()
dataWithSOCAll = auxiliaryFunc.getColumn(origData,[1,2,9,11,13])
avgSOCAll = cluster_afterCluster.socAvg(dataWithSOCAll, centroidsAll)
auxiliaryFunc.saveToCsv(avgSOCAll,"./output/FCM/各类别SOC平均消耗量C=4.csv")

# 计算把片段划分到不同海拔下之后，各类别的SOC平均消耗量C=20
listCentroids = pdcentroids.values
dataWithSOC = auxiliaryFunc.getColumn(origData,[1,2,9,11,12,13])
avgSOC = cluster_afterCluster.socAvg(dataWithSOC, listCentroids)
pdAvgSOC = pdcentroids
pdAvgSOC["SOC"] = avgSOC
auxiliaryFunc.saveToCsv(pdAvgSOC,"./output/FCM/各类别SOC平均消耗量C=20.csv")










