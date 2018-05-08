import auxiliaryFunc
import pandas as pd
import numpy as np
# list = [[1,2,3],[4,5,6],[7,8,9]]
# print(list)
# auxiliaryFunc.saveToCsv(list,"./test.csv")
# list1 = [0,1,2,3,4,5]
# print(list1)
# # print(list1[0:-1])
# # print(list1[-1])
#
# list2 = [2,3,1,4,5,0]
# print(list2)
# num = []
# for item in list1:
#     index = list2.index(item)
#     num.append(index)
# print(num)
#
# labels = [2,2,0,1,4,3,1,3,4]
# print(labels)
# for i in range(0,len(labels)):
#     if labels[i] == 0:
#         labels[i] = num[0]
#     elif labels[i] == 1:
#         labels[i] = num[1]
#     elif labels[i] == 2:
#         labels[i] = num[2]
#     elif labels[i] == 3:
#         labels[i] = num[3]
#     else:
#         labels[i] = num[4]
#
# print(labels)

datas = [{"head":"head0","tail":"tail0","distance":18,"status":"畅通"},
         {"head":"head1","tail":"tail1","distance":141,"status":"畅通"},
         {"head":"head2","tail":"tail2","distance":60,"status":"缓行"},
         {"head":"head3","tail":"tail3","distance":16,"status":"畅通"},
         {"head":"head4","tail":"tail4","distance":194,"status":"拥堵"},
         {"head":"head5","tail":"tail5","distance": 144, "status": "拥堵"}]

# 要分组成：
groups = [
    [
        {"head":"head0","tail":"tail0","distance":18,"status":"畅通"},
        {"head":"head1","tail":"tail1","distance":141,"status":"畅通"},
        {"head":"head2","tail":"tail2","distance":60,"status":"缓行"}
    ],
    [
        {"head":"head3","tail":"tail3","distance":16,"status":"畅通"},
        {"head":"head4","tail":"tail4","distance":194,"status":"拥堵"}
    ],
    [
        {"head":"head5","tail":"tail5","distance": 144, "status": "拥堵"}
    ]
]

# 先找到500米周期里面的head和tail，然后计算两点间的海拔差。
def group(datas):
    res = []
    dis = 0
    tmp = []
    for data in datas:
        tmp.append(data)
        dis += data['distance']
        print(dis)
        if (dis > 200):
            res.append(tmp)
            tmp = []
            dis = 0

    return res

res = group(datas)
print(res)
for re in res:
    origin = re[0]["head"]
    destination = re[-1]["tail"]
    print(origin)
    print(destination)


