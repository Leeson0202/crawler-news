from requests import get
from random import choices

header_list = [
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"]


def get_response(url=None, proxies=None):
    try:
        # url = ''
        headers = {
            'User-Agent': choices(header_list)[0],
        }
        r = get(url, headers=headers,
                timeout=25)  # 伪装浏览器进行爬取
        r.raise_for_status()  # 自动检测爬虫状态=200
    except Exception as e:
        return None
    # r.encoding = r.apparent_encoding  # 转换格式
    r.encoding = 'utf-8'  # 转换格式
    return r  # 返回response


def requests_get(url=None, ip=None):
    """
    获取response并返回
    """
    if not url:
        return None
    # ip = '61.164.109.14:2'
    # proxies = {'http': 'http://{}'.format(ip),
    #            'https': 'hppts://{}'.format(ip)}
    n = 3

    for i in range(n):  # --------------- 三次
        response = get_response(url)
        if response:
            return response
        if i == n - 1:
            return None
