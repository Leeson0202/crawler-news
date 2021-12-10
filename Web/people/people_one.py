import os
import random
import threading
import time

from NewClass import New
from bs4 import BeautifulSoup
from get_response import requests_get
from SaveNew import SaveNew

threadlock = threading.Lock()  # 线程锁
thread_list = []


def detail(new_one, fjson, percent, stime):
    # new_one[1]='http://politics.people.com.cn/n1/2021/0430/c1001-32092393.html'
    response = requests_get(new_one[1])
    if response is None:  # 如果没有爬到 直接返回
        # print("\n\r{:>3.0f}%".format(percent))
        return
    response.encoding='GBK'

    soup = BeautifulSoup(response.text, 'html.parser')  # -----------------深度提取文本开始
    # ------------------------------------------------提取标题
    div = soup.find_all(name='div', attrs={'class': 'col col-1 fl'})
    title = soup.find_all('h1')
    title_pre = ''
    t = ''
    if not title:
        title = soup.find_all('h2')[0].text
    else:
        t = soup.find_all('h3')  # 小标题
        if len(t) == 1:
            title_pre = t[0].text
        elif len(t) > 2:
            title_pre = t[len(t) - 2].text
            if title_pre == '旗下网站':
                title_pre = t[len(t) - 1].text
        else:
            title_pre = ''
        title = title[len(title) - 1].text
        title = title_pre + title
        if not title:
            return
    del t, title_pre, response
    # ------------------------提取内容
    # print(new_one[1].strip())
    if not div:
        div = soup.find_all(name='div', attrs={'class': 'box_con'})
        if not div:
            div = soup.find_all(name='div', attrs={'class': 'fl text_con_left'})
        if not div:
            div = soup.find_all(name='div', attrs={'class': 'rm_txt_con cf'})
        if not div:
            div = soup.find_all(name='div', attrs={'class': 'show_text'})
        if not div:
            div = soup.find_all(name='div', attrs={'class': 'text_wz'})
        if not div:
            div = soup.find_all(name='div', attrs={'class': 'artDet'})
        if not div:
            div = soup.find_all(name='div', attrs={'class': 'd2txt clearfix'})
        if not div:
            div = soup.find_all(name='div', attrs={'class': 'content clear clearfix'})
        if div:
            datalist = div[0].find_all('p')
        else:
            return
    else:
        datalist = div[len(div) - 1].find_all('p')
    # datalist=[i.text.strip() for i in datalist]
    # # -----------------------------------------------循环每一行
    contents = ''
    j = 1
    temp = ''
    for j in datalist:
        try:  # -----------------------------提取 内容
            temp = j.text.strip()
        except:
            temp = ''
        temp = str(temp)
        if '本报' in temp or '人民网' in temp or '新华社'in temp or '记者' in temp\
                or '吴谦' in temp or '图片来源' in temp :
            continue
        # ------------------------判断是否为结尾项
        if '分享让更多人看到' == temp or '相关新闻' in temp:
            break
        else:
            contents = contents + temp
    del j, datalist, temp, div, soup
    contents = contents.replace("\n", '')
    if len(contents)>32000:
        return
    # # ----------------------------------------------转化为类
    if len(contents) > 45:
        new = New(title=title, channelName=new_one[0], content=contents, href=new_one[1])
        SaveNew(new, fjson, percent, stime)


def people_getone():
    if not os.path.exists('datas/people/people.json'):  # ---------------判断文件是否存在
        open('datas/people/people.json', 'w', encoding="utf-8")  # 如果不存在，就自动创建一个
    with open("datas/people/people.txt", 'r', encoding='utf-8') as f:
        news_list = f.readlines()
    # ----------------------------------初始化json文件
    fjson = open('datas/people/people.json', 'r+', encoding='utf-8')
    fjson.seek(0, 0)
    if fjson.read() == '':
        fjson.truncate()  # 清空
        fjson.writelines('[')  # 初始化 并保持
        fjson.flush()
    stime = time.time() # ---------运行开始时间

    for i, newline in enumerate(news_list):  # ----------------------  循环每一行 多线程
        temp = newline.strip()
        # temp = random.choice(news_list)  # ----------测试
        percent = (i / len(news_list)) * 100  # 进度百分比
        if temp:
            temp = temp.split('||||')
        # detail(temp, fjson, percent, stime)  # 进入解析解析页面
        # ----------------------------------------- 多线程进入
        t = threading.Thread(target=detail, args=(temp, fjson, percent, stime))
        thread_list.append(t)
    num = 1000  # 设置的线程数
    t = None
    for i, t in enumerate(thread_list):
        try:
            t.start()
        except Exception as e:
            pass
        while len(threading.enumerate()) > num:
            time.sleep(0.2)
    for t in thread_list:
        t.join()
    fjson.seek(fjson.seek(0,2)-1,0)
    fjson.write(']')
    fjson.flush()
    fjson.close()
