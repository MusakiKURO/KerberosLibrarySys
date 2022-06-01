# coding=utf-8
import multiprocessing
import socket
import threading
import json
from datetime import *
import time
import logging

from werkzeug.security import check_password_hash

import linkDB
# ------数据协议相关配置------

# 服务器相关配置,便于修改
from DES.demo_DES import DES_call
from KDC_AS.myAS import *

SERVER_IP = ''
SERVER_PORT = 7788

'''
dict_user = \
    {'control_msg':{'control_src': 00, 'control_type': 0, 'control_target': 00000},
     'data_msg':{'ID_c': '张三', 'ID_tgs': 'TGS', 'TS_1': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
     }
'''


def create_Thread(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send('connect success!'.encode())
    # 客户端返回信息进行确认开始工作
    total_data = bytes()
    while True:
        data = sock.recv(8192)
        if len(data) < 8192:
            key_values = data.decode('utf-8')
            if key_values == '@':
                break
            else:
                total_data += data
        else:
            total_data += data
    # data = sock.recv(1024 * 10).decode()
    msg_data = json.loads(total_data)
    # print(msg_data)
    # file = open('from_client.json', 'w')
    # file.write(msg_data)
    final_dumps_data = json.dumps(
        {'control_msg': {'control_src': msg_data['control_msg']['control_src'],
                         'control_result': msg_data['control_msg']['control_result'],
                         'control_target': msg_data['control_msg']['control_target']},
         'data_msg': {'ID_c': msg_data['data_msg']['ID_c'], 'ID_tgs': msg_data['data_msg']['ID_tgs'],
                      'TS_1': msg_data['data_msg']['TS_1']}
         })
    Pk_c = int(db.getClientPk(msg_data['data_msg']['ID_c']))
    EK_c = db.getClientEk(msg_data['data_msg']['ID_c'])  # 从数据库中获取，作为参数向下传递
    TS_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hash_check = check_password_hash(RSA_call(msg_data['HMAC'], Pk_c, 65537, 1),
                                     final_dumps_data)
    # print(hash_check)
    if hash_check:
        if msg_data['control_msg']['control_target'] == '00011':
            msg_CtoA = msgCtoA(msg_data['data_msg']['ID_c'], msg_data['data_msg']['ID_tgs'],
                               msg_data['data_msg']['TS_1'])
            # print('2')
            # 验证时钟同步
            if datetime.datetime.strptime(msg_CtoA.ts_1, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(TS_2,
                                                                                                           '%Y-%m-%d %H:%M:%S') < timedelta(
                    minutes=5):
                msg_AtoC = create_msgAtoC(msg_CtoA, TS_2, addr)
                # print(msg_AtoC)
                send_msg(msg_AtoC, EK_c, '01', '0', '00001')
        elif msg_data['control_msg']['control_target'] == '00001':
            print('')
    else:
        tipsstr = {'tips': 'error'}
        json.dumps(tipsstr)
        send_data = generate_msg_to_C('01', '1', '00001', tipsstr)
        key_values = '@'
        sock.sendall(send_data.encode('utf-8'))
        time.sleep(1)
        sock.send(key_values.encode('utf-8'))

    sock.close()


def create_msgAtoC(msg_CtoA, TS_2, addr):
    ticket_temp = ticket_tgs(msg_CtoA.id_c, addr, TS_2)
    ticket_TGS = \
        {
            'EKc_tgs': ticket_temp.EKc_tgs,
            'ID_c': ticket_temp.id_c,
            'AD_c': ticket_temp.ad_c,
            'ID_tgs': ticket_temp.id_tgs,
            'TS_2': ticket_temp.ts_2,
            'LifeTime_2': ticket_temp.lifetime_2
        }
    msg_AtoC_tmp = msgAtoC(TS_2, ticket_temp.EKc_tgs)
    msg_AtoC = \
        {
            'EKc_tgs': msg_AtoC_tmp.Ekc_tgs,
            'ID_tgs': msg_AtoC_tmp.id_tgs,
            'TS_2': msg_AtoC_tmp.ts_2,
            'LifeTime_2': msg_AtoC_tmp.lifetime_2,
            'ticket_TGS': DES_call(json.dumps(ticket_TGS), myas.EKtgs, 0)  # 加密
        }
    return msg_AtoC


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
    send_data = generate_msg_to_C(src, result, target, DES_call(json.dumps(msg_AtoC), EK_c, 0))
    # print(send_data)
    key_values = '@'
    sock.sendall(send_data.encode('utf-8'))
    time.sleep(1)
    sock.send(key_values.encode('utf-8'))
    print('---------------发送完成---- -------------')


if __name__ == '__main__':
    myas = myAS()

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