
head = 'https://mil.huanqiu.com/api/list?node=%22/e3pmh1dm8/e3pmt7hva%22,%22/e3pmh1dm8/e3pmtdr2r%22,%22/e3pmh1dm8/e3pn62l96%22,%22/e3pmh1dm8/e3pn6f3oh%22&offset='
end = '&limit=20'

import json
import os
from bs4 import BeautifulSoup
from get_response import requests_get
import re
import threading

url1 = 'https://www.sina.com.cn/'
head_url = """http://news.sina.com.cn/head/news20"""
m = 5
n = 31

# 财经、房产、教育、科技、军事、汽车、体育、游戏、娱乐和其他
# 新浪： 军事 汽车 房产 游戏

newdict = {'军事': ["军事"],
           '财经': ["财经", "股票", "基金", "外汇"],
           '科技': ["科技", "手机", "探索", "众测"],
           '体育': ["体育", "NBA", "超英", "中超"],
           '娱乐': ["娱乐", "明星", "电影", "星座", "高尔夫"],
           '汽车': ["汽车", "报价", "买车", "新车"],
           '房产': ["房产", "二手房", "家具"],
           '教育': ["教育", "留学", "公益", "佛教", "育儿"],
           '游戏': ["游戏", "手游", "超英", "中超"],
           '其他': ["其他", "收藏", "时尚", "女性", "医药"],
           }
url_dict = {
    '军事': 'https://mil.news.sina.com.cn/http://mil',
    '财经': "https://finance.sina.com.cn/http://finance",
    '科技': 'https://tech.sina.com.cn/http://tech',
    '体育': 'http://sports.sina.com.cn/https://sports',
    '娱乐': 'https://ent.sina.com.cn/http://ent',
    '汽车': 'https://auto.sina.com.cn/http://auto',
    '房产': ' https://bj http://bj',
    '教育': 'http://edu.sina.com.cn/https://edu',
    '游戏': 'https://games.sina.com.cn/http://games http://www.97973.com/',
    '其他': 'https://med http://med https://fashion http://fashion http://travel https://travel '
          'http://cul https://cul https://lottery http://lottery ',
}
url_dict_keys = url_dict.keys()
url_dict_values = url_dict.values()
threadlock = threading.Lock()  # 线程锁
thread_list = []


# -----------------------------------------------------获取 新闻列表
def geturlliist(url_one, id):
    response = requests_get(url_one)
    if response:
        if id == 1:  # ------------- 首页
            try:
                c = re.compile(
                    r'<a target="_blank" href="(.{10,100})">(.{3,50})</a></li>')
                list1 = c.findall(response.text)
                list1 = [list(i) for i in list1]
            except:
                list1 = []
                return list1
            return list1
        if id == 2:  # ----------------军事
            try:
                c = re.compile(
                    r'<a href="(.{10,100})" target="_blank">(.{10,80})</a>')
                list1 = c.findall(response.text)
                list1 = [list(i) for i in list1]
            except:
                list1 = []
                return list1
            return list1
        if id == 3:  # -------------------汽车
            try:
                c = re.compile(
                    r'<div class="stit"><a href="(.{10,100})" target="_blank">(.{10,80})</a></div>')
                list1 = c.findall(response.text)
                list1 = [list(i) for i in list1]
            except:
                list1 = []
                return list1
            return list1


def one(id):  # ------------------新闻首页大多数
    print()
    newdetail_list = []
    for mm in range(21, 22):
        for k in range(5, m + 1):
            for i in range(1, n + 1):
                url_am = head_url + str(mm) + ("{:0>2}".format(str(k)) if k < 10 else str(k)) + (
                    "{:0>2}".format(str(i)) if i < 10 else str(i)) + "am.shtml"
                url_pm = head_url + str(mm) + ("{:0>2}".format(str(k)) if k < 10 else str(k)) + (
                    "{:0>2}".format(str(i)) if i < 10 else str(i)) + "pm.shtml"
                list1 = geturlliist(url_am, id)
                print('\r历年新闻首页', mm, k, i, end=' ')
                if list1:
                    newdetail_list.extend(list1)
                    print('am', end=' ')
                list1 = geturlliist(url_pm, id)
                if list1:
                    newdetail_list.extend(list1)
                    print('pm', end='      ')
    return newdetail_list


