# -*- coding: utf-8 -*-


#本模块提供一些辅助函数，如批量读取json文件、保存为CSV文件等等

import json
import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
np.set_printoptions(threshold = 1e6)


#==============================================================================
# 计算两个向量的欧式距离
#==============================================================================
def eculidDistance(vectA,vectB):
    return np.sqrt(np.sum(np.power(vectA-vectB,2)))

                
#==============================================================================
# 读取JSON文件，结果以列表形式返回
# path：要读取的放json文件的文件夹路径
#==============================================================================
def readJson(path):
    pathDir =  os.listdir(path)
    result=[]
    for allDir in pathDir:
        #print(allDir)
        data = []
        with open(os.path.join(path, allDir)) as f:
            for line in f:
                data.append(json.loads(line))
            for item in data:
                temp = list(item.values())[2:]
                result.append(temp)
        #print(allDir+" "+"success")
    return result

#==============================================================================
# 保存数据为CSV文件
# data:待保存的数据
# fileName:文件名
#==============================================================================
def saveToCsv(data,fileName):
    dfData = pd.DataFrame(data)
    with open(fileName, "w", encoding="gbk") as f:
        f.write(dfData.to_csv())
        

#==============================================================================
# 根据索引列表，获取输入数据的对应列，返回各列拼接之后的数据
# data:原始数据
# dataIndex:索引列表
#==============================================================================
def getColumn(data,dataIndex):
    data = np.array(data)
    points,attributes = data.shape
    result = data[:,dataIndex[0]]
    #一维数组使用转置、合并等，要指定shape，否则结果有异常
    result.shape = (points,1)
    if len(dataIndex) > 1:
        for i in range(1,len(dataIndex)):
            temp = data[:,dataIndex[i]]
            temp.shape = (points,1)
            result = np.hstack((result,temp))
    return result





    
# if __name__ == "__main__":
#     test = readJson("./input")
#     saveToCsv(test,"./resultShow/test.csv")
#     result = getColumn(test,[1,2,3])
#     saveToCsv(result,"./resultShow/test2.csv")

