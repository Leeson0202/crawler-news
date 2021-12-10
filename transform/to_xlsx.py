import json
import xlrd
import xlwt
from xlutils.copy import copy
import os

path = 'datas/数据集.xlsx'
sheet_names = [ '财经','房产','教育','科技','军事', '汽车', '体育', '游戏', '娱乐', '其他']


def write_excel_xls(path, i, value):
    workbook = xlrd.open_workbook(path,encoding_override='utf-8')  # 打开工作簿
    worksheet = workbook.sheet_by_name(sheet_names[i])  # 获取第i个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(i)  # 获取转化后工作簿中的第i个表格
    index = len(value)  # 获取需要写入数据的行数
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xlsx格式表格写入数据成功！")

def openf(path):
    with open(path, 'r', encoding='utf-8') as f:
        temp_list=json.load(f)
    return temp_list
def get_values():
    values = [[], [], [], [], [], [], [], [], [], []]
    all_list = []
    all_list.extend(openf('datas/tencent/tencent.json'))
    all_list.extend(openf('datas/sina/sina.json'))
    all_list.extend(openf('datas/people/people.json'))
    all_list.extend(openf('datas/game/game.json'))
    all_list.extend(openf('datas/huanqiu/huanqiu.json'))
    all_list.extend(openf('datas/other/other.json'))
    for i in all_list:
        index = sheet_names.index(i['channelName'])
        if i:
            values[index].append([i['content'], i['channelName'], i['title'],i['href']])
    return values


def to_xlsx():
    # 判断文件是否存在
    # if os.path.exists(path):
    #     os.remove(path)
    if not os.path.exists(path):
        workbook = xlwt.Workbook(encoding='utf-8')  # 新建一个工作簿
        for i in sheet_names:
            sheet = workbook.add_sheet(i)
            for j in range(4):
                sheet.write(0, j, ['content', 'channelName', 'title', 'href'][j])  # 像表格中写入数据（对应的行和列
        workbook.save(path)  # 保存工作簿
    values = get_values()
    print(sum([len(i) for i in values]))
    for i, value in enumerate(values):
        write_excel_xls(path, i, value)

