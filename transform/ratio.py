import json
import xlrd
import xlwt
from xlutils.copy import copy
import os

path = '../datas/数据集.xlsx'
sheet_names = ['财经', '房产', '教育', '科技', '军事', '汽车', '体育', '游戏', '娱乐', '其他']


def read_book():
    workbook = xlrd.open_workbook(path, encoding_override='utf-8')  # 打开工作簿
    values = []
    for _ in range(10):
        worksheet = workbook.sheet_by_name(sheet_names[_])  # 获取第i个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        for i in range(1, rows_old):
            value = str(worksheet.cell_value(i, 0))  # 返回单元格中第一列的数据
            if value[-1] == '。':
                value = value[:-1]
            value = value.split("。")
            value = [len(i) for i in value]
            values.extend(value)
    return values


values = read_book()
v_len = [len(i) for i in values]
print()
