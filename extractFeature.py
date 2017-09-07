# -*- coding: utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import json

def getdatetime(dt):
    return datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S.%f')


def getreldatetime(dt1, dt2):
    return (dt2 - dt1).seconds


def touniformdata(df):
    # "quadratic" 二次插值，1S钟采样一次
    return df.resample('1S').asfreq().interpolate(method="quadratic")

def extractfeature(seg):
    fa = {}
    # print(seg)

    acc = seg[seg['加速度'] > 0]
    dece = seg[seg['加速度'] < 0]
    constant = seg[seg['加速度'] == 0]

    park = seg[seg['速度'] == 0]
    unpark = seg[seg['速度'] != 0]

    fa['start'] = seg.head(1).index[0].strftime('%H-%M-%S')
    fa['end'] = seg.tail(1).index[0].strftime('%H-%M-%S')

    fa['Vmax'] = seg['速度'].max()
    fa['Vm'] = seg['速度'].mean()

    fa['Pi'] = park.index.size / seg.index.size

    fa['Vmr'] = unpark['速度'].mean()

    fa['Aa'] = acc['加速度'].mean() if acc.index.size != 0 else 0
    fa['Ad'] = dece['加速度'].mean() if dece.index.size != 0 else 0

    fa['Vsd'] = seg['速度'].std()

    fa['Amax'] = seg['加速度'].max()
    fa['Amin'] = seg['加速度'].min()

    fa['Pa'] = acc.index.size / seg.index.size
    fa['Pd'] = dece.index.size / seg.index.size
    fa['Pc'] = constant.index.size / seg.index.size

    return fa
"""
提取特征并输出为文件
每一个片段输出三个文件：
    1. 特征数据 .json
    2. 原始数据 .csv
    3. 图(t-v, t-a) .png
    
Parameters
------------
file: 文件路径
sheet: 表单名
sliceSize: 片段长度，单位：秒
outdice: 输出文件的目录
"""
def dealfeaturextra(file, sheet, sliceSize, outdict):
    df = pd.read_excel(file, index_col="时间", sheetname=sheet, parse_dates=True,)
    dfs = df.resample('1S').asfreq().interpolate()
    dfs['加速度'] = dfs['速度'].diff().fillna(0)
    filename = file.split("/").pop()
    filename = filename[0: filename.index(".")]
    prefix = outdict + "/" + filename + " "
    plt.rcParams['font.family'] = 'SimHei'

    for i in range(0, dfs.index.size, sliceSize):
        # 切出片段
        seg = dfs[i: i + sliceSize]

        # 去掉最后一个不完整的片段
        if seg.index.size < sliceSize:
            return

        # print("slice's offset is:", i)
        fa = extractfeature(seg)
        json_fa = json.dumps(fa)

        with open("%s%s至%s.%s" % (prefix, fa['start'], fa['end'], 'json'), 'w', encoding="utf-8") as f:
            f.write(json_fa)

        with open("%s%s至%s.%s" % (prefix, fa['start'], fa['end'], 'csv'), "w", encoding='gbk') as f:
            f.write(seg.to_csv())

        plt.figure()


        plt.subplot(2, 1, 1)
        plt.plot(seg.index, seg['速度'])
        plt.xlabel("时间(s)")
        plt.ylabel("速度(km/h)")
        plt.grid(True)


        plt.subplot(2, 1, 2)
        plt.plot(seg.index, seg['加速度'])
        plt.xlabel("时间(s)")
        plt.ylabel("加速度(km/h*s)")
        plt.grid(True)

        plt.savefig("%s%s至%s" % (prefix, fa['start'], fa['end']), dpi=1000)
        plt.close()

        print("progress：", "%2.2f" % (i * 100 / dfs.index.size), "%")

def main():
    dealfeaturextra("./inputData/0613WL0035ttt.xlsx", "片段一", 120, outdict="./output")
    return 0

if __name__ == "__main__":
    main()
