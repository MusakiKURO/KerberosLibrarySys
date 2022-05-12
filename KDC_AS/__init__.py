import socket
import threading
import json
import logging

# ------数据协议相关配置------

# 服务器相关配置,便于修改
SERVER_IP = '127.0.0.1'
SERVER_PORT = 11220

# 数据库配置信息
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = ''
DB_USER = 'ZUO'
DB_PASS = 'zxcvbnm.123'


def Create_Thread():
    print('Accept new connection from %s:%s...' % addr)
    sock.send(('connect success!').encode())
    # 客户端返回信息进行确认开始工作
    data = sock.recv(1024 * 10).decode()
    data_json = json.loads(data)
    file=open("from_client.json",'w')
    file.write(data_json)
    print(data_json["start"])

    while True:
    # 这里开始使用传数据
        data = {

        }
        str_json = json.dumps(data)
        sock.send(str_json.encode())

        print("---------------发送完成-----------------")



if __name__ == "__main__":
    # Create The Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Listen The Port
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(128)
    print('Waiting for connection...')
    # 一旦监听到立即进入连接
    while True:
        # 开始一个新连接
        sock, addr = s.accept()

        # 创建一个线程来处理连接
        t = threading.Thread(target=Create_Thread(sock, addr))