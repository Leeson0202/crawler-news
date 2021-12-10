import requests

urllist = [
    'https://www.thepaper.cn/load_index.jsp?nodeids=90069,&channelID=102407&topCids=,&pageidx=',
    'https://www.thepaper.cn/load_index.jsp?nodeids=25448,26609,25942,26015,25599,25842,80623,26862,25769,25990,26173,26202,26404,26490,&channelID=25953&topCids=,12781942&pageidx=60',
    'http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/life_4.jsonp?cb=t&cb=life',
    'https://shankapi.ifeng.com/shanklist/_/getColumnInfo/_/default/6800586942321791589/1621387567000/20/14-35083-/getColumnInfoCallback?callback=getColumnInfoCallback&_=16215141719923',
    'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=tech&srv_id=pc&offset=200&limit=20&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
]

response = requests.get(urllist[0])
response.encoding = response.apparent_encoding
with open('text.html', 'w', encoding='utf-8') as f:
    f.writelines(response.text)

# url =   'https://new.qq.com/rain/a/20210503A05MNT00'
# url = 'https://new.qq.com/omn/20210503/20210503A05MNT00.html'
# url = 'https://new.qq.com/omn/20210503/20210503A05MMZ00.html'
# response = requests.get(url)
# with open('text.html', 'w', encoding='utf-8') as f:
#     f.writelines(response.text)

# strt = '【17173鲜游快报，专注于快速带来全球新游信息】RockstarGames、2KGames等著名厂'
# re = '】'
# m = strt if re not in strt else strt[strt.index(re)+1:]
# print(m)
