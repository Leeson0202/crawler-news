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
        # print("\n\r{:>3.0f}%".format(percent))
        return
    # ----------注意编码
    response.encoding = 'GBK'
    # if response.apparent_encoding == 'GB2312':
    #     response.encoding = 'Gb2312'
    # else:
    #     response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')  # -----------------深度提取文本开始
    # ------------------------------------------------提取标题
    title = soup.find_all('h1')
    t1 = title
    if not title:
        new_one[1] = 'https://new.qq.com/rain/a/' + new_one[1].split('/')[-1][:-6]
        response = requests_get(new_one[1])
        if response is None:  # 如果没有爬到 直接返回
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find_all('h1')
        if not title:
            return
    title = title[0].text.strip()

    # -----------------------------------------------提取内容
    # print(new_one[1].strip())
    div = soup.find_all(name='div', attrs={'class': 'content-article'})
    # print(new_one)
    if not div:
        return
    del response

    contents = ''
    datalist = div[0].find_all('p')
    end_tag = [
        '【版权声明】','未经授权','记者','编辑','来源','原创文章','文|','转载','编辑',
        '来源','欢迎点击','监制','END','责编','完','作者','核 查 员','欢迎在评论区',
        '更多新闻资讯'
    ]
    if datalist:
        for i, text in enumerate(datalist):
            ok = False
            for _ in end_tag:
                if _ in text.text:
                    ok = True
            if (i < 2 and len(text.text.strip()) < 10) or ok:
                continue
            contents += text.text.strip()

    del datalist, div, soup
    contents = contents.replace("\n", '')
    if len(contents) > 32000:
        return
    # # # ----------------------------------------------转化为类
    if len(contents) > 45:
        new = New(title=title, channelName=new_one[0], content=contents, href=new_one[1])
        SaveNew(new, fjson, percent, stime)


def tencent_getone():
    if not os.path.exists('datas/tencent/tencent.json'):  # ---------------判断文件是否存在
        open('datas/tencent/tencent.json', 'w', encoding="utf-8")  # 如果不存在，就自动创建一个
    with open("datas/tencent/tencent.txt", 'r', encoding='utf-8') as f:
        news_list = f.readlines()
    # ----------------------------------初始化json文件
    fjson = open('datas/tencent/tencent.json', 'r+', encoding='utf-8')
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
