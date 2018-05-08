import numpy as np
from sklearn import preprocessing
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import auxiliaryFunc
np.set_printoptions(threshold = 1e6)

matplotlib.rcParams["font.family"] = "STSong"
#matplotlib.rcParams["font.size"] = 20



#==============================================================================
# 初始化模糊矩阵
# n：数据点个数（如本应用中的718）
# k：聚类个数
#==============================================================================
def initWithFuzzyMat(n,k):
    fuzzyMat=np.mat(np.zeros((k,n)))
    for colIndex in range(n):
        memDegreeSum=0
        randoms=np.random.rand(k-1,1)
        for rowIndex in range(k-1):
            fuzzyMat[rowIndex,colIndex]=randoms[rowIndex,0]*(1-memDegreeSum)
            memDegreeSum+=fuzzyMat[rowIndex,colIndex]
        fuzzyMat[-1,colIndex]=1-memDegreeSum
    return fuzzyMat

#==============================================================================
# 计算聚类中心
# dataSet：用于聚类的数据
# fuzzyMat：隶属度矩阵
# p：加权指数，一般为2
#==============================================================================
def calCentWithFuzzyMat(dataSet,fuzzyMat,p):
    n,m=dataSet.shape
    k=fuzzyMat.shape[0]
    centroids=np.mat(np.zeros((k,m)))
    for rowIndex in range(k):
        degExpArray=np.power(fuzzyMat[rowIndex,:],p)
        denominator=np.sum(degExpArray)
        numerator=np.array(np.zeros((1,m)))
        for colIndex in range(n):
            numerator+=dataSet[colIndex]*degExpArray[0,colIndex]
        centroids[rowIndex,:]=numerator/denominator
    return centroids

#==============================================================================
# 计算隶属度矩阵
# dataSet：用于聚类的数据
# centroids：聚类中心
# p：加权指数，一般取2
#==============================================================================
def calFuzzyMatWithCent(dataSet,centroids,p):
    n,m=dataSet.shape
    c=centroids.shape[0]
    fuzzyMat=np.mat(np.zeros((c,n)))
    for rowIndex in range(c):
        for colIndex in range(n):
            d_ij=auxiliaryFunc.eculidDistance(centroids[rowIndex,:],dataSet[colIndex,:])
            fuzzyMat[rowIndex,colIndex]=1/np.sum([np.power(d_ij/auxiliaryFunc.eculidDistance(centroid,dataSet[colIndex,:]),2/(p-1)) for centroid in centroids])
    return fuzzyMat

#==============================================================================
# 计算目标函数值
# dataSet：用于聚类的数据
# fuzzyMat：隶属度矩阵
# centroids：聚类中心
# p：加权指数，一般取2
#==============================================================================
def calTargetFunc(dataSet,fuzzyMat,centroids,k,p):
    n,m=dataSet.shape
    c=fuzzyMat.shape[0]
    targetFunc=0
    for rowIndex in range(c):
        for colIndex in range(n):
            targetFunc+=auxiliaryFunc.eculidDistance(centroids[rowIndex,:],dataSet[colIndex,:])**2*np.power(fuzzyMat[rowIndex,colIndex],p)
    return targetFunc
    

#==============================================================================
# 功能：进行模糊C均值聚类，返回隶属度矩阵、聚类中心、类别标签
# data：要进行聚类的数据
# n_clusters：聚类中心个数
# p：加权指数，一般取2
# interMax：最大迭代次数
#==============================================================================
def FCMMethod(data,n_clusters,p,interMax):
    points,attributes = data.shape

    #保留原始数据的均值和方差，用于反标准化
    mean = data.mean(axis = 0) 
    std = data.std(axis = 0)
    
    #为消除量纲，聚类前进行标准化
    scalData = preprocessing.scale(data)

    #初始化隶属度矩阵
    fuzzyMat = initWithFuzzyMat(points,n_clusters)  
    #根据初始化的隶属度矩阵计算聚类中心
    centroids = calCentWithFuzzyMat(scalData,fuzzyMat,p)
    #计算初始目标函数
    targetFunc = calTargetFunc(scalData,fuzzyMat,centroids,n_clusters,p)
    interCounter = 0
    while (True):
        fuzzyMat = calFuzzyMatWithCent(scalData,centroids,p)
        centroids = calCentWithFuzzyMat(scalData,fuzzyMat,p)
        nowTargetFunc = calTargetFunc(scalData,fuzzyMat,centroids,n_clusters,p)
        #print(targetFunc-nowTargetFunc)
        if (targetFunc-nowTargetFunc<=0.0001) or (interCounter>=interMax):
            print("聚类结束")
            break
        targetFunc = nowTargetFunc
        interCounter = interCounter + 1
        print(interCounter)
    #聚类中心反标准化
    for i in range(0,attributes):
        centroids[:,i] = centroids[:,i]*std[i] + mean[i]
        
    #计算类别标签矩阵
    label = fuzzyMat.argmax(0)
        
    return fuzzyMat,centroids,label