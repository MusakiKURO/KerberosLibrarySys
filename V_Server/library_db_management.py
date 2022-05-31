# 实现操作数据库的函数与类
from pymysql.cursors import DictCursor

from Server import *
import pymysql
# from Server import *
import json
import operator
import threading
import pymysql
from socket import *
from DES.demo_DES import *
from RSA.demo_RSA import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from V_Server.Server import con_msg, data_msg
from control_target import control_target

db = pymysql.connect(host='localhost', user='root', password='QIjiu111.', database='library_manager_system')
cursor = db.cursor(DictCursor)

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
# 连接

'''实现一个能够选择函数，该选择函数能够处理客户端的控制报文，
    并根据控制报文中的control_target来完成对功能的选择，
    
    输入：control_msg_dt,data_msg_dict
    输出：str_msg_final(未encode)'''


def control_target_select(control_msg_dict, data_msg_dict):
    RSA_n = None
    RSA_e = None
    EKc_v = None
    match control_msg_dict[control_target]:
        case '00101':
            str_msg_final, RSA_n, RSA_e, EKc_v = Kerberos(data_msg_dict)
        case '00110':
            str_msg_final = search_book(data_msg_dict, 0)
        case '00111':
            str_msg_final = search_book(data_msg_dict, 1)
        case '01000':
            str_msg_final = search_book(data_msg_dict, 2)
        case '01001':
            str_msg_final = reserve_book(data_msg_dict)
        case '01010':
            str_msg_final = borrowe_book(data_msg_dict)
        case '01011':
            str_msg_final = return_book(data_msg_dict)
        case '01100':
            str_msg_final = add_book(data_msg_dict)
        case '01101':
            str_msg_final = modify_book(data_msg_dict)
        case '01110':
            str_msg_final = remove_book(data_msg_dict)
        case _:
            control_target_error = data_msg()
            control_target_error.tips = '未知目标报文'
            data_msg_dict = control_target_error.create_data_msg()
            control_msg = con_msg('1', control_target[0])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    return str_msg_final


'''kerberos的认证流程
    输入：data_msg
    输出：str_msg_final(未encode)'''


def Kerberos(data):
    Ticket_v = json.loads(DES_call(data['ticket_V'], EKv, 1))
    EKc_v = Ticket_v['EKc_v']
    Auth = json.loads(DES_call(data['Authenticator'], EKc_v, 1))
    Lifetime_str = Ticket_v['Lifetime']
    TS_5_str = Auth['TS_5']
    Lifetime_dt = datetime.strptime(Lifetime_str, '%Y-%m-%d %H:%M:%S')
    TS_5_dt = datetime.strptime(TS_5_str, '%Y-%m-%d %H:%M:%S')
    get_RSA_n, get_RSA_e = get_RSA(Ticket_v['ID_c'])
    if operator.eq(Ticket_v['ID_c'], Auth['ID_c']) and operator.eq(Ticket_v['AD_c'],
                                                                   Auth['AD_c']) and Lifetime_dt >= TS_5_dt:
        TS_6_dt = TS_5_dt + timedelta(seconds=1)
        TS_6_dt.strptime()
        TS_6 = data_msg()
        TS_6.tips = TS_6_dt
        data_msg_dt = TS_6.create_Kdata_msg()
        control_msg = con_msg('0', control_target[0])
        con_msg_dt = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dt, data_msg_dt))
    else:
        Ker_error = data_msg()
        Ker_error.tips = '认证错误'
        data_msg_dt = Ker_error.create_data_msg()
        control_msg = con_msg('1', control_target[0])
        con_msg_dt = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dt, data_msg_dt))
    return str_msg_final, get_RSA_n, get_RSA_e,EKc_v


'''实现查阅图书功能
    输入：data_msg,key_values
    输出：str_msg_final(未encode)'''


