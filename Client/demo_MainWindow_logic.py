# @Time    : 2022/5/19 15:24
# @Author  : Nisky
# @File    : demo_MainWindow_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from KerberosLibrarySys.Client import demo_reader_MainWindow
import socket
import threading
import sys


class MainWindow_Logic(demo_reader_MainWindow.Ui_MainWindow):
    def __init__(self, num):
        super(MainWindow_Logic, self).__init__()
        self.socket = None
        
    def Cliet_start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
