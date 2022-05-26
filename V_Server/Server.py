import json
import operator
import threading
from socket import *
from DES.demo_DES import *
from RSA.demo_RSA import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from control_target import control_target


# 创建线程类
class MyThread(threading.Thread):
    def __init__(self, func, argc, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.argc = argc

    def run(self):
        self.func(*self.argc)


# 创建用户类
# class user():
# def __init__(self, username, conn='', addr=''):
#    self.name = username
#    self.conn = conn
#   self.addr = addr

# def conn_msg(self):
#    print('connected from ' + self.addr + ' by ' + self.addr)


# 创建消息类
class msg:
    def __init__(self, con_msg_dt, data_msg_dt='', HMAC=''):
        self.con_msg = con_msg_dt
        self.data_msg = data_msg_dt
        self.HMAC = HMAC

    def create_msg(self):
        send_msg = {'control_msg': self.con_msg,
                    'data_msg': self.data_msg,
                    'HMAC': self.HMAC}
        return send_msg


# 创建控制报文
class con_msg:
    def __init__(self, result, target, src='11'):
        self.src = src
        self.result = result
        self.target = target

    def create_con_msg(self):
        control_msg = {'con_src': self.src, 'con_result': self.result, 'con_target': self.target}
        return control_msg


# 创建数据报文类（查询图书）
class search_msg:
    def __init__(self, book_number, book_name, book_author, book_press, book_inventory):
        self.number = book_number
        self.name = book_name
        self.author = book_author
        self.press = book_press
        self.inventory = book_inventory

    def create_search_msg(self):
        book_msg = {'book_number': self.number, 'book_name': self.name, 'book_author': self.author,
                    'book_press': self.press, 'book_inventory': self.inventory}
        return book_msg


# 创建数据报文类
class data_msg:
    def __int__(self, tips):
        self.tips = tips

    def create_data_msg(self):
        data_tips = {'tips': self.tips}
        return data_tips

    def create_Kdata_msg(self):
        data_tips = {'ST_6': self.tips}
        return data_tips


def V_to_C_Ker(sock):
    all_msg = None
    while True:
        recv_data = sock.recv(BUFFSIZE)
        all_msg += recv_data
        if len(recv_data) < 1024:
            break
    if all_msg:
        final_str_data = all_msg.decode('utf-8')
        if hash_cmp(final_str_data):
            all_msg = json.loads(all_msg)
            if all_msg['control_msg']['control_result'] == '0':
                Ticket_v = json.loads(DES_call(all_msg['data_msg']['ticket_V'], EKtgs_v, 1))
                EKc_v = Ticket_v['EKc_v']
                Auth = json.loads(DES_call(all_msg['data_msg']['Authenticator'], EKc_v, 1))
                Lifetime_str = Ticket_v['Lifetime']
                TS_5_str = Auth['TS_5']
                Lifetime_dt = datetime.strptime(Lifetime_str, '%Y-%m-%d %H:%M:%S')
                TS_5_dt = datetime.strptime(TS_5_str, '%Y-%m-%d %H:%M:%S')
                if operator.eq(Ticket_v['ID_c'], Auth['ID_c']) and operator.eq(Ticket_v['AD_c'],
                                                                               Auth['AD_c']) and Lifetime_dt >= TS_5_dt:
                    TS_6_dt = TS_5_dt + timedelta(seconds=1)
                    TS_6 = data_msg()
                    TS_6.tips = TS_6_dt
                    data_msg_dt = TS_6.create_Kdata_msg()
                    control_msg = con_msg('0', control_target[0])
                    con_msg_dt = control_msg.create_con_msg()
                    str_msg_final = json.dumps(create_send_msg(con_msg_dt, data_msg_dt, EKc_v))
                    sock.sendall(str_msg_final)
                else:
                    Ker_error = data_msg()
                    Ker_error.tips = '认证错误'
                    data_msg_dt = Ker_error.create_data_msg()
                    control_msg = con_msg('1', control_target[0])
                    con_msg_dt = control_msg.create_con_msg()
                    str_msg_final = json.dumps(create_send_msg(con_msg_dt, data_msg_dt, EKc_v))
                    sock.sendall(str_msg_final)


def create_send_msg(control_msg_dt, data_msg_dt, EKc_v):
    dict_msg_origin = {'control_msg': control_msg_dt,
                       'data_msg': DES_call(json.dumps(data_msg_dt), EKc_v, 1)}
    str_msg_origin = json.dumps(dict_msg_origin)
    HMAC = generate_password_hash(str_msg_origin)
    dict_msg_origin['HMAC'] = RSA_call(HMAC, V_n, V_d, 0)
    return dict_msg_origin


def hash_cmp(data):
    data = json.loads(data)
    HMAC = data['HMAC']
    del data['HMAC']
    data = json.dumps(data)
    hash_check = check_password_hash(RSA_call(HMAC, C_n, C_e, 1, ),
                                     data)
    return hash_check


# 设定基础数据
HOST = ''
PORT = 21567
ADDR = (HOST, PORT)
BUFFSIZE = 1024
EKtgs_v = None
C_n = C_e = None
V_n = V_d = None
# 连接
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind(ADDR)

while True:
    server_sock.listen(5)
    client_sock, client_addr = server_sock.accept()
    t = MyThread(V_to_C_Ker, client_sock)
    t.start()
