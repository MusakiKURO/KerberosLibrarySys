# coding=utf-8
# @Time    : 2022/5/19 15:24
# @Author  : Nisky
# @File    : demo_MainWindow_logic.py
# @Software: PyCharm

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Client import demo_reader_MainWindow
from Client.demo_reader_MainWindow import Ui_MainWindow
from DES.demo_DES import DES_call
from RSA.demo_RSA import RSA_call
from werkzeug.security import generate_password_hash, check_password_hash
import json
import socket
import sys
import datetime

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

# 其他主体的公钥部分
# TGS
TGS_n = None
TGS_e = 65537
# AS
AS_n = None
AS_e = 65537
# S
S_n = None
S_e = 65537

# Kerberos流程中涉及的一些全局变量
# 由AS发给C的票据
global TGT
# C和TGS通信要用到的对称密钥
global EKc_tgs
# 由TGS发给C的票据
global ST
# C和S通信要用到的对称密钥
global EKc_v


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


C_n = 3951270249045146953972943163348434942592764989560360906533269897277080404934010181112385167732070275357806027491762234996305583674911212807857840660608406910051955297329683233106234207322044758397760274898933802535462100186118312888112180532109135970587764285970799040141296520625252128054797411575140828014980501308928204513652682136220524500675713399801045198810206992806199335791852827154930372510398253049468928422550127057850688190116699758746503012249254107915609637655541305024737077987890330855253602741330884459042041448515721767143012038195427206379154406467638677589417430783480145088864002792702243711871
C_d = 2757273636260153892397342107350259780423194855845766289858950397671128036969148536137032681933728579320666845526660699957063082811308337204049050565811744102070678725190020954569898057638571691346945552160656416853903721986232949376871604624486124103069872348296421143823823394078988290161741459382729076515559052021058495642905456516812473319945752701566826454688598762391217175129649908066837336480981333656504068536290700516972492847182109009403521746900589327304409884664070941216444164761014904237097127620724122770288299493272459500309150609158525585771453450568861932542872871536494818060418219971795890204521


