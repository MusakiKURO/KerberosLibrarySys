# coding=utf-8
# @Time    : 2022/5/19 15:24
# @Author  : Nisky
# @File    : demo_MainWindow_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from KerberosLibrarySys.Client import demo_reader_MainWindow
from KerberosLibrarySys.DES.demo_DES import DES_call
from KerberosLibrarySys.Client.generate_msg import *
import socket
import sys

# 要连接的目标IP和Port
# AS
AS_IP = ''
AS_Port = None
# TGS
TGS_IP = ''
TGS_Port = None
# Server
Server_IP = ''
Server_Port = None


class MainWindow_Logic(demo_reader_MainWindow.Ui_MainWindow):
    def __init__(self):
        super(MainWindow_Logic, self).__init__()
        self.socket = None

    def Cliet_AS(self):
        # 创建socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((AS_IP, AS_Port))
        try:
            # 发送数据
            send_data = DES_call(generate_msg_to_AS('00', '0', '00001', str(self.lineEdit_username.text()),
                                                    'TGS', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                 str(self.lineEdit_passwd.text()), 0)
            self.socket.sendall(send_data.encode('utf-8'))

            # 接收数据
            # 将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                final_str_data = DES_call(total_data.decode('utf-8'), str(self.lineEdit_passwd.text()), 1)
                final_dict_data = json.loads(final_str_data)

            self.socket.close()
        except socket.error as e:
            print("Socket error: %s" % str(e))
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()
