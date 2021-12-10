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
    # new_one[1]='https://new.qq.com/omn/20210430/20210430A0EGYK00.html'
    response = requests_get(new_one[1])
    if response is None:  # 如果没有爬到 直接返回
        return
    # ----------注意编码
    # response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')  # -----------------深度提取文本开始
    # ------------------------------------------------提取标题
    title = soup.find_all('h1')
    if not title:
        return
    title = title[0].text.strip()

    # -----------------------------------------------提取内容
    # print(new_one[1].strip())
    div = soup.find_all(name='div', attrs={'class': 'news_txt'})
    if not div:
        div = soup.find_all(name='div', attrs={'class': 'news_txt'})
    if not div:
        return
    del response

    div=div[0]
    contents = ''
    try:
        if div.text:
            contents=div.text
    except:
        pass

    contents = contents.replace("\n", '')
    contents = contents.replace(u'\xa0', u' ')
    if '本文来' in contents:
        contents = contents[:contents.index('本文来')-1]
    if len(contents) > 32000:
        return
    # # # ----------------------------------------------转化为类
    if len(contents) > 45:
        new = New(title=title, channelName=new_one[0], content=contents, href=new_one[1])
        SaveNew(new, fjson, percent, stime)


def other_getone():
    path_txt = 'datas/other/other.txt'
    path_json = 'datas/other/other.json'
    if not os.path.exists(path_json):  # ---------------判断文件是否存在
        open(path_json, 'w', encoding="utf-8")  # 如果不存在，就自动创建一个
    with open(path_txt, 'r', encoding='utf-8') as f:
        news_list = f.readlines()
    # ----------------------------------初始化json文件
    fjson = open(path_json, 'r+', encoding='utf-8')
    fjson.seek(0, 0)
    if fjson.read() == '':
        fjson.truncate()  # 清空
        fjson.writelines('[')  # 初始化 并保持
        fjson.flush()
    stime = time.time()  # ---------运行开始时间

    for i, newline in enumerate(news_list):  # ----------------------  循环每一行 多线程
        temp = newline.strip()
        # temp = random.choice(news_list).strip()  # ----------测试
        percent = (i / len(news_list)) * 100  # 进度百分比
        if temp:
            temp = temp.split('||||')
        # detail(temp, fjson, percent, stime)  # 进入解析解析页面
        # ----------------------------------------- 加入多线程
        t = threading.Thread(target=detail, args=(temp, fjson, percent, stime))
        thread_list.append(t)
    num = 1000  # 设置的线程数
    t = None
    for i, t in enumerate(thread_list):
        try:
            t.start()
        except Exception as e:
            print(e)
        while len(threading.enumerate()) > num:
            time.sleep(0.2)
    for t in thread_list:
        t.join()

    fjson.seek(fjson.seek(0, 2) - 1, 0)
    fjson.write(']')
    fjson.flush()
    fjson.close()
