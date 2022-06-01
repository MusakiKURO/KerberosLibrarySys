import json
import operator
import threading
from socket import *
from DES.demo_DES import *
from RSA.demo_RSA import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from control_target import control_target
from library_db_management import *


# 创建线程类
# class MyThread(threading.Thread):
#     def __init__(self, func, argc, name=''):
#         threading.Thread.__init__(self)
#         self.name = name
#         self.func = func
#         self.argc = argc


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
        control_msg = {'control_src': self.src, 'control_result': self.result, 'control_target': self.target}
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
    def __int__(self, tips=''):
        self.tips = tips

    def create_data_msg(self):
        data_tips = {'tips': self.tips}
        return data_tips

    def create_Kdata_msg(self):
        data_tips = {'TS_6': self.tips}
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
            Ticket_v = json.loads(DES_call(all_msg['data_msg']['ticket_V'], EKv, 1))
            EKc_v = Ticket_v['EKc_v']
            Auth = json.loads(DES_call(all_msg['data_msg']['Authenticator'], EKc_v, 1))
            Lifetime_str = Ticket_v['Lifetime']
            TS_5_str = Auth['TS_5']
            Lifetime_dt = datetime.strptime(Lifetime_str, '%Y-%m-%d %H:%M:%S')
            TS_5_dt = datetime.strptime(TS_5_str, '%Y-%m-%d %H:%M:%S')
            if operator.eq(Ticket_v['ID_c'], Auth['ID_c']) and operator.eq(Ticket_v['AD_c'],
                                                                           Auth['AD_c']) and Lifetime_dt >= TS_5_dt:
                TS_6_dt = TS_5_dt + timedelta(seconds=1)
                TS_6_dt.strptime()
                TS_6 = data_msg()
                TS_6.tips = TS_6_dt
                data_msg_dt = TS_6.create_Kdata_msg()
                control_msg = con_msg('0', control_target[0])
                con_msg_dt = control_msg.create_con_msg()
                str_msg_final = json.dumps(create_send_msg(con_msg_dt, data_msg_dt, EKc_v))
                sock.sendall(str_msg_final.encode('utf-8'))
            else:
                Ker_error = data_msg()
                Ker_error.tips = '认证错误'
                data_msg_dt = Ker_error.create_data_msg()
                control_msg = con_msg('1', control_target[0])
                con_msg_dt = control_msg.create_con_msg()
                str_msg_final = json.dumps(create_send_msg(con_msg_dt, data_msg_dt, EKc_v))
                sock.sendall(str_msg_final.encode('utf-8'))


#
# def create_send_msg(control_msg_dt, data_msg_dt, EKc_v):
#     dict_msg_origin = {'control_msg': control_msg_dt,
#                        'data_msg': DES_call(json.dumps(data_msg_dt), EKc_v, 0)}
#     str_msg_origin = json.dumps(dict_msg_origin)
#     HMAC = generate_password_hash(str_msg_origin)
#     dict_msg_origin['HMAC'] = RSA_call(HMAC, S_n, S_d, 0)
#     return dict_msg_origin


def hash_cmp(data):
    data = json.loads(data)
    HMAC = data['HMAC']
    del data['HMAC']
    data = json.dumps(data)
    hash_check = check_password_hash(RSA_call(HMAC, C_n, C_e, 1),
                                     data)
    return hash_check


# 设定基础数据
HOST = ''
PORT = 21567
ADDR = (HOST, PORT)
BUFFSIZE = 1024
EKv = None
C_n = 3951270249045146953972943163348434942592764989560360906533269897277080404934010181112385167732070275357806027491762234996305583674911212807857840660608406910051955297329683233106234207322044758397760274898933802535462100186118312888112180532109135970587764285970799040141296520625252128054797411575140828014980501308928204513652682136220524500675713399801045198810206992806199335791852827154930372510398253049468928422550127057850688190116699758746503012249254107915609637655541305024737077987890330855253602741330884459042041448515721767143012038195427206379154406467638677589417430783480145088864002792702243711871
C_e = 65537
S_n = 10469390129546136402029942747457300548433313561152500694655265739940475404319462139530628254855322586969734523342743903668412559804045845034210748615835404649037119900853265926666451144690640278649024315138788684707831566351503299322478262056212399670974114581850558320339645904277358701922873391829160151236405533264476749760758974104883363191923240109341780901794063881916334145879532060236519390370906919172355572965775460432228690239610801536843235695767284700782343713226170627931582080505723902106175293364974962491182627509560208769591792202469015835052126845105188154599166838191586917087104257804552326005823
S_e = 65537
S_d = 8110714186754298143092669075085860864016604301796462536720282468655230133025737091234707993278826287221376645546146352091988380401468111815874210426525400382088173880496849377126036552149674050194062324003640372613730019482102102830475400477867707647507480439289508934499359168896502067748418875596229903696601538947599762970083498153007126984514457653542261324691019431373092778414249493081800991492478535451747689826738343974509191893347816832399493117974542984766167012840616050188269725303380603488917126926095089931521535057761266939722944819520741894548836638416431206454098874309067605170447054752532589197921
