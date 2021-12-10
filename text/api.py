import ssl, time, hashlib, string
from urllib import request, parse, error
from urllib.parse import quote

api_url = 'https://yspm.api.storeapi.net/pyi/87/206'
appid = '7311'  # 在后台我的应用查看
secret = '96012a26852b5d11cbbebb695b3ee004'  # 在后台我的应用查看
data = {
    'appid': '1',
    'format': 'json',
    'n_channel': '头条',
    'n_num': '40',
    'n_start': '0',
    'time': '1545829466',
}
data['appid'] = appid

data['time'] = round(time.time())  # 当前服务器时间
keysArr = list(data.keys())  # 取出字典key
keysArr.sort()  # 对字典key进行排序
md5String = ''
params = []
for key in keysArr:
    if data[key]:
        val = str(data[key])
        md5String += key + val
        params.append(key + "=" + val)
md5String += secret
m = hashlib.md5()
b = md5String.encode(encoding='utf-8')
m.update(b)
sign = m.hexdigest()

params.append('sign=' + sign)  # 加入计算后的sign值去请求
params = '&'.join(tuple(params))  # 把列表转成元组后用&分隔，最终转换成字符串 a=b&c=d&e=f

ssl._create_default_https_context = ssl._create_unverified_context
url = api_url + '?' + params
url = quote(url, safe=string.printable)
req = request.Request(url)
opener = request.build_opener()
r = opener.open(fullurl=req)

doc = r.read()
print(doc.decode('utf-8'))
