# @Time    : 2022/5/19 15:02
# @Author  : Nisky
# @File    : demo_reader_client_main.py
# @Software: PyCharm
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
from KerberosLibrarySys.Client import demo_reader_logic
import sys


class MainWindow_Test(demo_reader_logic.Reader_Logic):
    def __init__(self):
        super(MainWindow_Test, self).__init__()
        self.pushButton_register.clicked.connect(self.C_AS_Register)
        self.pushButton_login.clicked.connect(self.C_AS_Kerberos)
        self.pushButton_search.clicked.connect(self.C_S_Search)


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow_Test()
    ui.show()
    sys.exit(app.exec_())
