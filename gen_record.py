# 生成重复数据文件
def gen():
    domain = 'baidu.com'
    type = 'A'
    num = 1000
    path = 'record_' + str(num) +'.txt'
    with open(path, 'a') as f:
        for i in range(num):
            f.write(domain + ' ' + type + '\n')

if __name__ == '__main__':
    gen()
