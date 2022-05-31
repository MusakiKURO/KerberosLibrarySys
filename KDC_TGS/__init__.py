# coding=utf-8
import socket
import threading
import json
from datetime import datetime, timedelta
import logging

from werkzeug.security import check_password_hash

import linkDB
# ------数据协议相关配置------

# 服务器相关配置,便于修改
from DES.demo_DES import DES_call
from KDC_TGS.myTGS import *

SERVER_IP = '127.0.0.1'
SERVER_PORT = 11230


def generate_msg_to_C(src, result, target, data_msg):
    dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg}
    str_msg_origin = json.dumps(dict_msg_origin)
    HMAC = generate_password_hash(str_msg_origin)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg,
                      'HMAC': RSA_call(HMAC, myTGS.sKey, 65537, 0)}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final


def create_msgAtoT(ticket_tgs, id_v, TS_4):
    EK_v = db.getClientEk(id_v)  # 从数据库中获取，作为参数向下传递
    ticket_V_tmp = ticket_v(ticket_tgs.id_c, ticket_tgs.ad_c, id_v, TS_4)
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
    send_data = generate_msg_to_C(src, result, target, DES_call(json.dumps(msg_TtoC), EK_CtoTGS, 0))
    sock.sendall(send_data.encode('utf-8'))
    print("---------------发送完成--- --------------")


def create_Thread(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('connect success!'.encode())
    # 客户端返回信息进行确认开始工作
    data = sock.recv(1024 * 10).decode()
    msg_data = json.loads(data)
    # file = open("from_client.json", 'w')
    # file.write(msg_data)

    final_dumps_data = json.dumps(
        {'control_msg': {'control_src': msg_data['control_msg']['control_src'],
                         'control_result': msg_data['control_msg']['control_result'],
                         'control_target': msg_data['control_msg']['control_target']},
         'data_msg': {'ID_v': msg_data['data_msg']['ID_v'], 'ticket_TGS': msg_data['data_msg']['ticket_TGS'],
                      'Authenticator': msg_data['data_msg']['Authenticator']}
         })

    TS_4 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Pk_c = int(db.getClientPk(msg_data["data_msg"]["ID_c"]))
    hash_check = check_password_hash(RSA_call(msg_data['HMAC'], Pk_c, 65537, 1),
                                     final_dumps_data)
    if hash_check:
        if msg_data["control_msg"]["control_target"] == "00010":
            msg_CtoT = msgCtoT(msg_data["data_msg"]["ID_v"], msg_data["data_msg"]["ticket_TGS"])

            ticket_tgs = loadticket_tgs(msg_CtoT.ticket_tgs)
            # 验证时钟同步
            if datetime.strptime(ticket_tgs.lifetime_2, "%Y-%m-%d %H:%M:%S") - datetime.strptime(TS_4,
                                                                                                 "%Y-%m-%d %H:%M:%S") < timedelta(
                minutes=5):
                EK_CtoTGS = ticket_tgs.EKc_tgs
                msg_TtoC = create_msgAtoT(ticket_tgs, msg_CtoT.id_v, TS_4)

                send_msg(msg_TtoC, EK_CtoTGS, "10", "0", "00000")
    else:
        tipsstr = { "tips": "error"}
        json.dumps(tipsstr)
        send_data = generate_msg_to_C("10", "1", "00001", tipsstr)
        sock.sendall(send_data.encode('utf-8'))


def loadticket_tgs(ticket_TGS):
    ticket_msg_origin = DES_call(ticket_TGS, myTGS.EKtgs, 1)
    ticket_msg_json = json.loads(ticket_msg_origin)
    return ticket_tgs(ticket_msg_json["EKc_tgs"], ticket_msg_json["ID_c"], ticket_msg_json["AD_c"],
                      ticket_msg_json["ID_tgs"], ticket_msg_json["TS_2"], ticket_msg_json["Lifetime_2"])


if __name__ == "__main__":
    myTGS = myTGS()

    db = linkDB.link_DB()
    # 创建TCP套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 取消主动断开连接四次握手后的TIME_WAIT状态
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定地址和端口号
    srv_addr = (SERVER_IP, SERVER_PORT)
    s.bind(srv_addr)

    # 侦听客户端
    s.listen(5)
    print('Waiting for connection...')
    while True:
        # 开始一个新连接
        sock, addr = s.accept()

        # 创建一个线程来处理连接
        t = threading.Thread(target=create_Thread(sock, addr))
        t.start()
