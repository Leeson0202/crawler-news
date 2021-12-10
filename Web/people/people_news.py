import os
from get_response import requests_get
import re

# 财经、房产、教育、科技、军事、汽车、体育、游戏、娱乐和其他
# 人民网： 军事 汽车 房产 游戏

url_dict = {
    '军事': 'http://military.',  # --
    '财经': "http://money. http://finance. http://okooo. 彩票 ",  # --,
    '科技': 'http://it. http://scitech. 科技 http://tc. 通信',  # --
    '体育': 'http://sports.people.com.cn/news_sitemap.xml',  # --
    '娱乐': 'http://ent. http://travel. 旅游',  # --
    '汽车': 'http://auto.',  # --
    '房产': 'http://house.',  # --
    '教育': 'http://edu.',  # --
    '游戏': 'http://game.',  # --
    '其他': 'http://politics. 政治 http://energy. 能源 http://ccnews. http://legal. 法律'
          'http://culture. 文化 http://society. 社会 http://media. 媒体 http://theory 党政'
          'http://opinion. 观点 http://env. 环境 http://gongyi. 公益 http://art. 艺术'
          'ttp://book. 书 http://shipin. 食品 http://health. 健康  http://ip. 知识产权'
          'http://dangjian. 党建 http://dangshi. 党史 '
          'http://yuqing. 疫情 http://hm. 港澳 http://lady. 时尚 http://hongmu. 红木',
}

url_dict_keys = url_dict.keys()
url_dict_values = url_dict.values()


# -----------------------------------------------------获取 新闻列表
def geturlliist(url_one):
    response = requests_get(url_one)
    if response:
        try:
            rec = re.compile(r'<loc>(.{10,80})</loc>')
            list1 = rec.findall(response.text)
        except:
            list1 = []
            return list1
        return list1


def gettag(tlist): # ---------打标签函数
    tolist=[]
    for i in tlist:
        tag = ''
        temp = i.split('.')[0]
        for m, k in enumerate(url_dict_values):
            if temp in k:
                tag = list(url_dict_keys)[m]
                break
        if 'http://sh.' in i or 'http://he.' in i:
            continue
        if tag == '':
            continue
        tolist.append([tag, i])
    return tolist

def people_getnews():  # 获取新闻
    # ----------------------------------------开始爬取--获得列表
    newdetail_list = []
    tolist = []
    url = 'http://www.people.cn/sitemap_index.xml'
    response = requests_get(url)
    rec = re.compile('<loc>(.{10,50})</loc>')
    if rec:
        templist = rec.findall(response.text)
    else:
        return
    # -----------------------------直接打标签
    tolist.extend(gettag(templist))

    url='http://www.people.com.cn/' # ------------------------爬取首页的url
    response = requests_get(url)
    rec=re.compile(r'href="(http:.{15,70}[0-9]{5,15}\.html)"')
    templist=rec.findall(response.text)
    taged_list=gettag(templist)
    del  rec, response, url,templist

    if not os.path.exists('datas/people/people.txt'):  # --------判断文件是否存在
        open('datas/people/people.txt', 'w')  # 自动创建一个
    # -------------------------------------读取 文件 f_list
    f_list=[]
    with open('datas/people/people.txt', 'r', encoding='utf-8') as ftxt:
        f_list = ftxt.readlines()
    if f_list: #----------------------------------得到一个文件中的列表
        f_list = [[j[0], j[1].strip()] for i in f_list for j in [i.split('||||')]]

    # ------------------------------------------分别进行爬取
    for i in tolist:
        newlist = geturlliist(i[1])  # -----分别爬取每一页 得到一页的链接
        if not newlist:
            continue
        for j in newlist:
            newdetail_list.append([i[0], j])
    newdetail_list.extend(taged_list) # 将首页更新的内容加入list

    f_list.extend(newdetail_list)
    count = len(newdetail_list)
    del i, j, newlist, tolist

    # ----------------------------------------查找新的与文件你的重复项
    count=len(newdetail_list)
    errorlist = []  # 去掉文件里的重复项
    for _ in newdetail_list:
        if _ in newdetail_list:
            count-=1
            continue
        errorlist.append(_)
    newdetail_list = errorlist

    # ----------------------------------------保存
    ftxt = open('datas/people/people.txt', 'r+', encoding='utf-8')
    ftxt.seek(ftxt.seek(0,2),0)
    for i in newdetail_list:
        ftxt.write("%s||||%s\n" % (i[0], i[1]))
        ftxt.flush()
    ftxt.close()
    print("people list finish! news = ",count)

