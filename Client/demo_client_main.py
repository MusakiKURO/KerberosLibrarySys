# @Time    : 2022/5/19 15:02
# @Author  : Nisky
# @File    : demo_client_main.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from demo_reader_MainWindow import *
from demo_reader_Dialog import *
import socket
import sys


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class MainWindow():
    def connect(self):
        super(MainWindow, self).connect()
