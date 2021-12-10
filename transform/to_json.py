import json
import os
import time
count = 0
max = 0
sheet_names = ['财经', '房产', '教育', '科技', '军事', '汽车', '体育', '游戏', '娱乐', '其他']
f_path = '../datas/数据集.json'


def openf(path):
    global count,max
    with open(path, 'r', encoding='utf-8') as f:
        temp_list = json.load(f)
    temp_list = [
        {"content": "%s" % (i['title'] + '。' + i['content']), "label": "%s" % (sheet_names.index(i['channelName']))} for
        i in temp_list]
    llist = temp_list
    temp_list=[]
    for i in llist:
        if len(i['content'])<8000:
            temp_list.append(i)
        else:
            if len(i['content'])>max:
                max =len(i['content'])
            count+=1
    return temp_list


def get_datas_content_label_list():
    st = time.time()
    datas = []
    datas.extend(openf('../datas/tencent/tencent.json'))
    datas.extend(openf('../datas/sina/sina.json'))
    datas.extend(openf('../datas/people/people.json'))
    datas.extend(openf('../datas/game/game.json'))
    datas.extend(openf('../datas/huanqiu/huanqiu.json'))
    datas.extend(openf('../datas/other/other.json'))
    et = time.time()
    return datas, et - st


def init_json():
    if os.path.exists(f_path):
        os.remove(f_path)
    if not os.path.exists(f_path):
        open(f_path, 'w', encoding='utf-8')
    return


def get_json_datas(f_json_path):
    with open(f_json_path, 'r', encoding='utf-8') as f:
        datas = json.load(f)
    for i in datas:
        index = i['content'].index('。')
        yield i['content'][:index], i['content'][index + 1:], i['label']


def main():
    # -----------------------写入json
    datas,t=get_datas_content_label_list()  # 获取数据
    init_json()          # 初始化json文件
    f_json = open(f_path,'r+',encoding='utf-8')
    json.dump(datas, f_json)
    f_json.close()
    print(max,count)
    # ------------------读取json
    # ts = time.time()
    # t = get_json_datas('../datas/a.json')
    # tn = time.time() - ts
    # print(tn)
    # for i in range(10):
    #     a,b,c = next(t)
    #     print(type(c))
    #     print(a,b,c)


main()
