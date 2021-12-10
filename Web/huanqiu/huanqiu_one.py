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
    response = requests_get(new_one[2])
    if response is None:  # 如果没有爬到 直接返回
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    # -----------------------------------------------提取内容
    div = soup.find_all(name='section', attrs={'data-type': 'rtext'})
    if not div:
        div = soup.find_all(name='div', attrs={'class': 'l-con clear'})
    if not div:
        return
    del response

    contents = ''
    datalist = div[0].find_all('p')
    if datalist:
        for i, newtext in enumerate(datalist):
            temp_text = newtext.text.strip()
            temp_text = temp_text if '】' not in temp_text[:42] else temp_text[temp_text.index('】')+1:]
            contents += temp_text.strip()

    del datalist, div, soup
    contents = contents.replace("\n", '')
    if len(contents) > 32000:
        return
    # # ----------------------------------------------转化为类
    if len(contents) > 45:
        new = New(title=new_one[1], channelName=new_one[0], content=contents, href=new_one[2])
        SaveNew(new, fjson, percent, stime)


def huanqiu_getone():
    print('获取mil详细详细')
    path_txt = 'datas/huanqiu/huanqiu.txt'
    path_json = 'datas/huanqiu/huanqiu.json'
    if os.path.exists(path_json):  # ---------------存在 就 删除
        os.remove(path_json)
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
    print('huanqiu news succesful!')
