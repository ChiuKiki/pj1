# 压力测试
import time
import threading
import copy
from dnsSelect import dns_select
from resolve import rsv
from ruling import ruling


# 逻辑同main函数
def handler():
    global ERROR_NUM
    ip = dns_select()
    if DNS_TYPE == 'A' or DNS_TYPE == 'NS' or DNS_TYPE == 'CNAME':
        res1 = []
        for i in range(3):
            try:
                res1.append(rsv(ip[i], DOMAIN, DNS_TYPE))
            except Exception as e:
                ERROR_NUM += 1
        ruling(res1)
    elif DNS_TYPE == 'MX':
        res2 = []
        for i in range(3):
            try:
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
    print("==================压力测试结果==================")
    print('运行时间：%s 秒' % (end - start))
    print('并发量：%s ' % (THREAD_NUM))
    print('平均处理时间(RT)：%s 秒' % ((end - start) / THREAD_NUM))
    print('每秒能处理查询数目(QPS)：%s q/s' % (THREAD_NUM / ((end - start) / THREAD_NUM)))
    print('错误次数：%s 次' % (ERROR_NUM))


if __name__ == '__main__':
    DOMAIN = 'baidu.com'    # 查询的域名
    DNS_TYPE = 'A'          # 域名记录类型
    THREAD_NUM = 3000        # 并发量
    ERROR_NUM = 0           # 错误次数
    run()

