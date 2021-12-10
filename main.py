import time
from Web.sina.sina_news import sina_getnews
from Web.sina.sina_one import sina_getone
from Web.people.people_news import people_getnews
from Web.people.people_one import people_getone
from Web.tencent.tencent_news import tencent_getnews
from Web.tencent.tencent_one import tencent_getone
from transform.to_xlsx import to_xlsx
from Web.huanqiu.huanqiu_news import huanqiu_getnews
from Web.huanqiu.huanqiu_one import huanqiu_getone
from Web.other.other_news import other_getnews
from Web.other.other_one import other_getone

# t = time.time()
# --------------------------------新浪
# sina_getnews() # 历年新闻已经爬好了（注）
# sina_getone()
# -------------------------------人民网
# people_getnews()
# people_getone()
# -------------------------------环球
# huanqiu_getnews()
# huanqiu_getone()
# ----------------------------- other
# other_getnews()
# other_getone()
# -------------------------------腾讯
# while 1:
#     print('--------------')
#     t = time.time()
#     tencent_getnews()  # 每天爬几次
#     print("%.3f s"%(time.time()-t))
#     time.sleep(20*60)
# tencent_getone()
# # ----------------------------------json转xlsx
to_xlsx() # 以追加的方式
# input()

