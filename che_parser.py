import binascii
import json
import math
from enum import Enum, IntEnum

from binary_helper import bytes_to_number

"""包头"""
head = (0x55, 0xAA)
"""波形高位需要相 & 的位"""
WAVE_BIT = [0b00000011, 0b00001100, 0b00110000, 0b11000000]
"""移位"""
MOVE = [0, 2, 4, 6]

"""电池电量"""
BATTERY_LEVEL_MAP = dict()
"""体温序号缓存"""
TEMPERATURE_SN_CACHE = dict()

class BatteryLevel(Enum):
    """电池电量"""
    COLLECTOR_INNER = 0    # 采集器内部电池
    COLLECTOR_OUTER = 1    # 采集器外部电池
    THERMOMETER = 2        # 体温计电池
    OXIMETER = 3           # 血氧计电池
    SPHYGMOMANOMETER = 4   # 血压计电池
    FLOWMETER = 5          # 流速仪电池


def is_head(data, start=0):
    """是否为数据头"""
    return data[start] == head[0] and data[start + 1] == head[1]


def length(data, start=2):
    """长度，除包头外的剩余字节"""
    return bytes_to_number(data, start, 2)


def is_collector_length(data, start=2):
    """是否为采集器的数据长度"""
    return (2 + length(data, start)) == len(data)


def check_sum(data, start=0):
    """计算校验和"""
    v = 0
    for i in range(start, min(start + 545, len(data))):
        v += data[i]
    return v & 0xFF


def verify(data, start=0):
    """验证UDP数据"""
    return is_head(data, start) \
           and is_collector_length(data, start + 2) \
           and check_sum(data, start) == data[min(start + 545, len(data))]


def parse_device_id(data, start=4, size=4):
    """解析设备ID"""
    return data[start, start + size].hex()


def parse_packet_type(data, start=8):
    """解析数据包类型"""
    return data[start] & 0xFF


def parse_file_head(data):
    """
    解析文件头
    :param data: 文件头的字节数据
    :return: 返回解析的对象
    """
    array = data.decode('UTF-8').rstrip().split('_')
    return dict(manufacturer=array[0],  # 厂商名
                deviceName=array[1],  # 设备名称
                firmwareVersion=array[3].split(':')[1],  # 固件版本
                hardwareVersion=array[4].split(':')[1],  # 硬件版本
                deviceId=array[5].split(':')[1],  # 设备ID
                resp=array[6].split(':')[1],  # 呼吸位数和采样率
                ecg=array[7].split(':')[1],  # 心电位数和采样率
                axes=array[8].split(':')[1],  # 三轴位数和采样率
                spo2=array[9].split(':')[1],  # 血氧位数和采样率
                )


def parse_packet_sn(data, start=0):
    """解析包序号"""
    return bytes_to_number(data, start, 4)


def parse_time(data, start=4, size=4):
    """解析时间"""
    time = bytes_to_number(data, start, 4) * 1000
    if size == 6:
        time += bytes_to_number[data, start + 4, 2]
    return time


def right_move(b, move):
    """
    右移
    :param b: 字节
    :param move: 右移的位数
    :return: 返回右移的结果
    """
    value = b
    if move == 0:
        value = (b & 0b00000001)
    elif move == 1:
        value = (b & 0b00000010)
    elif move == 2:
        value = (b & 0b00000100)
    elif move == 3:
        value = (b & 0b00001000)
    elif move == 4:
        value = (b & 0b00010000)
    elif move == 5:
        value = (b & 0b00100000)
    elif move == 6:
        value = (b & 0b01000000)
    elif move == 7:
        value = (b & 0b10000000)
    return value >> move


