# 随机选出3个DNS

import random


def dns_select():
    dns_ip = ['8.8.8.8', '8.8.8.8', '8.8.8.8', '8.8.8.8']
    # dns_ip = ['116.57.77.213', '116.57.77.214', '116.57.77.215', '116.57.77.216']
    ip_selected = random.sample(dns_ip, 3)
    return ip_selected