# coding=utf-8
# @Time    : 2022/5/11 11:28
# @Author  : Nisky
# @File    : demo_server.py
# @Software: PyCharm
import json
import socket
import threading
import sys
from DES.demo_DES import *
from RSA.demo_RSA import *
from werkzeug.security import generate_password_hash, check_password_hash

test_key = '0kLllffV'
C_n = 3951270249045146953972943163348434942592764989560360906533269897277080404934010181112385167732070275357806027491762234996305583674911212807857840660608406910051955297329683233106234207322044758397760274898933802535462100186118312888112180532109135970587764285970799040141296520625252128054797411575140828014980501308928204513652682136220524500675713399801045198810206992806199335791852827154930372510398253049468928422550127057850688190116699758746503012249254107915609637655541305024737077987890330855253602741330884459042041448515721767143012038195427206379154406467638677589417430783480145088864002792702243711871
C_e = 65537


def Creat_thread(sock, addr):
    print('Accept new connection from %s:%s' % addr)

    try:
        while True:
            # # 将收到的数据拼接起来
            total_data = bytes()
            while True:
                data = sock.recv(8192)
                if len(data) < 8192:
                    key_values = data.decode('utf-8')
                    if key_values == '@':
                        break
                    else:
                        total_data += data
                else:
                    total_data += data
            print(len(total_data))
            print(total_data.decode('utf-8'))
            if total_data:
                print("Message from %s:\n%s" % (addr[0], total_data.decode('utf-8')))

                # text_json_loads = json.loads(total_data.decode('utf-8'))
                # text_josn_dumps = json.dumps(
                #     {'control_msg': {'control_src': text_json_loads['control_msg']['control_src'],
                #                      'control_result': text_json_loads['control_msg']['control_result'],
                #                      'control_target': text_json_loads['control_msg']['control_target']},
                #      'data_msg': {'ID_c': text_json_loads['data_msg']['ID_c'],
                #                   'ID_tgs': text_json_loads['data_msg']['ID_tgs'],
                #                   'TS_1': text_json_loads['data_msg']['TS_1']}})
                # hash_check = check_password_hash(RSA_call(text_json_loads['HMAC'],))
                # print(text_josn_dumps)
                # sock.sendall("I have received".encode('utf-8'))
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        sock.close()


if __name__ == "__main__":
    # 创建TCP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 取消主动断开连接四次握手后的TIME_WAIT状态
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定地址和端口号
    srv_addr = ('', 7788)
    sock.bind(srv_addr)

    # 侦听客户端
    sock.listen(5)
    print('Waiting for connection...')
    while True:
        # 接受客户端连接
        conn, addr = sock.accept()
        t = threading.Thread(target=Creat_thread, args=(conn, addr))
        t.start()
