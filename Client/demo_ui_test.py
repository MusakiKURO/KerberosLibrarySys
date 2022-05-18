# @Time    : 2022/5/17 22:47
# @Author  : Nisky
# @File    : demo_ui_test.py
# @Software: PyCharm
from PyQt5.QtCore import QCoreApplication
from demo_reader_secondpage_2 import *
from demo_reader_firstpage_5 import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import sys


class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)


class childWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child = Ui_Dialog()
        self.child.setupUi(self)


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = parentWindow()
    child = childWindow()
    # 显示
    window.show()
    child.show()
    sys.exit(app.exec_())
