from json import dumps
import threading
import time

threadlock = threading.Lock()

def save(new_detail, f_json):
    try:
        # ----------------------------------写入json 文件
        f_json.seek(f_json.seek(0, 2) , 0)
        f_json.write('\n' + new_detail + ',')
        # f_json.seek(0, 0)  # 文件指针移动到头部
        # if f_json.read() == '[]':  # 判断 是否为空
        #     f_json.seek(f_json.seek(0, 2) - 1, 0)
        #     f_json.write(new_detail + ']')
        # else:  # 不为空
        #     f_json.seek(f_json.seek(0, 2) - 1, 0)
        #     f_json.write(',\n' + new_detail + ']')
    except :
        pass
    finally:
        f_json.flush()


def SaveNew(new, fjson, percent, stime):
    new_detail = dumps(new.__dict__)
    threadlock.acquire()  # 加个同步锁就好了
    save(new_detail, fjson)# 将单词对象 转化为json格式
    threadlock.release()
    end = time.time()
    print('\r{:>3.0f}%  {:>.1f}s  \t'.format(
        percent, end - stime), end='')  # 显示进度
    return
