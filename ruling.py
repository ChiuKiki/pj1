# 大数裁决
# 输入：三个DNS服务器的解析结果数组
# 输出：裁决结果在解析结果数组的哪个下标

def ruling(a):
    for i in range(len(a)):
        a[i].sort()
    q = 0
    Max = 0
    Len = len(a)
    for i in range(Len):
        count = 0
        for j in range(Len-i-1):
            if a[Len - i - 1] == a[Len - i - 1 - j - 1]:
                count += 1
        if count > Max:
            Max = count
            q = Len - i - 1
    if Max >= 1:
        return q
    else:
        return 0


if __name__ == '__main__':
    arr = [['a'], ['a'], ['b']]
    print('待裁决数组：' + str(arr))
    print('裁决结果所在的下标：' + str(ruling(arr)))
    print('裁决结果：' + str(arr[ruling(arr)]))

