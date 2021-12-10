import os
import random
import re
import threading
import time

from NewClass import New
from bs4 import BeautifulSoup
from get_response import requests_get
from SaveNew import SaveNew

threadlock = threading.Lock()  # 线程锁
thread_list = []


def detail(new_one, fjson, percent, stime):
    # new_one[1] = 'http://sports.sina.com.cn/g/pl/2017-12-12/doc-ifypnqvn3400219.shtml'
    url_error = ['ku/movie', 'driving/']
    for _ in url_error:
        if _ in new_one[1]:
            return
    response = requests_get(new_one[1])
    if response is None:  # 如果没有爬到 直接返回
        # print("\n\r{:>3.0f}%".format(percent))
        return
    if '�' in response.text:
        response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')  # -----------------深度提取文本开始
    if '//bj' in new_one[1]:
        res = soup.find_all(name='div', attrs={'id': 'editHTML'})
        if not res:
            res = soup.find_all(name='div', attrs={'class': 'l_articleMain'})
        if res:
            soup = res[0]
        else:
            return
    if '//auto.sina' in new_one[1]:
        res = soup.find_all(name='div', attrs={'class': 'article clearfix', 'id': 'artibody'})
        if not res:
            res = soup.find_all(name='div', attrs={'class': 'article clearfix', 'id': 'artibody'})
        if not res:
            res = soup.find_all(name='div', attrs={'id': 'articleContent'})
        if not res:
            res = soup.find_all(name='div', attrs={'class': 'page-content clearfix article_14'})
        if not res:
            res = soup.find_all(name='div', attrs={'class': 'article-content-left fL'})
        if not res:
            res = soup.find_all(name='div', attrs={'id': 'artibody'})
        if not res:
            res = soup.find_all(name='div', attrs={'class': 'bd'})
        if not res:
            res = soup.find_all(name='div', attrs={'class': 'adv-con'})
        if not res:
            res = soup.find_all(name='body')
            pass
        if res:
            soup = res[0]
        else:
            return
    if '//edu.sina' in new_one[1] or '//travel.sina' in new_one[1]:
        res = soup.find_all(name='div', attrs={'id': 'artibody'})
        if res:
            soup = res[0]
        else:
            return
    if 'ent' in new_one[1]:
        res = soup.find_all(name='div', attrs={'id': 'artibody'})
        if res:
            soup = res[0]
    if 'sports' in new_one[1]:
        res = soup.find_all(name='div', attrs={'id': 'artibody'})
        if res:
            soup = res[0]

    data_lines = soup.find_all('p')

    if not data_lines:
        return
    # ------------------------------------------------------------------删除中间变量 并解析
    del soup, response
    # -----------------------------------------------循环每一行
    contents = ''
    for index_a, j in enumerate(data_lines):
        temp = ''
        try:
            class_tagg = j.attrs['class']
            if class_tagg == 'cmnt_text':
                continue
        except:
            pass
        okk = False  # ------------------删除无无效项
        try:
            if '感知中国经济的真实温度' in j.contents[0].next:
                okk = True
        except:
            pass
        judge = j.text.strip()

        sort_isTrue = ['article_', '感知中国经济的真实温度', '环球', '观察者', '福利贴', '股市瞬息万变',
                       '欢迎关注', '安装新浪财经', '上证报中国', '文/', '记者', '作者', '吴谦', '中新网',
                       '中国日报', '相关报道', '直播吧', '参考消息', '微信公众号', '文|', '�',
                       '防务新闻', '上海证券', '推荐阅读', '郭普晖', '相关阅读', '证券时报', '南华早报',
                       '房产频道', '最新回应', '主播介绍', '【', '稿件来自', '本文来自', 'StartFragment',
                       '新浪港股大赛', '中国基金报', '留学生家长！改', '点击进入', '更多车型相对论',
                       '不再自动弹出'
                       ]
        long_isTrue = ['股市瞬息万变', '原标题', '原题', '来源', '摘自', '欢迎关注', '相关阅读', '推荐阅读',
                       '感知中国经济的真实温度', '线索征集', '微博关注', '【投资维权315线索征集】', '52亿！',
                       '北京晨报讯', '长江商报', '安装新浪财经客户端', '撰文', '我要投票', '点击投诉', '点此报名',
                       '市场赚钱效应升温', '每日经济新闻', '每经App登载', '点击查看', '点击看详情',
                       '更多外观细节',
                       ]
        if judge:
            for mm in sort_isTrue:
                if mm in judge and len(judge) < 30:
                    okk = True
                del mm
            for mm in long_isTrue:
                if mm in judge and len(judge) < 120:
                    okk = True
                del mm

        if 'article_' in judge or okk:
            continue
        del judge
        try:  # -----------------------------提取 内容 到temp
            temp = j.text.strip()
        except:
            try:
                temp = j.contents[0].text.strip()
            except:
                continue
        if '<p' in temp or 'font' in temp:
            try:
                temp = j.contents[0].text.strip()
            except:
                continue
        if not temp:
            try:
                temp = j.text.strip()
            except:
                continue
        get_end = [
            '中新经纬客户端', '新浪科技讯', '新浪数码讯', '新浪体育讯', '新浪娱乐讯', '新浪乐居讯',
            '新浪财经讯', '上证报讯', '北京晨报讯', '新浪科技', '新浪数码', '新京报讯', '新浪教育讯',
            '新浪手机讯', '新浪汽车讯', '新浪汽车讯'

        ]
        for mm in get_end:
            if mm in temp and len(temp) > len(mm) + 1:  # 连接的取后
                if mm in temp[:len(mm) + 2]:
                    temp = temp[len(mm):]
        del mm, get_end
        temp = str(temp).strip()
        if index_a < 3:
            rec = re.compile(r'\[.{2,20}\]')
            head = rec.match(temp)
            if head:
                temp = temp[len(head.group(0)):]
            rec = re.compile(r'（.{2,20}）')
            head = rec.match(temp)
            if head:
                temp = temp[len(head.group(0)):]
            rec = re.compile(r'\(.{2,5}\n?.{1,10}\)')
            head = rec.match(temp)
            if head:
                temp = temp[len(head.group(0)):]
            del rec, head

        # ------------------------判断是否为结尾项
        end_tag = [
            "责任编辑", "责编", 'Copyright', '更多汽车资讯', '电话：', 'article_adlistarticle_adlist',
            '微信搜索', '留言板', '监制', '更多娱乐', '更多内容', '为您推荐', '扫描二维码关注',
            '搜索微信', '微信公众号', '推荐阅读', '版权所有', '本次试驾车型', '招募', '已收藏',
            '[详情]', '免责声明', '新浪财经股吧', '三步报志愿', '更多简介', '旅游频道业务合作',
            '贵州省最小', '更多猛料！', '关注观察者网', '微信ID', '新浪财经股民投诉平台由新浪财经运营',
            '[详细]', '专注苹果新闻报道', '新浪汽车讯', '想和全国各地成千上万网友一起畅聊购车用车经验',
            '更多消息', '有想法，', '文章关键词', '想了解更多', '评天下游', '新浪声明：', '相关新闻',
            '精彩推荐', '是由新浪游戏推出', '下一页','新浪简介','About Sina','往期回顾','标签：',
            '标签:',
        ]

        okk = False
        for mm in end_tag:
            if mm in temp:
                okk = True

        if okk:
            break
        else:
            contents = contents + temp.strip()
    del data_lines, temp, j, sort_isTrue, long_isTrue, index_a
    if len(contents) > 32000 or '�' in contents:
        return
    # ----------------------------------------------转化为类
    if len(contents) > 65:
        new = New(title=new_one[2], channelName=new_one[0], content=contents, href=new_one[1])
        SaveNew(new, fjson, percent, stime)


def sina_getone():
    if os.path.exists('datas/sina/sina.json'):
        os.remove('datas/sina/sina.json')
    if not os.path.exists('datas/sina/sina.json'):  # ---------------判断文件是否存在
        open('datas/sina/sina.json', 'w', encoding="utf-8")  # 如果不存在，就自动创建一个
    with open("datas/sina/sina.txt", 'r', encoding='utf-8') as f:
        news_list = f.readlines()
    fjson = open('datas/sina/sina.json', 'r+', encoding='utf-8')

    fjson.seek(0, 0)
    if fjson.read() == '':
        fjson.truncate()  # 清空
        fjson.writelines('[')  # 初始化 并保持
        fjson.flush()
    stime = time.time()

    for i, newline in enumerate(news_list):  # ----------------------  循环每一行 多线程
        # if i >= 10000:
        #     break
        # temp = random.choices(news_list)[0].strip()
        # if '//auto.' not in newline and '//huanqiu.' not in newline:
        #     continue
        # if '其他' not in newline[:5]:
        #     continue
        temp = newline.strip()
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
            time.sleep(1)
    for t in thread_list:
        t.join()

    fjson.seek(fjson.seek(0, 2) - 1, 0)
    fjson.write(']')
    fjson.flush()
    fjson.close()
