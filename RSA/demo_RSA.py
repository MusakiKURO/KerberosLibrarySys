# coding=utf-8
# @Time    : 2022/5/19 22:42
# @Author  : Nisky
# @File    : demo_RSA.py
# @Software: PyCharm


# 整数转换成字节
def uint_to_bytes(x: int) -> bytes:
    if x == 0:
        return bytes(1)
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


# 字节转换成整数
def bytes_to_uint(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def generate_block_text(text, option):
    if option == 0:
        length = len(text)
        max_msg_length = 80
        r = length // max_msg_length
        if length % max_msg_length > 0:
            r = r + 1
        M = []
        for i in range(0, r):
            start = max_msg_length * i
            size = max_msg_length
            if i < r - 1:
                M.append(text[start:start + size])
            else:
                M.append(text[start:length])
        return M
    else:
        text_list = text.split(",")
        text_list = [int(text_list[i]) for i in range(len(text_list))]
        return text_list


def RSA_call(text, n, x, option):
    if option == 0:
        byte_text = []
        c = []
        m = []
        M = generate_block_text(text, option)
        for i in range(len(M)):
            byte_text.append(M[i].encode('utf8'))
            m.append(bytes_to_uint(byte_text[i]))
            c.append(pow(m[i], x, n))
        return ",".join(list(map(str, c)))
    else:
        text_list = generate_block_text(text, option)
        int_text = []
        byte_text = []
        m = []
        for i in range(len(text_list)):
            int_text.append(pow(text_list[i], x, n))
            byte_text.append(uint_to_bytes(int_text[i]))
            m.append(byte_text[i].decode('utf8'))
        sum = ""
        for i in m:
            sum += str(i)
        return sum
