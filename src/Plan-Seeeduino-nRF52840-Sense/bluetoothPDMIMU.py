import asyncio
from bleak import BleakClient

# 蓝牙设备的 MAC 地址（替换为实际设备地址）
device_address = "XX:XX:XX:XX:XX:XX"

# 读取 IMU 数据的 UUID
imu_uuid = "2A56"
mic_uuid = "2A57"

async def connect_to_device():
    async with BleakClient(device_address) as client:
        print(f"连接到设备：{client.address}")

        # 读取并打印 IMU 数据
        def imu_data_callback(sender: int, data: bytearray):
            imu_data = data.decode('utf-8')
            print(f"IMU 数据：{imu_data}")

        # 读取并打印麦克风数据
        def mic_data_callback(sender: int, data: bytearray):
            mic_data = data.decode('utf-8')
            print(f"麦克风数据：{mic_data}")

        # 注册数据通知
        await client.start_notify(imu_uuid, imu_data_callback)
        await client.start_notify(mic_uuid, mic_data_callback)

        # 保持连接直到退出
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(connect_to_device())
