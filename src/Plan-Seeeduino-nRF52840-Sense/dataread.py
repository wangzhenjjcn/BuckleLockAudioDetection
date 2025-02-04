import serial
import time
import json
from pyecharts import options as opts
from pyecharts.charts import Line, Page
from pyecharts.faker import Faker

# 设定串口
ser = serial.Serial('COM13', 115200)  # 根据实际连接的端口号选择串口
time.sleep(2)  # 给串口设备一些时间初始化

# 初始化数据
accel_data = []
gyro_data = []
audio_data = []
timestamps = []

# 创建 Pyecharts Line 图表
def create_line_chart():
    line = Line()
    line.add_xaxis(timestamps)
    line.add_yaxis("Accel X", [data[0] for data in accel_data], is_smooth=True)
    line.add_yaxis("Accel Y", [data[1] for data in accel_data], is_smooth=True)
    line.add_yaxis("Accel Z", [data[2] for data in accel_data], is_smooth=True)
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="3-Axis Accelerometer Data"),
        xaxis_opts=opts.AxisOpts(type_="time"),
        yaxis_opts=opts.AxisOpts(name="Acceleration (m/s²)"),
        datazoom_opts=opts.DataZoomOpts(type_="slider")
    )
    return line

def create_area_chart():
    area = Line()
    area.add_xaxis(timestamps)
    area.add_yaxis("Audio Data", audio_data, is_area=True, is_smooth=True)
    area.set_global_opts(
        title_opts=opts.TitleOpts(title="Audio Data over Time"),
        xaxis_opts=opts.AxisOpts(type_="time"),
        yaxis_opts=opts.AxisOpts(name="Audio Amplitude"),
        datazoom_opts=opts.DataZoomOpts(type_="slider")
    )
    return area

def update_data():
    line_chart = create_line_chart()
    area_chart = create_area_chart()
    
    page = Page()
    page.add(line_chart, area_chart)
    page.render('real_time_data.html')  # 输出为 HTML 文件，支持动态更新

# 串口数据处理
while True:
    # 读取串口数据
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        try:
            # 假设数据格式为 JSON，例如：{"accel": [x, y, z], "gyro": [gx, gy, gz], "audio": [audio_data]}
            data = json.loads(line)

            # 解析数据
            accel = data['accel']
            gyro = data['gyro']
            audio = data['audio']
            timestamp = time.time()

            # 保存数据
            accel_data.append(accel)
            gyro_data.append(gyro)
            audio_data.append(audio[0])  # 假设音频数据是单通道

            # 更新时间戳
            timestamps.append(timestamp)

            # 限制数据数量（保持一定的数据点）
            if len(accel_data) > 100:
                accel_data.pop(0)
                gyro_data.pop(0)
                audio_data.pop(0)
                timestamps.pop(0)

            # 更新图表
            update_data()

        except json.JSONDecodeError:
            continue

    time.sleep(0.1)  # 延迟，用于防止串口读取过快