def two(id):  # ----------------------------军事新闻
    newdetail_list = []
    # ------------------------------------------------军事首页（国内国外）
    print()
    head = 'http://mil.news.sina.com.cn/roll/index.d.html?cid=5791'
    for i in range(1, 26):
        print("\r军事首页\t", i, "/25  ", end='')
        url = head + '8&page=' + str(i)
        newdetail_list.extend(geturlliist(url, id))
        url = head + '9&page=' + str(i)
        newdetail_list.extend(geturlliist(url, id))
    # ----------------------------------------------------------------------------------json军事
    head = "http://interface.sina.cn/news/get_news_by_channel_new_v2018.d.json?cat_1=263326&level=1,2,3&page="
    end = "&show_num=10&callback=jQuery1910019561703174667766_1619608416490&_=1619608416492"
    head1 = "http://interface.sina.cn/news/get_news_by_channel_new_v2018.d.json?cat_1=70035&level=1,2&page="
    end1 = "&show_num=10&callback=jQuery19102723591824207987_1619611580296&_=1619611580297"
    print()
    for i in range(1, 101):  # 100
        content = ''
        print("\r军事json\t", i, "/100  ", end='')
        url = head + str(i) + end
        url1 = head1 + str(i) + end1
        txt = requests_get(url).text
        content = txt if txt[0:4] == 'jQue' else ''
        txt = requests_get(url1).text
        content = (content + txt) if txt[0:4] == 'jQue' else content
        # ----匹配
        rec = re.compile(
            r',"title":"(.{10,250})","url":"(.{10,200})","keywords"')
        temp = rec.findall(content)
        temp = [list(i) for i in temp]
        newdetail_list.extend([[i[1].replace("\\", ""), i[0].encode(
            'utf-8').decode('unicode_escape')] for i in temp])
    return newdetail_list


def three():  # -------------------------------------------------------汽车新闻
    newdetail_list = []
    # ------------------------------------------------汽车首页
    print()
    head0 = 'https://interface.sina.cn/auto/news/getWapNewsNewBycID.d.json?cid=78590&page='
    for i in range(1, 51):  # ---1,51
        print("\r汽车首页\t", i, "/50  ", end='')
        url = head0 + str(i) + '&limit=20&tagid=0'
        t = requests_get(url)
        txt = t.text if t else '       '
        content = ('[' + txt) if txt[0:4] == '{"st' else '['
        url = head0 + str(i) + '&limit=20&tagid=1'
        t = requests_get(url)
        txt = t.text if t else '       '
        content = (content + ',' + txt) if txt[0:4] == '{"st' else content
        url = head0 + str(i) + '&limit=20&tagid=2'
        t = requests_get(url)
        txt = t.text if t else '       '
        content = (content + ',' + txt) if txt[0:4] == '{"st' else content
        url = head0 + str(i) + '&limit=20&tagid=3'
        t = requests_get(url)
        txt = t.text if t else '       '
        content = (content + ',' + txt) if txt[0:4] == '{"st' else content
        content += ']'
        # -------匹配
        rec = json.loads(content)
        temp = []
        for i in rec:
            for j in i['data']:
                temp.append([j['pc_url'], j['title']])
        newdetail_list.extend(temp)
    return newdetail_list


