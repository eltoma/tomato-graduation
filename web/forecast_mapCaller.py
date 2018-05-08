# -*- coding: utf-8 -*-


import requests
import json
import numpy as np
import pandas as pd
import cluster_afterCluster

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
    print("总距离：" + res["route"]["paths"][0]["distance"])
    print("地图预计行驶时间：" + res["route"]["paths"][0]["duration"])
    # print()
    return steps

# 解析steps，返回[{经度：，维度：，状态：},{},...]
# steps：路径信息中的steps
def analyseRoute(steps):
    global flag
    datas = []
    for step in steps:
        tmcs = step["tmcs"]
        for tmc in tmcs:
            status = tmc["status"]
            distance = tmc["distance"]
            polyline = tmc["polyline"]
            coordinates = polyline.split(";")
            head = coordinates[0]
            tail = coordinates[-1]
            data = {"head":head,"tail":tail,"distance":distance,"status":status}
            datas.append(data)
            # for coordinate in coordinates:
            #     longitude = coordinate.split(",")[0]
            #     latitude = coordinate.split(",")[1]
            #     data = {"longitude": longitude, "latitude": latitude, "status": status}
            #     datas.append(data)
    # print(len(datas))
    # (output,temp) = ([],[])
    # for data in datas:
    #     for key,value in data.items():
    #         flag = False
    #         if(key,value) not in temp:
    #             flag = True
    #             break
    #     if flag:
    #         output.append(data)
    #     temp.extend(data.items())
    # print(len(output))
    return datas

# 根据经纬度调用Google地图，读取海拔
# locations：经纬度坐标，格式："latitude,longitude"
# googleMapKey：谷歌地图开发者密钥

def getElevation(locations,googleMapKey):
    # 需要代理，google的api被墙了
    proxies = {
		"http": "http://127.0.0.1:1080",
		"https": "http://127.0.0.1:1080",
	}
    # locations = latitude + "," + longitude
    # 谷歌地图请求时是纬度在前经度在后
    tmp = locations.split(",")
    newLocations = tmp[-1] + "," + tmp[0]
    querystring = {
        "locations":newLocations,
        "key":googleMapKey
    }
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    response = requests.get(url,params=querystring,proxies=proxies)
    res = json.loads(response.text)
    elevation = res["results"][0]["elevation"]
    return elevation


def getDistance(origin,destination,gaodeMapKey):
    url = "http://restapi.amap.com/v3/direction/driving"
    querystring = {
        "key":gaodeMapKey,
        "origin":origin,
        "destination":destination,
        "extensions":"all" # all
    }
    response = requests.request("Get", url, params = querystring)
    res = json.loads(response.text)
    distance = res["route"]["paths"][0]["distance"]
    distance = int(distance)
    return distance


if __name__ == "__main__":
    gaodeMapKey = "4a6d7fc937cfd3d38a6ef3e8e259fbb5"
    origin = "116.481028,39.989643"
    destination = "116.434446,39.90816"

    googleMapKey = "AIzaSyATW2zfFWbHLlRoNMYs7Sa33iRpyjZOjAU"
    longitude = "116.481028"
    latitude = "39.989643"

    steps = queryRoute(origin,destination,gaodeMapKey)
    output = analyseRoute(steps)
    print(output)
    output = pd.DataFrame(output)
    with open("./经纬度序列.csv", "w", encoding="gbk") as f:
        f.write(output.to_csv())

    # getElevation(longitude,latitude,googleMapKey)