def search_book(data, key_values):
    data_msg_dt = json.loads(DES_call(data, EKc_v, 1))
    book_content = data_msg_dt['book_content']
    if key_values == 0:
        sql = "SELECT * FROM BOOK WHERE BOOK_ID='%c'" % book_content
    elif key_values == 1:
        sql = "SELECT * FROM BOOK WHERE BOOK_NAME='%c'" % book_content
    else:
        sql = "SELECT * FROM BOOK WHERE book_author='%c'" % book_content
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        data_msg_dict = results[0]
        data_msg_str = DES_call(json.dumps(data_msg_dict), EKc_v, 0)
        control_msg = con_msg('0', control_target[1])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_str))
    else:
        search_data_msg = data_msg()
        search_data_msg.tips = '不存在该图书'
        data_msg_dict = search_data_msg.create_data_msg()
        control_msg = con_msg('1', control_target[1])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    return str_msg_final


'''实现借阅图书功能
    输入：data_msg
    输出：str_msg_final(未encode)'''


def borrowe_book(data):
    data_msg_dt = json.loads(DES_call(data, EKc_v, 1))
    book_id = data_msg_dt['book_id']
    sql = "SELECT BOOK_INVENTORY FROM BOOK WHERE BOOK_ID='%c'" % book_id
    cursor.execute(sql)
    results = cursor.fetchall()
    book_inventory = results[0]['book_inventory']
    if book_inventory:
        sql = "UPDATE BOOK WHERE BOOK_INVENTORY = BOOK_INVENTORY-1 WHERE BOOK_ID = '%c'" % book_id
        try:
            cursor.execute(sql)
            db.commit()
            borrowe_data_msg = data_msg()
            borrowe_data_msg.tips = '借阅成功'
            data_msg_dict = borrowe_data_msg.create_data_msg()
            control_msg = con_msg('0', control_target[3])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
        except:
            db.rollback()
            error_data_msg = data_msg()
            error_data_msg.tips = '借阅失败'
            data_msg_dict = error_data_msg.create_data_msg()
            control_msg = con_msg('1', control_target[3])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    else:
        error_data_msg = data_msg()
        error_data_msg.tips = '借阅失败'
        data_msg_dict = error_data_msg.create_data_msg()
        control_msg = con_msg('1', control_target[3])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    return str_msg_final


'''实现预约图书功能
    输入：data_msg
    输出：str_msg_final(未encode)'''


def reserve_book(data):
    data_msg_dt = json.loads(DES_call(data, EKc_v, 1))
    book_id = data_msg_dt['book_id']
    sql = "SELECT BOOK_ID FROM BOOK_RESERVATION WHERE BOOK_ID='%c'" % book_id
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        sql = "INSERT INTO BOOK_RESERVATION(BOOK_ID,READER_NUMBER) VALUES ('%c,1')" % book_id
        try:
            cursor.execute(sql)
            db.commit()
            reserve_data_msg = data_msg()
            reserve_data_msg.tips = '借阅成功'
            data_msg_dict = reserve_data_msg.create_data_msg()
            control_msg = con_msg('0', control_target[2])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
        except:
            db.rollback()
            error_data_msg = data_msg()
            error_data_msg.tips = '预约失败'
            data_msg_dict = error_data_msg.create_data_msg()
            control_msg = con_msg('1', control_target[2])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    else:
        sql = "UPDATE BOOK_RESERVATION SET READER_NUMBER = READER_NUMBER+1 WHERE BOOK_ID='%c'" % book_id
        try:
            cursor.execute(sql)
            db.commit()
            reserve_data_msg = data_msg()
            reserve_data_msg.tips = '借阅成功'
            data_msg_dict = reserve_data_msg.create_data_msg()
            control_msg = con_msg('0', control_target[2])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
        except:
            db.rollback()
            error_data_msg = data_msg()
            error_data_msg.tips = '预约失败'
            data_msg_dict = error_data_msg.create_data_msg()
            control_msg = con_msg('1', control_target[2])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    return str_msg_final


'''实现归还图书功能
    输入：data_msg
    输出：str_msg_final(未encode)'''


