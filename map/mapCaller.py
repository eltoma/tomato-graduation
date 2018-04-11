# -*- coding: utf-8 -*-


import requests
import json
import numpy as np
import pandas as pd
import googlemaps

gaodeMapKey = "4a6d7fc937cfd3d38a6ef3e8e259fbb5"
origin = "116.481028,39.989643"
destination = "116.434446,39.90816"
# 请求路径信息,返回steps
# origin:起点经纬度坐标
# destination:终点经纬度坐标
# gaodeMapKey:高德地图开发者密钥
def queryRoute(origin,destination,gaodeMapKey):
    url = "http://restapi.amap.com/v3/direction/driving"
    querystring = {
        "key":gaodeMapKey,
        "origin":origin,
        "destination":destination,
        "extensions":"all" # all
    }
    response = requests.request("Get", url, params = querystring)
    res = json.loads(response.text)
    steps = res["route"]["paths"][0]["steps"]
    return steps

# 解析steps，返回[{经度：，维度：，状态：},{},...]
# steps：路径信息中的steps
def analyseSteps(steps):
    global flag
    datas = []
    for step in steps:
        tmcs = step["tmcs"]
        for tmc in tmcs:
            status = tmc["status"]
            polyline = tmc["polyline"]
            coordinates = polyline.split(";")
            for coordinate in coordinates:
                longitude = coordinate.split(",")[0]
                latitude = coordinate.split(",")[1]
                data = {"longitude": longitude, "latitude": latitude, "status": status}
                datas.append(data)
    print(len(datas))
    (output,temp) = ([],[])
    for data in datas:
        for key,value in data.items():
            flag = False
            if(key,value) not in temp:
                flag = True
                break
        if flag:
            output.append(data)
        temp.extend(data.items())
    print(len(output))
    return output

# 根据经纬度调用Google地图，读取海拔
# longitude：经度
# latitude：维度
# googleMapKey：谷歌地图开发者密钥
googleMapKey = "AIzaSyATW2zfFWbHLlRoNMYs7Sa33iRpyjZOjAU"
locations = [116.481028,39.989643] # 这个locations格式好像有问题哦，
def getAltitude(locations,googleMapKey):
    # 需要代理，google的api被墙了
    proxies = { 
		"http": "http://127.0.0.1:1080",  
		"https": "http://127.0.0.1:1080",  
	}

    querystring = {
        "locations":"39.7391536,-104.9847034",
        "key":googleMapKey
    }
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    res = requests.get(url,params=querystring,proxies=proxies)
   
    print(res.text)
    # res = json.loads(response.text)
    # altitude = res
    # return altitude


if __name__ == "__main__":
    # steps = queryRoute(origin,destination,gaodeMapKey)
    # output = analyseSteps(steps)
    # output = pd.DataFrame(output)
    # with open("./经纬度序列.csv", "w", encoding="gbk") as f:
    #     f.write(output.to_csv())
    # print(output)
   getAltitude(locations,googleMapKey)





