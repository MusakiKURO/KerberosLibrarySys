# @Time    : 2022/5/17 22:47
# @Author  : Nisky
# @File    : demo_ui_test.py
# @Software: PyCharm
from PyQt5.QtCore import QCoreApplication
from demo_reader_Dialog_ui import *
from demo_reader_MainWindow_ui import *
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
    # 通过toolButton将两个窗体关联
    jump = window.main_ui.pushButton_login
    jump.clicked.connect(child.show)
    # 显示
    window.show()
    sys.exit(app.exec_())
