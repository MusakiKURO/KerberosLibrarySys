import socket
import threading
import json
from datetime import datetime, timedelta
import logging

import linkDB
# ------数据协议相关配置------

# 服务器相关配置,便于修改
from DES.demo_DES import DES_call
from KDC_TGS.myTGS import myTGS

SERVER_IP = '127.0.0.1'
SERVER_PORT = 11230

def create_Thread(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('connect success!'.encode())
    # 客户端返回信息进行确认开始工作
    data = sock.recv(1024 * 10).decode()
    msg_data = json.loads(data)
    # file = open("from_client.json", 'w')
    # file.write(msg_data)

    EK_v = "33333333"  # 从数据库中获取，作为参数向下传递

    TS_2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if msg_data["control_msg"]["control_target"] == "00010":
        msg_CtoT = msgCtoT(["data_msg"]["ID_c"], ["data_msg"]["ID_tgs"], ["data_msg"]["TS_1"])
        # 验证时钟同步
        if datetime.strptime(msg_CtoT.ts_1, "%Y-%m-%d %H:%M:%S") - datetime.strptime(TS_2, "%Y-%m-%d %H:%M:%S") < timedelta(minutes=5):
            msg_TtoC = create_msgAtoT(msg_CtoT, TS_2, addr)
            send_msg(msg_TtoC, EK_c, "01", "0", "00001")
    elif msg_data["control_msg"]["control_target"] == "00000":
        print("")

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