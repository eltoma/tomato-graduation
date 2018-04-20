datas = [{"head":"head0","tail":"tail0","distance":18,"status":"畅通"},
         {"head":"head1","tail":"tail1","distance":141,"status":"畅通"},
         {"head":"head2","tail":"tail2","distance":60,"status":"缓行"},
         {"head":"head3","tail":"tail3","distance":16,"status":"畅通"},
         {"head":"head4","tail":"tail4","distance":194,"status":"拥堵"},
         {"head":"head5","tail":"tail5","distance": 144, "status": "拥堵"}]


def func(datas):
    res = []
    head = None
    dis = 0
    for data in datas:
        if(head == None):
            head = data['head']
        dis += data['distance']
        print(dis)
        if(dis > 200):
            temp = {}
            temp['head'] = head
            temp['tail'] = data['tail']
            res.append(temp)
            
            head = None
            dis = 0
    return res


print(func(datas))