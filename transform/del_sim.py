# path = '../datas/sina/sina.txt'
path = '../datas/tencent/tencent.txt'
# path = '../datas/huanqiu/huanqiu.txt'
ftxt = open(path, 'r+', encoding='utf-8')
new_list = ftxt.readlines()
new_list = [i.split('||||') for i in new_list]
print(len(new_list))
f_list = []
temp_list = []
for i in new_list:
    if i[1] not in temp_list:
        f_list.append(i)
        temp_list.append(i[1])

ftxt.seek(0, 0)
ftxt.truncate()  # 清空
for i in f_list:
    ftxt.write("%s||||%s" % (i[0], i[1]))
    # ftxt.write("%s||||%s||||%s" % (i[0], i[1], i[2]))
    ftxt.flush()
print(len(f_list))
ftxt.close()
