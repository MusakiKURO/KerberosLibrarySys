import socket
import threading
import json
from datetime import datetime, timedelta
import logging

import linkDB
# ------数据协议相关配置------

# 服务器相关配置,便于修改
from KDC_AS.myAS import myAS, msgCtoA

SERVER_IP = '127.0.0.1'
SERVER_PORT = 11220

"""
dict_user = \
    {"control_msg":{"control_src": 00, "control_type": 0, "control_target": 00000},
     "data_msg":{"ID_c": "张三", "ID_tgs": "TGS", "TS_1": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
     }
"""


def Create_Thread():
    print('Accept new connection from %s:%s...' % addr)
    sock.send('connect success!'.encode())
    # 客户端返回信息进行确认开始工作
    data = sock.recv(1024 * 10).decode()
    msg_data = json.loads(data)
    file = open("from_client.json", 'w')
    file.write(msg_data)

    msg_CtoA = msgCtoA(["data_msg"]["ID_c"], ["data_msg"]["ID_tgs"], ["data_msg"]["TS_1"])
    if(msg_data["control_msg"]["control_target"]=="00010"):
        #验证时钟同步
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # difference = (datetime.strptime(msg_CtoA.ts_1, "%Y-%m-%d %H:%M:%S") - datetime.strptime(nowtime, "%Y-%m-%d %H:%M:%S"))
        # print(difference)
        if datetime.strptime(msg_CtoA.ts_1, "%Y-%m-%d %H:%M:%S") - datetime.strptime(nowtime, "%Y-%m-%d %H:%M:%S") < timedelta(minutes=5):
            send_msg()

    # print(msg_data["start"])
def create_msgAtoC():


def send_msg():
    create_msgAtoC()
    # 这里开始使用传数据
    data = {
    }
    str_json = json.dumps(data)
    sock.send(str_json.encode())
    print("---------------发送完成-----------------")


if __name__ == "__main__":
    myas = myAS()

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
        t = threading.Thread(target=Create_Thread(sock, addr))
