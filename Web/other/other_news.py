import os
from get_response import requests_get
import re
import operator


# 财经、房产、教育、科技、军事、汽车、体育、游戏、娱乐和其他
# 腾讯： 军事 汽车 房产 游戏


# -----------------------------------------------------获取 新闻列表
def geturllist(url_one):
    response = requests_get(url_one)
    response.encoding = response.apparent_encoding
    templist = []
    if response:
        try:
            rec = re.compile(r'<a href="(.{10,50})" id=')
            templist = rec.findall(response.text)
        except:
            return templist
        templist = ['https://www.thepaper.cn/' + i for i in templist]
    return templist


def other_getnews():  # 获取新闻
    # ----------------------------------------开始爬取--获得列表
    newdetail_list = []
    url_h = 'https://www.thepaper.cn/load_index.jsp?nodeids=25448,26609,25942,26015,25599,25842,80623,26862,25769,25990,26173,26202,26404,26490,&channelID=25953&topCids=,12781942&pageidx='
    url_h = 'https://www.thepaper.cn/load_index.jsp?nodeids=90069,&channelID=102407&topCids=,&pageidx='
    for i in range(100):
        print('\r',i,end='   ')
        url = url_h + str(i)
        newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    errorlist = []

    if not os.path.exists('datas/other/other.txt'):  # --------判断文件是否存在
        open('datas/other/other.txt', 'w')  # 自动创建一个
    # -------------------------------------读取 文件 用于判断是否重复f_list
    with open('datas/other/other.txt', 'r', encoding='utf-8') as ftxt:
        f_list = ftxt.readlines()
    if f_list:  # ----------------------------------得到一个文件中的列表
        f_list = [[j[0], j[1].strip()] for i in f_list for j in [i.split('||||')]]

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
    ftxt = open('datas/other/other.txt', 'r+', encoding='utf-8')
    ftxt.seek(ftxt.seek(0, 2), 0)
    for i in newdetail_list:
        ftxt.write("%s||||%s\n" % (i[0], i[1]))
        ftxt.flush()
    ftxt.close()
    print("other list finish! news = ", count)
