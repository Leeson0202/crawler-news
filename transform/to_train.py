import random
import json

fjson='../datas/数据集.json'
f1 = '../datas/a.json'
f2 = '../datas/b.json'
f3 = '../datas/c.json'
list1=[]
list2=[]
list3=[]

with open(fjson,'r',encoding='utf-8') as f:
    datas = json.load(f)
for i in datas:
    print(type(i))
    t = random.random()
    if t<0.8:
        list1.append(i)
    elif t>=0.9:
        list2.append(i)
    else:
        list3.append(i)
with open(f1,'w',encoding='utf-8') as f:
    json.dump(list1,f)
with open(f2,'w',encoding='utf-8') as f:
    json.dump(list2,f)
with open(f3,'w',encoding='utf-8') as f:
    json.dump(list3,f)
