# 主程序
from dnsSelect import dns_select
from resolve import rsv
from ruling import ruling
import copy
import time
import random


def main(domain, dnsType):
    ip = dns_select()
    rd = random.randrange(10)   # 随机生成出错的DNS服务器的ip下标，出错概率为3/10
    if dnsType == 'A' or dnsType == 'NS' or dnsType == 'CNAME':
        res1 = []
        for i in range(3):
            try:
                if i == rd:     # 随机错误
                    res1.append(['err'])
                else:
                    res1.append(rsv(ip[i], domain, dnsType))  # 三个DNS服务器解析的A记录结果
            except Exception as e:
                print('Error:', e)
        a1 = ruling(res1)       # 大数裁决
        if a1 == 0:
            print('系统错误')
        else:
            print(res1[a1])

    elif dnsType == 'MX':
        # 解析MX记录
        res2 = []
        for i in range(3):
            try:
                if i == rd:     # 随机错误
                    res2.append([['err1'], ['err2']])
                else:
                    res2.append(rsv(ip[i], domain, dnsType))
            except Exception as e:
                print('Error:', e)
        # print(res2)
        # 深复制：res2_dp1、res2_dp2与res2相同，但不改变res2
        res2_dp1 = copy.deepcopy(res2)
        res2_dp2 = copy.deepcopy(res2)
        # 取出优先级记录，进行大数裁决
        preference = []
        for i in range(len(res2_dp1)):
            preference.append(res2_dp1[i][0])
        a2 = ruling(preference)
        # 取出邮件服务器记录，进行大数裁决
        exchange = []
        for i in range(len(res2_dp2)):
            for j in range(len(res2_dp2[i])):
                if j == 0:
                    continue
                else:
                    exchange.append(res2_dp2[i][j])
        a3 = ruling(exchange)
        # 打印结果
        if a2 == 0 or a3 == 0:
            print('系统错误')
        else:
            print("优先级  |  服务器地址")
            for i in range(len(res2[a2][0])):
                print(res2[a2][0][i], end="")
                print("      |   ", end="")
                print(res2[a3][1][i])

    else:
        print('输入错误')


if __name__ == '__main__':
    domain = input('输入查询域名(DNS记录类型若为CNAME则需要加上www.):')
    dnsType = input('请输入DNS记录类型(A,MX,NS,CNAME)：')
    start = time.time()  # 开始计时
    main(domain, dnsType)
    end = time.time()  # 结束计时
    print('运行时间：%s 秒' % (end - start))
