"""16进制和2进制转换"""
HEX_UPPER_CASE = "0123456789ABCDEF"
"""16进制和2进制转换"""
HEX_LOWER_CASE = "0123456789abcdef"

"""2进制字符串"""
BINARY_STR = (
    "0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
    "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"
)

HEX_CHARS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')

"""默认字节序，默认大端字节顺序（高位在前，低位在后）"""
order = 'BIG_ENDIAN'


def bytes_to_number(data, start=0, size=0, big_endian=True, signed=False):
    """
    字节转为数值
    :param data: 数据
    :param start: 开始的位置
    :param size: 计算的长度，为0表示全部计算
    :param big_endian: 字节顺序，大端/小端
    :param signed: 是否为有符号数值
    :return: 返回计算后的数值
    """
    v = 0
    if size <= 0:
        size = int(len(data) - start)

    if big_endian:
        if signed and ((data[start] & 0b10000000) >> 7) == 1:
            for i in range(size):
                v <<= 8
                v |= ~data[start + i] & 0xFF
            v = ((-v) - 1)
        else:
            for i in range(size):
                v <<= 8
                v |= data[start + i] & 0xFF
    else:
        if signed and ((data[len(data) - 1] & 0b10000000) >> 7) == 1:
            for i in reversed(range(size)):
                v <<= 8
                v |= ~data[start + i] & 0xFF
            v = ((-v) - 1)
        else:
            for i in reversed(range(size)):
                v <<= 8
                v |= data[start + i] & 0xFF
    return int(v)


def int_to_float(value):
    """
    整数转换为浮点数
    :param value: 数值
    :return: 返回值
    """
    pass