def four():
    newdetail_list = []
    # ------------------------------------------------游戏首页
    print()
    head0 = 'https://interface.sina.cn/games/gpapi/2016index/2020_interface_game_pc_home_newslist.shtml?fid=1_'
    for i in range(1, 51):  # ---1,51
        print("\r游戏json\t", i, "/50  ", end='')
        url = head0 + '1&page=' + str(i)
        t = requests_get(url)
        txt = t.text[9:-1] if t else '       '
        content = ('[' + txt) if txt[0:4] == '{"re' else '['
        url = head0 + '3&page=' + str(i)
        t = requests_get(url)
        txt = t.text[9:-1] if t else '       '
        content = (content + ',' + txt) if txt[0:4] == '{"re' else content
        url = head0 + '4&page=' + str(i)
        t = requests_get(url)
        txt = t.text[9:-1] if t else '       '
        content = (content + ',' + txt) if txt[0:4] == '{"re' else content
        content += ']'
        # -------匹配
        rec = json.loads(content)
        del content
        del t
        temp = []
        txt = ''
        for i in rec:
            for j in i['result']['data']:
                if j:
                    txt += j.strip().replace(' ', '').replace("""
                    """, '')
        rec = re.compile(
            r'(https?://.{30,70}\.shtml).{10,40}"title="?(.{10,50})">')

        tt = rec.findall(txt)
        for i in tt:
            if list(i) not in temp and list(i) not in newdetail_list:
                temp.append(list(i))
        newdetail_list.extend(temp)
    return newdetail_list


def sina_getnews():  # 获取新闻
    # --------------------------------------------------开始爬取
    newdetail_list = []
    # newdetail_list.extend(one(1))  # ------新闻首页 大多数
    newdetail_list.extend(two(2))  # ------军事新闻
    newdetail_list.extend(three())  # ------汽车新闻
    newdetail_list.extend(four())  # ------游戏新闻

    # ------------------------------------------------- 打开文件 读取文件中的列表
    count = 0
    if not os.path.exists('datas/sina/sina.txt'):  # ---------------判断文件是否存在
        # 如果不存在这个logs文件夹，就自动创建一个
        open('datas/sina/sina.txt', 'w', encoding="utf-8")
    with open("datas/sina/sina.txt", "r+", encoding='utf-8') as ftxt:
        f_list = ftxt.readlines()
    if f_list:  # ----------------------------------得到一个文件中的列表
        f_list = [[j[0], j[1].strip(), j[2].strip()]
                  for i in f_list for j in [i.split('||||')]]
    # ------------------------------------将新的加入到列表
    end_list = []
    for i in newdetail_list:
        if 'http' not in i[0] or i[1] in ['国内新闻', '港澳台', 'MPV']:  # 初步过滤无用
            continue
        temp2 = i[0].split('.')[-1]
        temp1 = i[0].split('.')[0]
        if 'video' in i[0] or 'gif' in i[0] or 'collection' in i[0] or 'db.auto' in i[0] \
                or 'weibo' in i[0] or 'news' in temp1 or 'blog' in i[0] or 'tousu' in i[0] \
                or 'slide' in i[0] or 'lottery' in i[0] or 'zhongce' in i[0] or 'baby' in i[0] \
                or 'match' in i[0] or 'live' in i[0] or 'cn' in temp2 or 'zt_d' in i[0] \
                or 'ischool' in i[0]:  # 严格筛选
            continue
        # -------------------------------------用网址判断标签
        tag = ''
        temp = i[0].split('.')[0]
        for m, k in enumerate(url_dict_values):
            if temp in k:
                tag = list(url_dict_keys)[m]
                break
        temp = i[0].split('/')[3]
        if temp == 'tech':
            tag = '科技'
        new_ = [tag, i[0], i[1]]
        # ------------------------------------如果有标签 保存
        if tag and new_ not in f_list and new_ not in end_list:
            end_list.append(new_)
            count += 1

    ftxt = open('datas/sina/sina.txt', 'r+', encoding='utf-8')
    ftxt.seek(ftxt.seek(0, 2), 0)
    for i in end_list:
        ftxt.write("%s||||%s||||%s\n" % (i[0], i[1], i[2]))
        ftxt.flush()
    ftxt.close()
    print("\nsina list finish! news = ", count)
