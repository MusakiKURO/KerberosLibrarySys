import socket
import threading
import json
from datetime import datetime, timedelta
import logging

import linkDB
# ------数据协议相关配置------

# 服务器相关配置,便于修改
from DES.demo_DES import DES_call
from KDC_AS.myAS import *

SERVER_IP = '127.0.0.1'
SERVER_PORT = 11220

"""
dict_user = \
    {"control_msg":{"control_src": 00, "control_type": 0, "control_target": 00000},
     "data_msg":{"ID_c": "张三", "ID_tgs": "TGS", "TS_1": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
     }
"""


def create_Thread(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('connect success!'.encode())
    # 客户端返回信息进行确认开始工作
    data = sock.recv(1024 * 10).decode()
    msg_data = json.loads(data)
    # file = open("from_client.json", 'w')
    # file.write(msg_data)

    EK_c = int(db.getClientEk(msg_data["data_msg"]["ID_c"])) # 从数据库中获取，作为参数向下传递

    TS_2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if msg_data["control_msg"]["control_target"] == "00001":
        msg_CtoA = msgCtoA(["data_msg"]["ID_c"], ["data_msg"]["ID_tgs"], ["data_msg"]["TS_1"])
        # 验证时钟同步
        if datetime.strptime(msg_CtoA.ts_1, "%Y-%m-%d %H:%M:%S") - datetime.strptime(TS_2, "%Y-%m-%d %H:%M:%S") < timedelta(minutes=5):
            msg_AtoC = create_msgAtoC(msg_CtoA, TS_2, addr)
            send_msg(msg_AtoC, EK_c, "01", "0", "00001")
    elif msg_data["control_msg"]["control_target"] == "00000":
        print("")


def create_msgAtoC(msg_CtoA, TS_2, addr):
    ticket_temp = ticket_tgs(msg_CtoA.id_c, addr, TS_2)
    ticket_TGS = \
        {
            "EKc_tgs": ticket_temp.EKc_tgs,
            "ID_c": ticket_temp.id_c,
            "AD_c": ticket_temp.ad_c,
            "ID_tgs": ticket_temp.id_tgs,
            "TS_2": ticket_temp.ts_2,
            "LifeTime_2": ticket_temp.lifetime_2
        }
    msg_AtoC_tmp = msgAtoC(TS_2, myas.EKtgs)
    msg_AtoC = \
        {
            "EKc_tgs": msg_AtoC_tmp.Ekc_tgs,
            "ID_tgs": msg_AtoC_tmp.id_tgs,
            "TS_2": msg_AtoC_tmp.ts_2,
            "LifeTime_2": msg_AtoC_tmp.lifetime_2,
            "ticket_TGS": DES_call(json.dumps(ticket_TGS), myas.EKtgs, 0)  # 加密
        }
    return json.dumps(msg_AtoC)

def generate_msg_to_C(src, result, target, data_msg):
    dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg}
    str_msg_orign = json.dumps(dict_msg_orign)
    HMAC = generate_password_hash(str_msg_orign)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg,
                      'HMAC': RSA_call(HMAC, myas.pKey, myas.sKey, 0)}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final

def send_msg(msg_AtoC, EK_c, src, result, target):
    # 这里开始使用传数据
    send_data = DES_call(generate_msg_to_C(src, result, target, msg_AtoC), EK_c, 0)
    sock.sendall(send_data.encode('utf-8'))
    print("---------------发送完成-----------------")


if __name__ == "__main__":
    myas = myAS()

    db = linkDB.link_DB()
    # Create The Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Listen The Port
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(10)
    print('Waiting for connection...')
    # 一旦监听到立即进入连接
    while True:
        # 开始一个新连接
        sock, addr = s.accept()

        # 创建一个线程来处理连接
        t = threading.Thread(target=create_Thread(sock, addr))
