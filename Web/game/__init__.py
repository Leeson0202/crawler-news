import os
import random
import re
import json
import threading
import time

from NewClass import New
from get_response import requests_get
from SaveNew import SaveNew

head = 'http://interface.17173.com/content/list.jsonp?callback=jQuery111105449853679787608_1621514817116&categoryIds=10019%2C10152%2C10161&pageSize=500&pageNo='
end = '&_=1621514817118'


def game_getone_detail(stime):
    news = []
    for i in range(1, 60):
        entime = time.time()
        tt = entime - stime
        print("\r{:}  {:>.1f}s".format(i, tt), end='    ')
        url = head + str(i) + end
        response = requests_get(url)
        if not response:
            continue
        page_data = json.loads(response.text[42:-1])
        datas = page_data['data']
        error = '】'

        temp = [
            [j['title'], '游戏',
             j['content'] if error not in j['content'][:40] else j['content'][j['content'].index(error) + 1:],
             j['pageUrl']]
            for j in datas]
        news.extend(temp)
    print()
    return news


def get_gameone():
    stime = time.time()
    path = '../../datas/game/game.json'
    if os.path.exists(path):  # ---------------判断文件是否存在
        os.remove(path)

    if not os.path.exists(path):  # ---------------判断文件是否存在
        # 如果不存在这个logs文件夹，就自动创建一个
        f = open(path, 'w', encoding="utf-8")
        f.write('[')
        f.flush()
        f.close()

    # --------打开文件 读取列表
    fjson = open(path, "r+", encoding='utf-8')
    news = game_getone_detail(stime)
    # ---------------------------将新的新闻加入json里面
    for index, i in enumerate(news):
        percent = (index / len(news)) * 100
        new = New(i[0], i[1], i[2], i[3])
        SaveNew(new, fjson, percent, stime)

    fjson.seek(fjson.seek(0, 2) - 1, 0)
    fjson.write(']')
    fjson.flush()
    fjson.close()


get_gameone()
