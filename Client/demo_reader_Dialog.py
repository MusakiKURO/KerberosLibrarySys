# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo_reader_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QApplication
import sys


class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(698, 425)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.tableWidget_result = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_result.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget_result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableWidget_result.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_result.setObjectName("tableWidget_result")
        self.tableWidget_result.setColumnCount(5)
        self.tableWidget_result.setRowCount(12)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_result.setHorizontalHeaderItem(4, item)
        self.gridLayout.addWidget(self.tableWidget_result, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.label_result = QtWidgets.QLabel(Dialog)
        self.label_result.setObjectName("label_result")
        self.gridLayout.addWidget(self.label_result, 3, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_select = QtWidgets.QLabel(Dialog)
        self.label_select.setObjectName("label_select")
        self.horizontalLayout.addWidget(self.label_select)
        self.comboBox_select = QtWidgets.QComboBox(Dialog)
        self.comboBox_select.setObjectName("comboBox_select")
        self.comboBox_select.addItem("")
        self.comboBox_select.addItem("")
        self.comboBox_select.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_select)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.label_content = QtWidgets.QLabel(Dialog)
        self.label_content.setObjectName("label_content")
        self.horizontalLayout.addWidget(self.label_content)
        self.lineEdit_content = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_content.setObjectName("lineEdit_content")
        self.horizontalLayout.addWidget(self.lineEdit_content)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.pushButton_search = QtWidgets.QPushButton(Dialog)
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout.addWidget(self.pushButton_search)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 1, 1, 1)

        # 设置字体
        font = QtGui.QFont()
        font.setFamily("Yuppy TC")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font_1 = QtGui.QFont()
        font_1.setFamily("Yuppy TC")
        font_1.setPointSize(10)
        font_1.setBold(True)
        font_1.setItalic(False)
        font_1.setUnderline(True)
        font_1.setWeight(75)
        font_1.setStrikeOut(False)
        self.label_select.setFont(font_1)
        self.label_content.setFont(font_1)
        self.label_result.setFont(font)
        self.label_result.setAlignment(QtCore.Qt.AlignCenter)
        # 对TableWidget控件的修改
        # 让表格铺满整个QTableWidget控件
        self.tableWidget_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 将表格变为禁止编辑
        self.tableWidget_result.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 表格填满窗口
        self.tableWidget_result.resizeColumnsToContents()
        self.tableWidget_result.resizeRowsToContents()
        # 解决表头与第一行之间网格线不显示
        self.tableWidget_result.setStyleSheet("QHeaderView::section{background:skyblue;color: black;}")
        # 允许右键产生菜单
        self.tableWidget_result.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 将右键菜单绑定到槽函数generateMenu
        self.tableWidget_result.customContextMenuRequested.connect(self.generateMenu)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.tableWidget_result.setSortingEnabled(False)
        item = self.tableWidget_result.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_result.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget_result.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "3"))
        item = self.tableWidget_result.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "4"))
        item = self.tableWidget_result.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "5"))
        item = self.tableWidget_result.verticalHeaderItem(5)
        item.setText(_translate("Dialog", "6"))
        item = self.tableWidget_result.verticalHeaderItem(6)
        item.setText(_translate("Dialog", "7"))
        item = self.tableWidget_result.verticalHeaderItem(7)
        item.setText(_translate("Dialog", "8"))
        item = self.tableWidget_result.verticalHeaderItem(8)
        item.setText(_translate("Dialog", "9"))
        item = self.tableWidget_result.verticalHeaderItem(9)
        item.setText(_translate("Dialog", "10"))
        item = self.tableWidget_result.verticalHeaderItem(10)
        item.setText(_translate("Dialog", "11"))
        item = self.tableWidget_result.verticalHeaderItem(11)
        item.setText(_translate("Dialog", "12"))
        item = self.tableWidget_result.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "书号"))
        item = self.tableWidget_result.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "书名"))
        item = self.tableWidget_result.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "作者"))
        item = self.tableWidget_result.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "出版社"))
        item = self.tableWidget_result.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "当前库存"))
        self.label_result.setText(_translate("Dialog", "搜索结果展示"))
        self.label_select.setText(_translate("Dialog", "搜索条件"))
        self.comboBox_select.setItemText(0, _translate("Dialog", "书号"))
        self.comboBox_select.setItemText(1, _translate("Dialog", "书名"))
        self.comboBox_select.setItemText(2, _translate("Dialog", "作者"))
        self.label_content.setText(_translate("Dialog", "搜索内容"))
        self.pushButton_search.setText(_translate("Dialog", "查找"))


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
