# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:15:30 2017

@author: Tomato
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing
import auxiliaryFunc
np.set_printoptions(threshold = 1e6)

#==============================================================================
# 功能：传入片段特征（多个JSON文件），调用readJson批量读取文件
#       然后进行PCA分析，返回主成分、主成分方差、贡献率、相关性分析结果，保存为CSV文件
#       过程中拼接原始数据和主成分，进行相关性分析，保存csv文件
#path：JSON文件路径地址
#==============================================================================
def PCAMethod(path):
    origData = auxiliaryFunc.readJson("./input")
    #取除了Dh和SOC的其他前12个参数
    data = np.array(origData)[:,0:-2]
    #消除量纲的影响，将变量标准化
    scaledData = preprocessing.scale(data)
    #加载PCA算法，未设置主成分数目，默认为所有
    pca = PCA()
    #对原始数据进行降维，保存在reduced_X中
    #主成分
    reduced_X = pca.fit_transform(scaledData)  
    #方差，小数点后三位    
    variance = np.around(pca.explained_variance_,3) 
    #贡献率，小数点后三位
    percent = np.around(100*pca.explained_variance_ratio_,3)    
    
    #拼接特征参数变量和主成分变量
    allData = np.hstack((scaledData,reduced_X)) 
    # print(scaledData.shape)
    # print(reduced_X.shape)
    # print(allData.shape)
    allData = pd.DataFrame(allData)
    #相关性分析
    corre = allData.corr()                         
    
    print("主成分方差：")
    print(variance)
    print("贡献率")
    print(percent)
    
    reduced_X = pd.DataFrame(reduced_X)
    with open("./output/PCA/主成分.csv", "w", encoding="gbk") as f:
        f.write(reduced_X.to_csv())
    
    variance = pd.DataFrame(variance)    
    with open("./output/PCA/主成分方差.csv", "w", encoding="gbk") as f:
        f.write(variance.to_csv())
    
    percent = pd.DataFrame(percent)    
    with open("./output/PCA/贡献率.csv", "w", encoding="gbk") as f:
        f.write(percent.to_csv())
        
    with open("./output/PCA/特征参数间以及特征参数与主成分间相关分析.csv", "w", encoding="gbk") as f:
        f.write(corre.to_csv())
    
    return reduced_X, variance, percent,corre
    

if __name__ == "__main__":
    PCAMethod("./input")

