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
            rec = re.compile(r'"url":"(.{50,100})",')
            templist = rec.findall(response.text)
        except:
            templist = []
            return templist
    return templist


def tencent_getnews():  # 获取新闻
    # ----------------------------------------开始爬取--获得列表
    newdetail_list = []
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=milite&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:2,%22check_type%22:true}'
    newdetail_list.extend([['军事', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=finance&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['财经', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=nstock&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['财经', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=tech&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['科技', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=digi&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['科技', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=ent&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['娱乐', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=auto&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['汽车', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=house&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['房产', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=edu&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['教育', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=games&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['游戏', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=sports&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:14,%22check_title%22:0,%22check_type%22:true}'
    newdetail_list.extend([['体育', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=sports&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['体育', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=lifes&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=pet&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=pet&srv_id=pc&offset=1&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=rushidao&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url='https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=visit&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url='https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=zfw&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22hot%22],%22is_filter%22:2,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url='https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=astro&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url='https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=comic&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url='https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=emotion&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])
    url='https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=health&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    newdetail_list.extend([['其他', i.strip()] for i in geturllist(url)])


    errorlist = []

    if not os.path.exists('datas/tencent/tencent.txt'):  # --------判断文件是否存在
        open('datas/tencent/tencent.txt', 'w')  # 自动创建一个
    # -------------------------------------读取 文件 用于判断是否重复f_list
    with open('datas/tencent/tencent.txt', 'r', encoding='utf-8') as ftxt:
        f_list = ftxt.readlines()
    if f_list:  # ----------------------------------得到一个文件中的列表
        f_list = [[j[0],j[1].strip()] for i in f_list for j in [i.split('||||')] ]

    # ----------------------------------------查找新的与文件你的重复项
    temp = newdetail_list
    newdetail_list = []
    count = len(temp)
    for i in temp:
        if i in f_list:
            count-=1
            continue
        newdetail_list.append(i)

    # ----------------------------------------保存
    ftxt = open('datas/tencent/tencent.txt', 'r+', encoding='utf-8')
    ftxt.seek(ftxt.seek(0,2),0)
    for i in newdetail_list:
        ftxt.write("%s||||%s\n" % (i[0], i[1]))
        ftxt.flush()
    ftxt.close()
    print("tencent list finish! news = ",count)
