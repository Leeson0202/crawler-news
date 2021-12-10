import numpy as  np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

# file = r'E:\Code\news\文件\A7-训练数据样本.xls'
file = r'E:\Code\news\datas\数据集.xlsx'

import xlrd
import xlutils.copy
import os


def myplt(list):
    x = []
    y = []
    x_word = []
    n = 10  # -----------设置的最大字数 1000
    for i in range(n + 1):  # ------- n+1类
        x.append(i + 1)
        y.append(0)
        x_word.append('%d' % ((i + 1) * 100))
    for i in list:  # ----------遍历分类
        k = i // 100
        if k < n:  # ---- 0-n*100
            y[k] += 1
        else:  # -----大于n*100
            y[n] += 1
    plt.xticks(x, x_word[::], rotation=0)
    plt.bar(x, y)
    for a, b in zip(x, y):  # 柱子上的数字显示
        plt.text(a, b, "{}\n{:.2f}%".format(b,( b / len(list))*100), ha='center', va='bottom')
    plt.show()

    pass


if __name__ == '__main__':
    wb = xlrd.open_workbook(file,encoding_override='udf-8')
    list = []
    for sht in wb.sheets():  # ------遍历每个表
        print('Sheet:', sht.name)
        for row in range(sht.nrows):  # ---------遍历每一行
            values = []
            for col in range(sht.ncols):  # ----------每一行的几列
                values.append(sht.cell(row, col).value)
            if row != 0:
                list.append(len(values[0]))
    print(max(list))
    # array = np.array(list, dtype=np.int)
    # median = np.median(array)  # ------------中位数
    # myplt(list)
    #
    # a = 1

""":cvar
统计每一篇文章的字数
将字数进行分类 0-100 101-200 201-300 301-400 401-510 510--
字数平均数
字数中位数 

用可视化工具 显示字数分类


"""