def return_book(data):
    data_msg_dt = json.loads(DES_call(data, EKc_v, 1))
    book_id = data_msg_dt['book_id']
    sql = "UPDATE BOOK SET BOOK_INVENTORY = BOOK_INVENTORY+1 WHERE BOOK_ID='%c" % book_id
    try:
        cursor.execute(sql)
        db.commit()
        return_data_msg = data_msg()
        return_data_msg.tips = '归还成功'
        data_msg_dict = return_data_msg.create_data_msg()
        control_msg = con_msg('0', control_target[7])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    except:
        db.rollback()
        error_data_msg = data_msg()
        error_data_msg.tips = '归还失败'
        data_msg_dict = error_data_msg.create_data_msg()
        control_msg = con_msg('1', control_target[7])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    return str_msg_final


'''实现增加图书图书功能
    输入：data_msg
    输出：str_msg_final(未encode)'''


def add_book(data):
    data_msg_dt = json.loads(DES_call(data, EKc_v, 1))
    book_id = data_msg_dt['book_id']
    book_name = data_msg_dt['book_name']
    book_author = data_msg_dt['book_author']
    book_press = data_msg_dt['book_press']
    book_totalnum = data_msg_dt['book_totalnum']
    sql = "INSERT INTO BOOK(BOOK_ID,BOOK_NAME,BOOK_AUTHOR,BOOK_PRESS,BOOK_INVENTORY,BOOK_TOTALNUM)" \
          "VALUES ('%c','%c','%c','%c',%d,%d)" % (
              book_id, book_name, book_author, book_press, book_totalnum, book_totalnum)
    try:
        cursor.execute(sql)
        db.commit()
        add_data_msg = data_msg()
        add_data_msg.tips = '增加成功'
        data_msg_dict = add_data_msg.create_data_msg()
        control_msg = con_msg('0', control_target[6])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    except:
        db.rollback()
        error_data_msg = data_msg()
        error_data_msg.tips = '增加失败'
        data_msg_dict = error_data_msg.create_data_msg()
        control_msg = con_msg('1', control_target[6])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    return str_msg_final


'''实现修改图书功能
    输入：data_msg
    输出：str_msg_final(未encode)'''


def modify_book(data):
    data_msg_dt = json.loads(DES_call(data, EKc_v, 1))
    book_id = data_msg_dt['book_id']
    book_name = data_msg_dt['book_name']
    book_author = data_msg_dt['book_author']
    book_press = data_msg_dt['book_press']
    book_totalnum = data_msg_dt['book_totalnum']
    sql = "SELECT BOOK_TOTALNUM FROM BOOK WHERE BOOK_ID='%c'" % book_id
    cursor.execute(sql)
    results = cursor.fetchall()
    book_origin_totalnum = results[0]['book_totalnum']
    sql = "UPDATE BOOK SET BOOK_INVENTORY = BOOK_INVENTOR + %d WHERE BOOK_ID ='%c'" % (
        book_totalnum - book_origin_totalnum, book_id)
    try:
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE BOOK SET BOOK_NAME='%c',BOOK_AUTHOR='%c',BOOK_PRESS='%c',BOOK_TOTALNUM=%d WHERE BOOK_ID='%c'" \
              % (book_name, book_author, book_press, book_totalnum, book_id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            db.rollback()
            error_data_msg = data_msg()
            error_data_msg.tips = '修改失败'
            data_msg_dict = error_data_msg.create_data_msg()
            control_msg = con_msg('1', control_target[5])
            con_msg_dict = control_msg.create_con_msg()
            str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
            return str_msg_final
        modify_data_msg = data_msg()
        modify_data_msg.tips = '修改成功'
        data_msg_dict = modify_data_msg.create_data_msg()
        control_msg = con_msg('0', control_target[5])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    except:
        db.rollback()
        error_data_msg = data_msg()
        error_data_msg.tips = '修改失败'
        data_msg_dict = error_data_msg.create_data_msg()
        control_msg = con_msg('1', control_target[5])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))

    return str_msg_final


