# -*- coding: utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import json

'''
提取平均速度Vm，驻车比例Pi，加速比例Pa，匀速比例Pc特征

Parameters
------------
speedCurve: 速度序列， 以1s为间隔
ct: 周期，单位为s

return： [...,[Vm, Pi, Pa, Pc],...]
'''
def getFeature(speedCurve, ct):
    ps = pd.Series(speedCurve)
    res = []
    for i in range(0, ps.size, ct):
        seg = ps[i: i+ct]
        print(seg)
        Vm = seg.mean()

        park = seg[seg == 0]
        unpark = seg[seg != 0]
        Pi = park.size / seg.size

        # 查分求加速度序列
        a = seg.diff().fillna(0)
        acc = a[a > 0]
        const = a[a == 0]

        Pa = acc.size / seg.size
        Pc = const.size / seg.size

        # 平均速度Vm，驻车比例Pi，加速比例Pa，匀速比例Pc
        res.append([Vm, Pi, Pa, Pc])
    return res

    res = getFeature([1,2,3,4,5,6], 2)
    print(res)


        


        
