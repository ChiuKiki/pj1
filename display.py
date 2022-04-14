# 监测结果显示模块
# 需提前准备top命令输出的监测结果文件
import matplotlib.pyplot as plt
import numpy as np


# 从监测结果文件中提取数据
def data(file_path):
    fi = open(file_path, "r", encoding="utf-8")
    arr = []
    for line in fi:
        line_split = line.split()
        if "average:" in line:  # 平均负载
            arr.append(line_split[-3][:-1])
            arr.append(line_split[-2][:-1])
            arr.append(line_split[-1])
        if "%Cpu(s):" in line:  # 用户空间占用CPU的百分比(us)、内核空间占用CPU的百分比(sy)、软中断占用CPU的百分比(si)
            arr.append(line_split[1])
            arr.append(line_split[3])
            arr.append(line_split[-4])
        if "lab401" in line:  # 进程占用CPU的百分比(%CPU)
            arr.append(line_split[-4])
        for i in range(len(arr)):
            arr[i] = float(arr[i])
    arrays = [arr[i:len(arr):7] for i in range(0, 7)]    # 按不同指标来分，共七个
    return arrays


def display(data_arrays):
    data_ndarrays = np.array(data_arrays)  # 把list类型转为numpy.ndarray
    picture_num = data_ndarrays.shape[0]
    data_num_per_line = data_ndarrays.shape[1]
    titles = ['5min前到现在系统平均负载', '10min前到现在系统平均负载', '15min前到现在系统平均负载',
              '用户空间占用CPU的百分比(%)', '内核空间占用CPU的百分比(%)', '软中断占用CPU的百分比(%)', '进程占用CPU的百分比(%)']
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
    for i in range(picture_num):
        plt.figure()
        plt.plot(list(range(1, data_num_per_line + 1)), data_ndarrays[i, :], markerfacecolor='blue', marker='o')
        plt.xlabel('时间(/秒)')
        if i >= 3:
            plt.ylabel('百分比(%)')
        else:
            plt.ylabel('负载值')
        plt.title(titles[i])
    plt.show()


if __name__ == '__main__':
    file_path = "top_test_A_5000.txt"
    data_arrays = data(file_path)
    display(data_arrays)
