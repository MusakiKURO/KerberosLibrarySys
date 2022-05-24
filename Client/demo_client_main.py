# @Time    : 2022/5/19 15:02
# @Author  : Nisky
# @File    : demo_client_main.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from KerberosLibrarySys.Client import demo_MainWindow_logic
import socket
import sys


class MainWindow(demo_MainWindow_logic.MainWindow_Logic):
    def __init__(self):
        super(MainWindow, self).__init__()

    def connect(self):
        super(MainWindow, self).connect()
        self.pushButton_register.clicked.connect(self.C_AS_Register)
        self.pushButton_login.clicked.connect(self.C_AS_Kerberos)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
