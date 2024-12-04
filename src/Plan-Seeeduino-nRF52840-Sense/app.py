import serial
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets, QtCore

# 串口设置
ser = serial.Serial('COM8', 115200)

# 初始化绘图
plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [])
line2, = ax.plot([], [])
line3, = ax.plot([], [])

# 数据缓存
xdata, y1data, y2data, y3data = [], [], [], []

# 更新绘图函数
def update_plot():
    global xdata, y1data, y2data, y3data
    # 从串口读取数据，解析并更新数据缓存
    # ...
    xdata.append(len(xdata))
    # ...
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.01)

# 主循环
if __name__ == '__main__':
    timer = QtCore.QTimer()
    timer.timeout.connect(update_plot)
    timer.start(100)  # 每100ms更新一次
    # ... (其他GUI逻辑)
    app = QtWidgets.QApplication([])
    # ...
    app.exec_()