# coding=utf-8
# @Time    : 2022/5/18 20:29
# @Author  : Nisky
# @File    : demo_DES.py
# @Software: PyCharm

from bitarray import bitarray
from DES import demo_DES_BOX


def str2bits(s):
    ret = ''.join([bin(int('1' + hex(c)[2:], 16))[3:] for c in s.encode("utf-8")])
    return ret


def bits2str(bits):
    b = bitarray(bits)
    return b.tobytes().decode("utf-8")


def generate_msg_block(text, option):
    # 将要加密的数据分块
    if option == 0:
        bit_text = str2bits(text)
        length = len(bit_text)
        fixed_length = 64
        r = length // fixed_length
        if length % fixed_length > 0:
            r = r + 1
        if length % 64 != 0:
            bit_text = bit_text + str2bits(((r * 64) - length) // 8 * " ")
        text_bit_block = []
        for i in range(0, r):
            start = fixed_length * i
            size = fixed_length
            text_bit_block.append(bit_text[start:start + size])
        return text_bit_block

    # 由于密文无法decode()编码，部分步骤可省略
    else:
        length = len(text)
        fixed_length = 64
        r = length // fixed_length
        text_bit_block = []
        for i in range(0, r):
            start = fixed_length * i
            size = fixed_length
            text_bit_block.append(text[start:start + size])
        return text_bit_block


# 生成每一轮的key
def create_Keys(inkeys):
    keyResult = []
    str_bit_keys = str2bits(inkeys)
    keyinit = list(map(int, str_bit_keys))
    # print(keyinit)
    # 初始化列表key0,key1
    key0 = [0 for i in range(56)]
    key1 = [0 for i in range(48)]
    # 进行密码压缩置换1，将64位密码压缩为56位
    for i in range(56):
        key0[i] = keyinit[demo_DES_BOX.PC1[i] - 1]

    # 进行16轮的密码生成
    for i in range(16):
        # ---------确定左移的次数----------
        if i == 0 or i == 1 or i == 8 or i == 15:
            moveStep = 1
        else:
            moveStep = 2
        # ------------------------------

        # --------分两部分，每28bit位一部分，进行循环左移------------
        for j in range(moveStep):
            for k in range(8):
                temp = key0[k * 7]
                for m in range(7 * k, 7 * k + 6):
                    key0[m] = key0[m + 1]
                key0[k * 7 + 6] = temp
            temp = key0[0]
            for k in range(27):
                key0[k] = key0[k + 1]
            key0[27] = temp
            temp = key0[28]
            for k in range(28, 55):
                key0[k] = key0[k + 1]
            key0[55] = temp
        # -----------------------------------------------------

        # ------------对56位密钥进行压缩置换，压缩为48位-------------
        for k in range(48):
            key1[k] = key0[demo_DES_BOX.PC2[k] - 1]
        keyResult.extend(key1)

        # ------------------------------------------------------

    return keyResult


def DES(bitText, key, optionType):
    keyResult = create_Keys(key)
    finalTextOfBit = [0 for i in range(64)]

    if optionType == 0:  # 选择的操作类型为加密

        tempText = [0 for i in range(64)]  # 用于临时盛放IP逆置换之前，将L部分和R部分合并成64位的结果
        extendR = [0 for i in range(48)]  # 用于盛放R部分的扩展结果

        initTrans = [0 for i in range(64)]  # 初始化，用于存放IP置换后的结果

        # ------------------进行初始IP置换---------------
        for i in range(64):
            initTrans[i] = bitText[demo_DES_BOX.IP[i] - 1]
        # 将64位明文分为左右两部分
        L = [initTrans[i] for i in range(32)]
        R = [initTrans[i] for i in range(32, 64)]

        # 开始进行16轮运算
        for i in range(16):
            tempR = R  # 用于临时盛放R

            # -----------进行扩展，将32位扩展为48位--------
            for j in range(48):
                extendR[j] = R[demo_DES_BOX.E[j] - 1]
            #           print(len(keyResult))
            keyi = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # ----------与key值进行异或运算----------------
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if keyi[j] != extendR[j]:
                    XORResult[j] = 1

            SResult = [0 for k in range(32)]
            # ---------开始进行S盒代换-------------------
            for k in range(8):
                row = XORResult[k * 6] * 2 + XORResult[k * 6 + 5]
                column = XORResult[k * 6 + 1] * 8 + XORResult[k * 6 + 2] * 4 + XORResult[k * 6 + 3] * 2 + XORResult[
                    k * 6 + 4]
                temp = demo_DES_BOX.S[k][row * 16 + column]
                for m in range(4):
                    SResult[k * 4 + m] = (temp >> m) & 1
            # -----------------------------------------
            PResult = [0 for k in range(32)]
            # --------------开始进行P盒置换----------------
            for k in range(32):
                PResult[k] = SResult[demo_DES_BOX.P[k] - 1]
            # ------------------------------------------

            # --------------与L部分的数据进行异或------------
            XORWithL = [0 for k in range(32)]
            for k in range(32):
                if L[k] != PResult[k]:
                    XORWithL[k] = 1
            # ----------------------------------------------

            # -------------将临时保存的R部分值，即tempR复制给L------
            L = tempR
            R = XORWithL

        # ----交换左右两部分------
        L, R = R, L

        # -----合并为一部分
        tempText = L
        tempText.extend(R)
        # -----------IP逆置换--------
        for k in range(64):
            finalTextOfBit[k] = tempText[demo_DES_BOX.RIP[k] - 1]
        finalTextOfStr = "".join(list(map(str, finalTextOfBit)))
        return finalTextOfStr

    else:  # 选择的操作类型为解密
        tempText = [0 for i in range(64)]  # 用于临时盛放IP逆置换之前，将L部分和R部分合并成64位的结果
        extendR = [0 for i in range(48)]  # 用于盛放R部分的扩展结果

        initTrans = [0 for i in range(64)]  # 初始化，用于存放IP置换后的结果

        # ------------------进行初始IP置换---------------
        for i in range(64):
            initTrans[i] = bitText[demo_DES_BOX.IP[i] - 1]
        # 将64位明文分为左右两部分
        L = [initTrans[i] for i in range(32)]
        R = [initTrans[i] for i in range(32, 64)]

        # -----------------开始16轮的循环-----------------
        for i in range(15, -1, -1):
            tempR = R  # 用于临时盛放R

            # -----------进行扩展，将32位扩展为48位--------
            for j in range(48):
                extendR[j] = R[demo_DES_BOX.E[j] - 1]

            keyi = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # ----------与key值进行异或运算----------------
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if keyi[j] != extendR[j]:
                    XORResult[j] = 1

            SResult = [0 for k in range(32)]
            # ---------开始进行S盒替换-------------------
            for k in range(8):
                row = XORResult[k * 6] * 2 + XORResult[k * 6 + 5]
                column = XORResult[k * 6 + 1] * 8 + XORResult[k * 6 + 2] * 4 + XORResult[k * 6 + 3] * 2 + XORResult[
                    k * 6 + 4]
                temp = demo_DES_BOX.S[k][row * 16 + column]
                for m in range(4):
                    SResult[k * 4 + m] = (temp >> m) & 1
            # -----------------------------------------
            PResult = [0 for k in range(32)]
            # --------------开始进行P盒置换----------------
            for k in range(32):
                PResult[k] = SResult[demo_DES_BOX.P[k] - 1]
            # ------------------------------------------

            # --------------与L部分的数据进行异或------------
            XORWithL = [0 for k in range(32)]
            for k in range(32):
                if L[k] != PResult[k]:
                    XORWithL[k] = 1
            # ----------------------------------------------

            # -------------将临时保存的R部分值，即tempR复制给L------
            L = tempR
            R = XORWithL

        # ----交换左右两部分------
        L, R = R, L

        # -----合并为一部分
        tempText = L
        tempText.extend(R)
        # -----------IP逆置换--------
        for k in range(64):
            finalTextOfBit[k] = tempText[demo_DES_BOX.RIP[k] - 1]
        finalTextOfStr = "".join(list(map(str, finalTextOfBit)))
        return finalTextOfStr


# 输入的参数：文本（明文或者密文），
def DES_call(text, key, option):
    # 加密
    if option == 0:
        msg_list = generate_msg_block(text, option)
        # print(bits2str("".join(msg_list)))
        result_bit = ""
        for i in range(len(msg_list)):
            result_bit = result_bit + DES(list(map(int, msg_list[i])), key, option)
        return result_bit

    # 解密
    else:
        msg_list = generate_msg_block(text, option)
        result_bit = ""
        for i in range(len(msg_list)):
            result_bit = result_bit + DES(list(map(int, msg_list[i])), key, option)
        return bits2str(result_bit)
