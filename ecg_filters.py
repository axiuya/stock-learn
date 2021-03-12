
import matplotlib.pyplot as plt
import numpy as np

from scipy import signal


def draw_ecg():
    filename = "./resources/02000060__20210311161905548.ecg"
    data = np.loadtxt(filename, dtype=np.int32, delimiter=',')
    a = np.array(data)
    data = a[:, 4]
    plt.plot(data)

    b, a = signal.butter(8, [0.01, 0.4], 'bandpass')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, data)  # data为要过滤的信号

    plt.plot(filtedData * 80 / 10768 + 512)
    plt.show()
    # a = a + 1000
    # b = []
    # for v in range(len(a)):
    #     b.append(int(a[v] * 10))
    #
    # plt.plot(b)
    # plt.show()

if __name__ == '__main__':
    print()

    # 绘制
    draw_ecg()