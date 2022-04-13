# 性能测试
import time
import threading
import copy
import random
from main import db, init
from dnsSelect import dns_select
from resolve import rsv
from ruling import ruling


# 逻辑同main函数
def handler():
    global ERROR_NUM
    selected = dns_select()
    rm = selected[0]
    ip = selected[1]
    dns_ip = selected[2]
    rd = random.randrange(10)
    if rd < 4 and rd != rm:
        db(rd)
    if DNS_TYPE == 'A' or DNS_TYPE == 'NS' or DNS_TYPE == 'CNAME':
        res1 = []
        for i in range(3):
            try:
                if rd < 4 and ip[i] == dns_ip[rd]:
                    res1.append(['err'])
                else:
                    res1.append(rsv(ip[i], DOMAIN, DNS_TYPE))
            except Exception as e:
                ERROR_NUM += 1
        a1 = ruling(res1)
    elif DNS_TYPE == 'MX':
        res2 = []
        for i in range(3):
            try:
                if rd < 4 and ip[i] == dns_ip[rd]:
                    res2.append([['err1'], ['err2']])
                else:
                    res2.append(rsv(ip[i], DOMAIN, DNS_TYPE))
            except Exception as e:
                ERROR_NUM += 1
        res2_dp1 = copy.deepcopy(res2)
        res2_dp2 = copy.deepcopy(res2)
        preference = []
        for i in range(len(res2_dp1)):
            preference.append(res2_dp1[i][0])
        ruling(preference)
        exchange = []
        for i in range(len(res2_dp2)):
            for j in range(len(res2_dp2[i])):
                if j == 0:
                    continue
                else:
                    exchange.append(res2_dp2[i][j])
        ruling(exchange)


def run():
    global THREAD_NUM
    threads_list = []
    # 创建线程
    for k in range(THREAD_NUM):
        t = threading.Thread(target=handler)
        threads_list.append(t)
    # 开启线程
    start = time.time()
    for j in threads_list:
        j.start()
    for j in threads_list:
        j.join()
    end = time.time()
    print("==================性能测试结果==================")
    print('总运行时间：%s 秒' % (end - start))
    print('并发量：%s ' % (THREAD_NUM))
    print('平均处理时间(RT)：%s 秒' % ((end - start) / THREAD_NUM))
    print('每秒查询率(QPS)：%s q/s' % (THREAD_NUM / (end - start)))
    print('错误次数：%s 次' % (ERROR_NUM))


if __name__ == '__main__':
    # init()
    DOMAIN = 'baidu.com'    # 查询的域名
    DNS_TYPE = 'A'          # 域名记录类型
    THREAD_NUM = 500        # 并发量
    ERROR_NUM = 0           # 错误次数
    run()