'''实现删除图书功能
    输入：data_msg
    输出：str_msg_final(未encode)'''


def remove_book(data):
    data_msg_dt = json.loads(DES_call(data, EKc_v, 1))
    book_id = data_msg_dt['book_id']
    sql = "DELETE FROM BOOK WHERE BOOK_ID='%c'" % book_id
    try:
        cursor.execute(sql)
        db.commit()
        remove_data_msg = data_msg()
        remove_data_msg.tips = '删除成功'
        data_msg_dict = remove_data_msg.create_data_msg()
        control_msg = con_msg('0', control_target[4])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    except:
        db.rollback()
        error_data_msg = data_msg()
        error_data_msg.tips = '删除失败'
        data_msg_dict = error_data_msg.create_data_msg()
        control_msg = con_msg('1', control_target[4])
        con_msg_dict = control_msg.create_con_msg()
        str_msg_final = json.dumps(create_send_msg(con_msg_dict, data_msg_dict))
    return str_msg_final


# '''实现生成数据功能
#     输入：control_msg_dict,data_msg_dict,EKc_v
#     输出：str_msg_final(没有encode，发送前需要encode)'''
# def create_send_msg(control_msg_dt,data_msg_dt,EKc_v):
#     dict_msg_origin = {'control_msg': control_msg_dt,
#                        'data_msg': DES_call(json.dumps(data_msg_dt), EKc_v, 0)}
#     str_msg_origin = json.dumps(dict_msg_origin)
#     HMAC = generate_password_hash(str_msg_origin)
#     dict_msg_origin['HMAC'] = RSA_call(HMAC, S_n, S_d, 0)
#     str_msg_final = json.dumps(dict_msg_origin)
#     return str_msg_final

'''从数据库中获取用户的密钥
    输入：ID_c
    输出:RSA_n,RSA_e'''


def get_RSA(ID_c):
    sql = "SELECT * FROM USER_RSA WHERE USER_ID='%c'" % ID_c
    cursor.execute(sql)
    results = cursor.fetchall()
    RSA_n = int(results[0]['user_RSA_n'])
    RSA_e = int(results[0]['user_RSA_e'])
    return RSA_n, RSA_e


'''在得到数据之后可以根据data中的HMAC
    对数据进行报文完整性检测'''


def hash_cmp(data):
    data = json.loads(data)
    HMAC = data['HMAC']
    del data['HMAC']
    data = json.dumps(data)
    hash_check = check_password_hash(RSA_call(HMAC, C_n, C_e, 1),
                                     data)
    return hash_check


'''生成发送信息（不加密data_msg）
    如果data_msg需要加密则在函数前加密
    输入：control_msg_dt,data_msg_dt
    输出：dict_msg_origin(未dumps)'''


def create_send_msg(control_msg, data_msg_dict):
    dict_msg_origin = {'control_msg': control_msg,
                       'data_msg': data_msg_dict}
    str_msg_origin = json.dumps(dict_msg_origin)
    HMAC = generate_password_hash(str_msg_origin)
    dict_msg_origin['HMAC'] = RSA_call(HMAC, S_n, S_d, 0)
    return dict_msg_origin


def total_process(sock):
    all_msg = None
    while True:
        recv_data = sock.recv(BUFFSIZE)
        all_msg += recv_data
        if len(recv_data) < 1024:
            break
        if all_msg:
            all_msg = all_msg.decode('utf-8')
            if hash_cmp(all_msg):
                str_msg_final = control_target_select(all_msg['control_msg'], all_msg['data_msg'])
                sock.sendall(str_msg_final.encode('utf-8'))
            else:
                Ker_error = data_msg()
                Ker_error.tips = '认证错误'
                data_msg_dt = Ker_error.create_data_msg()
                control_msg = con_msg('1', control_target[0])
                con_msg_dt = control_msg.create_con_msg()
                str_msg_final = json.dumps(create_send_msg(con_msg_dt, data_msg_dt))
                sock.sendall(str_msg_final.encode('utf-8'))
