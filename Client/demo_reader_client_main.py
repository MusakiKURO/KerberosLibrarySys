# coding=utf-8
# @Time    : 2022/5/19 15:02
# @Author  : Nisky
# @File    : demo_reader_client_main.py
# @Software: PyCharm
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
from Client import demo_reader_logic
import sys


class MainWindow_Test(demo_reader_logic.Reader_Logic):
    def __init__(self):
        super(MainWindow_Test, self).__init__()
        self.pushButton_login.clicked.connect(self.Kerberos)


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow_Test()
    ui.show()
    sys.exit(app.exec_())