def parse_packet(data, device_id=None, start=0):
    """解析数据包"""
    if verify(data):
        start = start + 9
    else:
        start = start

    pkt = Packet()
    pkt.deviceId = device_id
    pkt.deviceCode = 0
    if device_id is not None and isinstance(device_id, str):
        pkt.deviceCode = bytes_to_number(binascii.unhexlify(device_id))
    # 包序号: (0 ~ 3)
    pkt.packetSn = parse_packet_sn(data, start)
    # 获取设备时间: (4 ~ 9)
    pkt.time = parse_time(data, start + 4)

    # 解析波形数据
    # 胸呼吸波形: (10 ~ 59) => 50
    pkt.rawChestRespList = parse_array(data, start + 10, start + 60, 2)
    # 腹呼吸波形: (60 ~ 109) => 50
    pkt.rawAbdominalRespList = parse_array(data, start + 60, start + 110, 2)
    # 心电波形: (110 ~ 361) => [4 * (50 + 13) = 252]
    pkt.ecgList = parse_wave(4, 50, 13, data, start + 110)
    # 加速度波形数据 (362, 456) => 96
    # X轴 (362, 393) => [25 + 7 = 32]
    pkt.xList = parse_wave(1, 25, 7, data, start + 362)
    # Y轴 (394, 425) => [25 + 7 = 32]
    pkt.yList = parse_wave(1, 25, 7, data, start + 394)
    # Z轴 (426, 457) => [25 + 7 = 32]
    pkt.zList = parse_wave(1, 25, 7, data, start + 426)
    # 血氧波形: (458, 507) => 50
    pkt.spo2List = parse_array(data, start + 458, start + 508, 1)

    # 包含流速仪数据: (544, 668)
    pkt.flowmeter = (data[start + 8] & 0xFF) == 0xF3
    if pkt.flowmeter:
        # 流速仪第0组数据 (544, 549]
        # 25组，
        # 第一组:
        # 吹气或呼吸(0/1)，1个字节(544)
        # 实时流速值 ml/s，2个字节(545, 547]
        # 实时容积 ml，2个字节(547, 549]
        pkt.breathList = [0] * 25
        pkt.flowVelocityList = [0] * 25
        pkt.volumeList = [0] * 25
        j = start + 544
        for i in range(25):
            pkt.breathList[i] = data[i + j] & 0xFF
            pkt.flowVelocityList[i] = bytes_to_number([data[i + j + 1], data[i + j + 2]])
            pkt.volumeList[i] = bytes_to_number([data[i + j + 3], data[i + j + 4]])
            j += 5

    # 体温时间: (508, 511)
    pkt.temperatureTime = parse_time(data, 508 + start, 4) * 1000

    # 参数高位：(512)
    paramHigh = data[512 + start]
    # 设备功耗过高标志       (5)
    pkt.deviceOverload = right_move(paramHigh, 5)
    # 胸呼吸连接标志( 0 连接 (6)
    pkt.respConnState = right_move(paramHigh, 6)
    # 腹呼吸连接标志( 0 连接 (7)
    pkt.abdominalConnState = right_move(paramHigh, 7)
    # 血氧信号强度(513)
    pkt.spo2Signal = data[513 + start]
    # 胸呼吸系数(514)
    pkt.respRatio = data[513 + start]
    # 腹呼吸系数(515)
    pkt.abdominalRatio = (data[515 + start] & 0xff)
    # 体温(516)
    pkt.temperature = ((right_move(paramHigh, 2) << 8) | (data[516 + start] & 0xFF))
    # 血氧饱和度(517)
    pkt.spo2 = data[517 + start]

    ## 设备状态: (518)   ... 0 为正常; / 1 为告警;
    # 开机标志在开机第一包数据该位置 1, 其他数据包该位置 0;
    # 时间设置标志开机置 1,在接收到时间设备指令后置 0
    deviceState = data[518 + start]
    # 心电导联脱落状态
    pkt.ecgConnState = right_move(deviceState, 0)
    # 血氧探头脱落标志
    pkt.spo2ProbeConnState = right_move(deviceState, 1)
    # 体温连接断开标志
    pkt.temperatureConnState = right_move(deviceState, 2)
    # 血氧连接断开标志
    pkt.spo2ConnState = right_move(deviceState, 3)
    # 血压连接断开标志
    pkt.elecMmhgConnState = right_move(deviceState, 4)
    # 流速仪连接断开标志
    pkt.flowmeterConnState = right_move(deviceState, 5)
    # 时间设置标志
    pkt.calibrationTime = right_move(deviceState, 6)
    # 开机标志
    pkt.powerOn = right_move(deviceState, 7)

    # 电量提示：(519)   0 为正常; 1 为告警
    batteryHint = data[519 + start]
    # 外部电池电量低
    pkt.deviceOuterBatteryAlarm = right_move(batteryHint, 0)
    # 蓝牙体温计电量低
    pkt.temperatureBatteryAlarm = right_move(batteryHint, 1)
    # 蓝牙血氧电量低
    pkt.spo2BatteryAlarm = right_move(batteryHint, 2)
    # 蓝牙血压计电量低
    pkt.elecMmhgBatteryAlarm = right_move(batteryHint, 3)
    # 流速仪电量低
    pkt.flowmeterBatteryAlarm = right_move(batteryHint, 4)

    # 状态开关: (520)，0为关; 1为开
    switchState = data[520 + start]
    # 蓝牙连接断开蓝闪
    pkt.bluetoothConnSwitch = right_move(switchState, 0)
    # 锂电池电量低绿闪
    pkt.batteryLowLightSwitch = right_move(switchState, 1)
    # 锂电池电量低震动
    pkt.batteryLowShockSwitch = right_move(switchState, 2)
    # 蓝牙设备电量低绿闪
    pkt.bluetoothLightSwitch = right_move(switchState, 3)
    # 蓝牙体温计开关位
    pkt.temperatureSwitch = right_move(switchState, 4)
    # 蓝牙血氧计开关位
    pkt.spo2Switch = right_move(switchState, 5)
    # 蓝牙血压计开关位
    pkt.elecMmhgSwitch = right_move(switchState, 6)
    # 蓝牙流速仪开关位
    pkt.flowmeterSwitch = right_move(switchState, 7)

    # 电量: (521)
    batteryType = BatteryLevel(data[521 + start])
    devceBatteryInfo = BATTERY_LEVEL_MAP.get(device_id)
    if devceBatteryInfo is None:
        devceBatteryInfo = dict()
        BATTERY_LEVEL_MAP[device_id] = devceBatteryInfo
    if batteryType != BatteryLevel.COLLECTOR_INNER and batteryType != BatteryLevel.COLLECTOR_OUTER:
        devceBatteryInfo[batteryType.name] = data[522 + start] & 0xFF
    else:
        power = math.floor(((((data[522 + start] & 0xFF) - 15) * 5 + 3200 - 3300) / (4050 - 3300)) * 100)
        devceBatteryInfo[batteryType.name] = max(min(power, 100), 0)
    # # 0：内部电池
    # pkt.deviceBattery =
    # # 1：外部电池
    # pkt.deviceOuterBattery =
    # # 2：体温计电池
    # pkt.semperatureBattery =
    # # 3：血氧计电池
    # pkt.spo2Battery =
    # # 4：血压计电池
    # pkt.elecMmhgBattery =
    # # 5：流速仪
    # pkt.flowmeterBattery =

    # WiFi信号强度(523)
    pkt.wifiSignal = -(data[523 + start] & 0xFF)
    #脉率 (524)
    pkt.pulseRate = ((right_move(paramHigh, 1) << 8) | (data[524 + start] & 0xFF))

    # AP MAC (525, 529)
    apMac = data[525 + start:525 + start+5]

    if device_id is not None and device_id.startswith('11'):
        pkt.apMac = apMac.hex()
    else:
        # 体温数据
        temperatureSn = apMac[2] & 0xFF
        oldTemperatureSn = TEMPERATURE_SN_CACHE.get(device_id)
        pkt.carepatchSn = temperatureSn
        if oldTemperatureSn is not  None:
            if temperatureSn != oldTemperatureSn:
                temperature = (((apMac[0] & 0xFF) << 8) | (apMac[1] & 0xFF))
                pkt.carepatchTemperature(temperature)
                TEMPERATURE_SN_CACHE[device_id] = temperatureSn
            else:
             pkt.carepatchTemperature = None
        else:
            pkt.carepatchTemperature = None
            TEMPERATURE_SN_CACHE[device_id] = temperatureSn
        pkt.setTemperature = 0

    # 电池电量格数
    pkt.batteryLevelGridCount = data[534 + start] & 0xFF

    # 版本号 (530)
    version = data[530 + start]
    if version != 0:
        # 高位
        high = (version & 0b11100000) >> 5
        # 中位
        middle = (version & 0b00011100) >> 2
        # 低位
        low = version & 0b00000011
        # 固件版本
        pkt.versionCode = (high << 5) | (middle << 2) | low
        pkt.versionName = "%d.%d.%d".format(high, middle, low)

    return pkt


