# @Time    : 2022/5/19 15:24
# @Author  : Nisky
# @File    : demo_MainWindow_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from KerberosLibrarySys.Client import demo_reader_MainWindow
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
    def __init__(self, num):
        super(MainWindow_Logic, self).__init__()
        self.socket = None

    def Cliet_AS(self):
        # 创建socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((AS_IP, AS_Port))
        try:
            # 发送数据
            send_data = " "
            self.socket.send(send_data.encode('utf-8'))

            # 接收数据
            recv_data = self.socket.recv(1024)

            print("Message from server: %s" % recv_data.decode('utf-8'))
            self.socket.close()
        except socket.error as e:
            print("Socket error: %s" % str(e))
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()
