# 随机选出3个DNS
import copy
import redis


def dns_select():
    dns_ip = ['8.8.8.8', '8.8.4.4', '1.2.4.8', '210.2.4.8']
    # dns_ip = ['116.57.77.213', '116.57.77.214', '116.57.77.215', '116.57.77.216']
    # redis数据库中找出被攻击次数最多的DNS服务器
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    server = r.zrevrange("server_zset", 0, 0)
    print('所有DNS服务器ip：' + str(dns_ip))
    print('有序集合(\'值\', 分数)：' + str(r.zrevrange("server_zset", 0, -1, withscores=True)))
    print('出错最多的服务器：'+str(server[0]))
    rm = -1
    if server[0] == 'server_0':
        rm = 0
    elif server[0] == 'server_1':
        rm = 1
    elif server[0] == 'server_2':
        rm = 2
    elif server[0] == 'server_3':
        rm = 3
    dns_ip_cp = copy.deepcopy(dns_ip)
    del(dns_ip_cp[rm])
    print('动态选择结果：'+str(dns_ip_cp))
    return rm, dns_ip_cp, dns_ip


if __name__ == '__main__':
    dns_select()
