# coding=utf-8
# @Time    : 2022/5/19 22:42
# @Author  : Nisky
# @File    : demo_RSA.py
# @Software: PyCharm
from random import randint

n = 3951270249045146953972943163348434942592764989560360906533269897277080404934010181112385167732070275357806027491762234996305583674911212807857840660608406910051955297329683233106234207322044758397760274898933802535462100186118312888112180532109135970587764285970799040141296520625252128054797411575140828014980501308928204513652682136220524500675713399801045198810206992806199335791852827154930372510398253049468928422550127057850688190116699758746503012249254107915609637655541305024737077987890330855253602741330884459042041448515721767143012038195427206379154406467638677589417430783480145088864002792702243711871
e = 65537
d = 2757273636260153892397342107350259780423194855845766289858950397671128036969148536137032681933728579320666845526660699957063082811308337204049050565811744102070678725190020954569898057638571691346945552160656416853903721986232949376871604624486124103069872348296421143823823394078988290161741459382729076515559052021058495642905456516812473319945752701566826454688598762391217175129649908066837336480981333656504068536290700516972492847182109009403521746900589327304409884664070941216444164761014904237097127620724122770288299493272459500309150609158525585771453450568861932542872871536494818060418219971795890204521


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
        C = []
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


test_str = "随着基于实时竞价(RTB)的程序性广告的普及，基于点击农场的无效流量利用大量真实的智能手机进行大规模的广告欺诈活动，正在成为在线广告的主要威胁之一。在本研究中，我们向基于点击场的无效流量的检测和大规模测量迈出了第一步。我们的研究首先使用真实世界标记的数据集对设备的特征进行测量，揭示了一系列区分欺诈性设备和良性设备的特征。基于这些特征，我们开发了EvilHunter，这是一个通过广告出价请求日志检测欺诈设备的系统，重点是对欺诈设备进行集群。EvilHunter的功能由1)建立区分欺诈和良性设备的分类；2)基于APP使用模式的设备集群；3)通过多数投票在集群中重新标记设备。EvilHunter在一个真实的标签数据集上展示了97%的准确率和95%的召回率。通过对一个超级点击场的调查，我们揭示了欺诈性集群普遍采用的几种欺骗策略。我们进一步降低了EvilHunter的开销，并讨论了如何在实际系统中部署优化后的EvilHunter。我们正在与一家领先的广告验证公司合作，将EvilHunter整合到他们的工业平台中。"
print(RSA_call(test_str, n, e, 0))
print(RSA_call(RSA_call(test_str, n, e, 0), n, d, 1))
