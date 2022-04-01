# 主程序
from dnsSelect import dns_select
from resolve import resolve
from ruling import ruling
import copy
import time


domain = input('输入查询域名(DNS记录类型若为CNAME则需要加上www.):')
dnsType = input('请输入DNS记录类型(A,MX,NS,CNAME)：')
ip = dns_select()

if dnsType == 'A':
    start = time.time()
    res_A = []
    for i in range(3):
        res_A.append(resolve(ip[i], domain, dnsType))   # 三个DNS服务器解析的A记录结果
    a1 = ruling(res_A)      # 大数裁决
    if a1 == 0:
        print('Error')
    else:
        print(res_A[a1])
    end = time.time()
    print('运行时间：%s 秒' % (end-start))

elif dnsType == 'MX':
    start = time.time()
    MSbackp = []
    for i in range(3):
        MSbackp.append(resolve(ip[i], domain, dnsType))
    print(MSbackp)
    MSbackpc = copy.deepcopy(MSbackp)  # 不改变MSbackp，深复制
    MSbackpd = copy.deepcopy(MSbackp)
    MSbackppre = []
    MSbackpexc = []
    for i in range(len(MSbackpc)):
        MSbackppre.append(MSbackpc[i][0])
    a2 = ruling(MSbackppre)
    for i in range(len(MSbackpd)):
        for j in range(len(MSbackpd[i])):
            if j == 0:
                continue
            else:
                MSbackpexc.append(MSbackpd[i][j])
    a3 = ruling(MSbackpexc)
    if a2 == 0 or a3 == 0:
        print('Error')
    else:
        print("优先级  |  服务器地址")
        for i in range(len(MSbackp[a2][0])):
            print(MSbackp[a2][0][i], end="")
            print("      |   ", end="")
            print(MSbackp[a3][1][i])
    end = time.time()
    print('运行时间：%s 秒' % (end - start))

elif dnsType == 'NS':
    start = time.time()
    NSback = []
    for i in range(3):
        NSback.append(resolve(ip[i], domain, dnsType))
    a4 = ruling(NSback)
    if a4 == 0:
        print('Error')
    else:
        print(NSback[a4])
    end = time.time()
    print('运行时间：%s 秒' % (end - start))

elif dnsType == 'CNAME':
    start = time.time()
    CNAMEback = []
    for i in range(3):
        CNAMEback.append(resolve(ip[i], domain, dnsType))
    a5 = ruling(CNAMEback)
    if a5 == 0:
        print('Error')
    else:
        print(CNAMEback[a5])
    end = time.time()
    print('运行时间：%s 秒' % (end - start))

else:
    print('输入错误')
