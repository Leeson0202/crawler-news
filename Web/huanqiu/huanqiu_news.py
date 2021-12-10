import json
import os
import time
from get_response import requests_get
import re

head = ['https://mil.huanqiu.com/api/list?node=%22/e3pmh1dm8/e3pmt7hva%22,%22/e3pmh1dm8/e3pmtdr2r%22,%22/e3pmh1dm8/e3pn62l96%22,%22/e3pmh1dm8/e3pn6f3oh%22&offset=',
        'https://mil.huanqiu.com/api/list2?node=/e3pmh1dm8/e3pn62l96&offset=',
        'https://auto.huanqiu.com/api/list?node=%22/e3pmh24qk/e3pmh25cs%22,%22/e3pmh24qk/e3pmtj57c%22,%22/e3pmh24qk/e3pmtkgc2%22,%22/e3pmh24qk/e3pn02mp3%22,%22/e3pmh24qk/e3pn4el6u%22,%22/e3pmh24qk/ej8aajlga%22,%22/e3pmh24qk/en0e9b249%22&offset=',
        'https://house.huanqiu.com/api/list?node=%22/e8nf57tcn/e8nf6ch75%22&offset=',
        'https://house.huanqiu.com/api/list2?node=/e8nf57tcn/e8nf6ch75&offset=',
        'https://auto.huanqiu.com/api/list2?node=/e3pmh24qk/e3pmh25cs&offset='
        ]
end = '&limit=20'
href='https://mil.huanqiu.com/article/'


# -----------------------------------------------------获取 新闻列表
def geturllist(url_one,tag):
    response = requests_get(url_one)
    response.encoding = response.apparent_encoding
    templist = []
    if response:
        retext = response.text.replace('\n', '')
        retext = retext.replace(' ', '')
        try:
            news_list = json.loads(retext)['list'][:-1]
            for i in news_list:
                templist.append([tag,i['title'],href+ i['aid']])
        except:
            pass
    return templist


def huanqiu_getnews():  # 获取新闻
    # ----------------------------------------开始爬取--获得列表
    stime = time.time()
    print('获取mil列表 500')
    newdetail_list = []
    for i in range(500):
        entime = time.time()
        tt = entime - stime
        print("\r{:}  {:>.1f}s".format(i, tt), end='    ')
        url = head[0] + str(i*20) + end
        newdetail_list.extend(geturllist(url,'军事'))
        url = head[1] + str(i*20) + end
        newdetail_list.extend(geturllist(url,'军事'))
        url = head[2] + str(i*20) + end
        newdetail_list.extend(geturllist(url,'汽车'))
        url = head[5] + str(i*20) + end
        newdetail_list.extend(geturllist(url,'汽车'))
        url = head[3] + str(i*20) + end
        newdetail_list.extend(geturllist(url,'房产'))
        url = head[4] + str(i*20) + end
        newdetail_list.extend(geturllist(url,'房产'))

    path_txt = 'datas/huanqiu/huanqiu.txt'
    if not os.path.exists(path_txt):  # --------判断文件是否存在
        open(path_txt, 'w')  # 自动创建一个
    # -------------------------------------读取 文件 用于判断是否重复f_list
    with open(path_txt, 'r', encoding='utf-8') as ftxt:
        f_list = ftxt.readlines()
    if f_list:  # ----------------------------------得到一个文件中的列表
        f_list = [i.strip().split('||||') for i in f_list ]

    # ----------------------------------------查找新的与文件你的重复项

    temp = newdetail_list
    newdetail_list = []
    count = len(temp)
    for i in temp:
        if i in f_list:
            count -= 1
            continue
        newdetail_list.append(i)

    # ----------------------------------------保存
    ftxt = open(path_txt, 'r+', encoding='utf-8')
    ftxt.seek(ftxt.seek(0, 2), 0)
    for i in newdetail_list:
        ftxt.write("%s||||%s||||%s\n" % (i[0], i[1],i[2]))
        ftxt.flush()
    ftxt.close()
    print("\nhuanqiu list finish! news = ", count)
