import numpy as np
import auxiliaryFunc
import pandas as pd

# 根据距离最小原则，判断某个数据点属于哪个类别，返回类别标签
# sample：待识别的数据点
# centroids：聚类中心
def categoryRecognize(sample,centroids):
    minDist = auxiliaryFunc.eculidDistance(sample, centroids[0])
    label = 0
    for i in range(1,len(centroids)):
        dist = auxiliaryFunc.eculidDistance(sample,centroids[i])
        if dist < minDist:
            minDist = dist
            label = i
    return label


#计算每个类别下的平均SOC
#dataWithSOC：带SOC变化量的数据列表
#center：20个聚类中心组成的dataframe
def socAvg(dataWithSOC,centroids):
    n = len(centroids)
    # print(n)
    soc = np.zeros(n)  # 存放每个类别下的SOC变化量数组
    count = np.zeros(n)  # 存放每个类别下的片段数

    for item in dataWithSOC:
        sample = item[0:-1]
        label = categoryRecognize(sample,centroids)
        soc[label] = soc[label] + item[-1]
        count[label] = count[label] + 1
    avgSoc = soc/count
    return avgSoc

#==============================================================================
# 根据类别标签将数据分类，返回分组对象
# data:待分组数据
# label:类别标签
#==============================================================================
def diviCategory(data,label):
    points,attributes = data.shape
    index = []
    for i in range(0,attributes):
        temp = "attr" + str(i)
        index.append(temp)
    index.append("类别")
    print(index)
    n,m = label.shape
    label.shape = (n,m)
    label = np.transpose(label)
    together = np.hstack((data,label))
    df = pd.DataFrame(together,columns=index)
    groups = df.groupby("类别")
    return groups