def parse_array(data, start, end, byte_size):
    """解析数组"""
    arr = [0] * int((end - start) / byte_size)
    j = start
    for i in range(len(arr)):
        if byte_size == 1:
            arr[i] = data[j + 1] & 0xFF
        else:
            arr[i] = bytes_to_number(data[j:j + byte_size])
        j += byte_size
    return arr


def parse_wave(group, wave_len, high_len, data, start):
    """解析波形数组"""
    arr = [0] * int(wave_len * group)
    i = 0
    for n in range(group):
        for j in range(wave_len):
            arr[i] = calculate(wave_len, high_len, data, start, n, j)
            i += 1
    return arr


def calculate(wave_len, high_len, data, start, group, index):
    # 数据范围是“左开右闭”，以心电波形数据为例，其他同理
    # ============================================
    # 心电波形: (119, 371] == >: 252
    # ============================================
    # 心电波形1(高位)(119, 132] == >: 13
    # 心电波形1(低位)(132, 182] == >: 50
    # ============================================
    # 心电波形2(高位)   (182, 195]   ==>: 13
    # 心电波形2(低位)   (195, 245]   ==>: 50
    # ============================================
    # 心电波形3(高位)   (245, 258]   ==>: 13
    # 心电波形3(低位)   (258, 308]   ==>: 50
    # ============================================
    # 心电波形4(高位)   (308, 321]   ==>: 13
    # 心电波形4(低位)   (321, 371]   ==>: 50
    # ============================================
    # 4 * 63 ==>: 252
    # ============================================
    # 1个字节有8位
    # 每个波形的高位占2两位，如下标为119的字节值，8位分别为(132 ~ 136] 4个波形提供高位
    # ============================================
    # 以波形1为例：(119, 182]
    # 假如下标119的值为：55，即：‭0011 0111‬，第0个波形值取(0, 2]的2位(11)
    # 假如下标119的值为：55，即：‭0011 0111‬，第1个波形值取(2, 4]的2位(01)
    # 假如下标119的值为：55，即：‭0011 0111‬，第2个波形值取(4, 6]的2位(11)
    # 假如下标119的值为：55，即：‭0011 0111‬，第3个波形值取(6, 8]的2位(00)

    # 则，(((data[119] & (0000 0011)) >>> 0) << 8) | (data[132] & 0xFF)
    # 则，(((data[119] & (0000 1100)) >>> 2) << 8) | (data[133] & 0xFF)
    # 则，(((data[119] & (0011 0000)) >>> 4) << 8) | (data[134] & 0xFF)
    # 则，(((data[119] & (1100 0000)) >>> 6) << 8) | (data[135] & 0xFF)

    # 共有4组，每组占63个字节，n记录是第几组，假如第0组的第9个值，
    # 即，
    # 高位为：data[(n * 63) + (i / 4) + start]  ==>: data[(0 * 63) + (8 / 4) + 119] = data[121]
    # (data[121] & WAVE_BIT[i % 4]) >>> MOVE[i % 4]
    #
    # 低位为：data[(n * 63) + 13 + start]  ==>: data[(0 * 63) + 13 + 119] = data[132]
    # (data[132] & 0xFF)

    # 高位 | 低位  ==> 波形值

    size = wave_len + high_len
    high = ((((data[group * size + int(index / 4) + start] & 0xFF) & WAVE_BIT[index % 4]) >> MOVE[index % 4]) << 8)
    low = (data[group * size + high_len + index + start] & 0xFF)
    return high | low


class Packet:
    """解析后的数据包"""
    pass


if __name__ == '__main__':
    # with open('./resources/11000014-2020_12_17-09_55_00-001.CHE', 'rb+') as f:
    with open('E:/0000037E-2019_11_06-14_58_46.CHE', 'rb+') as f:
        file_head = parse_file_head(f.read(576))
        print(json.dumps(file_head))
        print('deviceId:', file_head['deviceId'])

        for i in range(20):
            data = f.read(576)
            p = parse_packet(data, file_head['deviceId'])
            print(i, json.dumps(p.__dict__))