class MainWindow_Logic(demo_reader_MainWindow.Ui_MainWindow):
    def __init__(self):
        super(MainWindow_Logic, self).__init__()

        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        # 创建socket
        self.socket = None

    def generate_msg_to_AS_register(self, src, result, target, ID_c, ID_pw):
        dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_c': ID_c, 'ID_pw': ID_pw}}
        str_msg_orign = json.dumps(dict_msg_orign)
        HMAC = generate_password_hash(str_msg_orign)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_c': ID_c, 'ID_pw': ID_pw},
                          'HMAC': RSA_call(HMAC, C_n, C_d, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_AS_Kerberos(self, src, result, target, ID_c, ID_tgs, TS_1):
        dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_c': ID_c, 'ID_tgs': ID_tgs, 'TS_1': TS_1}}
        str_msg_orign = json.dumps(dict_msg_orign)
        HMAC = generate_password_hash(str_msg_orign)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_c': ID_c, 'ID_tgs': ID_tgs, 'TS_1': TS_1},
                          'HMAC': RSA_call(HMAC, C_n, C_d, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_TGS_Kerberos(self, src, result, target, ID_v, Ticket_tgs, ID_c, AD_c, TS_3):
        dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_v': ID_v, 'tick_tgs': Ticket_tgs,
                                       'Authenticator': {'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_3}}}
        str_msg_orign = json.dumps(dict_msg_orign)
        HMAC = generate_password_hash(str_msg_orign)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_v': ID_v, 'tick_tgs': TGT,
                                       'Authenticator': DES_call(json.dumps({'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_3}),
                                                                 EKc_tgs, 0)},
                          'HMAC': RSA_call(HMAC, C_n, C_d, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_S_Kerberos(self, src, result, target, Ticket_v, ID_c, AD_c, TS_5):
        dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'tick_v': Ticket_v,
                                       'Authenticator': {'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_5}}}
        str_msg_orign = json.dumps(dict_msg_orign)
        HMAC = generate_password_hash(str_msg_orign)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'tick_v': ST,
                                       'Authenticator': DES_call(json.dumps({'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_5}),
                                                                 EKc_v, 0)},
                          'HMAC': RSA_call(HMAC, C_n, C_d, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_S_Search(self, src, result, target, select, content):
        dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'book_select': select, 'book_content': content}}
        str_msg_orign = json.dumps(dict_msg_orign)
        HMAC = generate_password_hash(str_msg_orign)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'book_select': select, 'book_content': content},
                          'HMAC': RSA_call(HMAC, C_n, C_d, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def C_AS_Register(self):
        self.socket.connect((AS_IP, AS_Port))
        try:
            # 发送数据
            send_data = DES_call(
                self.generate_msg_to_AS_register('00', '0', '00000', str(self.lineEdit_username.text()), 'TGS'),
                str(self.lineEdit_passwd.text()), 0)
            self.socket.sendall(send_data.encode('utf-8'))
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                final_str_data = DES_call(total_data.decode('utf-8'), str(self.lineEdit_passwd.text()), 1)
                final_loads_data = json.loads(final_str_data)
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'EKc_tgs': final_loads_data['data_msg']['EKc_tgs'],
                                  'ID_tgs': final_loads_data['data_msg']['ID_tgs'],
                                  'TS_2': final_loads_data['data_msg']['TS_2'],
                                  'tick_tgs': final_loads_data['data_msg']['tick_tgs']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], AS_n, AS_e, 1), final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
        except socket.error as e:
            print("Socket error: %s" % str(e))
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()

    def C_AS_Kerberos(self):
        global TGT
        global EKc_tgs
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((AS_IP, AS_Port))
        try:
            # 发送数据
            send_data = self.generate_msg_to_AS_Kerberos('00', '0', '00001', str(self.lineEdit_username.text()), 'TGS',
                                                         datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.socket.sendall(send_data.encode('utf-8'))
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                final_str_data = DES_call(total_data.decode('utf-8'), str(self.lineEdit_passwd.text()), 1)
                final_loads_data = json.loads(final_str_data)
                ###
                # 收到来自TGS的正确消息的情况
                if final_loads_data['control_msg']['control_result'] == '0':
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': {'EKc_tgs': final_loads_data['data_msg']['EKc_tgs'],
                                      'ID_tgs': final_loads_data['data_msg']['ID_tgs'],
                                      'TS_2': final_loads_data['data_msg']['TS_2'],
                                      'lifetime_2': final_loads_data['data_msg']['lifetime_2'],
                                      'tick_tgs': final_loads_data['data_msg']['tick_tgs']}})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], AS_n, AS_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        QMessageBox.information(self, "提示", "AS认证通过！", QMessageBox.Yes, QMessageBox.Yes)
                        TGT = final_loads_data['data_msg']['tick_tgs']
                        EKc_tgs = final_loads_data['data_msg']['EKc_tgs']
                # 收到来自TGS的错误消息的情况
                if final_loads_data['control_msg']['control_result'] == '1':
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': {'EKc_tgs': final_loads_data['data_msg']['EKc_tgs'],
                                      'ID_tgs': final_loads_data['data_msg']['ID_tgs'],
                                      'TS_2': final_loads_data['data_msg']['TS_2'],
                                      'lifetime_2': final_loads_data['data_msg']['lifetime_2'],
                                      'tick_tgs': final_loads_data['data_msg']['tick_tgs']}})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], AS_n, AS_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        QMessageBox.information(self, "提示", "AS认证不通过！", QMessageBox.Yes, QMessageBox.Yes)
                ###
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()

    def C_TGS_Kerberos(self):
        global TGT
        global EKc_tgs
        global ST
        global EKc_v
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TGS_IP, TGS_Port))
        try:
            # 发送数据
            send_data = self.generate_msg_to_TGS_Kerberos('00', '0', '00010', 'S', TGT,
                                                          str(self.lineEdit_username.text()),
                                                          get_host_ip(),
                                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.socket.sendall(send_data.encode('utf-8'))
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                final_str_data = DES_call(total_data.decode('utf-8'), EKc_tgs, 1)
                final_loads_data = json.loads(final_str_data)
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'EKc_v': final_loads_data['data_msg']['EKc_v'],
                                  'ID_v': final_loads_data['data_msg']['ID_v'],
                                  'TS_4': final_loads_data['data_msg']['TS_4'],
                                  'lifetime_4': final_loads_data['data_msg']['lifetime_4'],
                                  'tick_v': final_loads_data['data_msg']['tick_v']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], TGS_n, TGS_e, 1), final_dumps_data)
                ST = final_loads_data['data_msg']['tick_v']
                EKc_v = final_loads_data['data_msg']['EKc_v']
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", "TGS认证通过！", QMessageBox.Yes, QMessageBox.Yes)
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()

    def C_S_Kerberos(self):
        global ST
        global EKc_v
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TGS_IP, TGS_Port))
        TS_5 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # 发送数据
            send_data = self.generate_msg_to_S_Kerberos('00', '0', '00011', ST, str(self.lineEdit_username.text()),
                                                        get_host_ip(),
                                                        TS_5)
            self.socket.sendall(send_data.encode('utf-8'))
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                final_str_data = DES_call(total_data.decode('utf-8'), EKc_v, 1)
                final_loads_data = json.loads(final_str_data)
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'TS_6': final_loads_data['data_msg']['TS_6']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], TGS_n, TGS_e, 1), final_dumps_data)
                ST = final_loads_data['data_msg']['tick_v']
                EKc_v = final_loads_data['data_msg']['EKc_v']
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", "TGS认证通过！", QMessageBox.Yes, QMessageBox.Yes)
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow_Logic()
    ui.show()
    sys.exit(app.exec_())
