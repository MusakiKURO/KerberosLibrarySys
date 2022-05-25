import socket
import threading
import json
from datetime import datetime, timedelta
import logging

import linkDB
# ------数据协议相关配置------

# 服务器相关配置,便于修改
from DES.demo_DES import DES_call
from KDC_TGS.myTGS import *

SERVER_IP = '127.0.0.1'
SERVER_PORT = 11230

def generate_msg_to_C(src, result, target, data_msg):
    dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg}
    str_msg_orign = json.dumps(dict_msg_orign)
    HMAC = generate_password_hash(str_msg_orign)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg,
                      'HMAC': RSA_call(HMAC, myTGS.pKey, myTGS.sKey, 0)}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final

def create_msgAtoT(EK_CtoTGS,ticket_tgs, id_v, TS_4):
    EK_v = "33333333"  # 从数据库中获取，作为参数向下传递
    ticket_V_tmp = ticket_v(EK_CtoTGS, ticket_tgs.id_c, ticket_tgs.ad_c, id_v, TS_4)
    ticket_V = \
        {
            "EKc_v": ticket_V_tmp.EKc_v,
            "ID_c": ticket_V_tmp.id_c,
            "AD_c": ticket_V_tmp.ad_c,
            "ID_v": ticket_V_tmp.id_v,
            "TS_4": ticket_V_tmp.ts_4,
            "LifeTime_4": ticket_V_tmp.lifetime_4
        }
    msgttoc = \
        {
            "EKc_v": ticket_V_tmp.EKc_v,
            "ID_v": ticket_V_tmp.id_v,
            "TS_4": ticket_V_tmp.ts_4,
            "ticket_V": DES_call(json.dumps(ticket_V), EK_v, 0)  # 加密
        }
    return json.dumps(msgttoc)

def send_msg(msg_TtoC, EK_CtoTGS, src, result, target):
    send_data = DES_call(generate_msg_to_C(src, result, target, msg_TtoC), EK_CtoTGS, 0)
    sock.sendall(send_data.encode('utf-8'))
    print("---------------发送完成-----------------")

def create_Thread(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('connect success!'.encode())
    # 客户端返回信息进行确认开始工作
    data = sock.recv(1024 * 10).decode()
    msg_data = json.loads(data)
    # file = open("from_client.json", 'w')
    # file.write(msg_data)

    TS_4 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if msg_data["control_msg"]["control_target"] == "00010":
        msg_CtoT = msgCtoT(["data_msg"]["ID_v"], ["data_msg"]["ticket_TGS"])

        ticket_tgs = loadticket_tgs(msg_CtoT.ticket_tgs)
        # 验证时钟同步
        if datetime.strptime(ticket_tgs.lifetime_2, "%Y-%m-%d %H:%M:%S") - datetime.strptime(TS_4,
                                                                                             "%Y-%m-%d %H:%M:%S") < timedelta(
                minutes=5):
            EK_CtoTGS = ticket_tgs.EKc_tgs
            msg_TtoC = create_msgAtoT(EK_CtoTGS,ticket_tgs, msg_CtoT.id_v, TS_4)

            send_msg(msg_TtoC, EK_CtoTGS, "10", "0", "00000")


def loadticket_tgs(ticket_TGS):
    ticket_msg_orign = DES_call(ticket_TGS, myTGS.EKtgs, 1)
    ticket_msg_json = json.loads(ticket_msg_orign)
    return ticket_tgs(ticket_msg_json["EKc_tgs"], ticket_msg_json["ID_c"], ticket_msg_json["AD_c"],
                      ticket_msg_json["ID_tgs"], ticket_msg_json["TS_2"], ticket_msg_json["Lifetime_2"])


if __name__ == "__main__":
    myTGS = myTGS()

    # cursor = linkDB.link_DB()
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
