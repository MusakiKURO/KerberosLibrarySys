# @Time    : 2022/5/11 11:26
# @Author  : Nisky
# @File    : demo_client.py
# @Software: PyCharm
import socket
import datetime
import json

# 创建socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 目的信息
server_ip = '127.0.0.1'
server_port = 7788

# 链接服务器
sock.connect((server_ip, server_port))

dict_user = \
    {"control_msg":
         {"control_src": 00, "control_type": 0, "control_target": 00000},
     "data_msg":
         {"name": "张三", "ID_tgs": "TGS", "TS_1": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
     }
str_user = json.dumps(dict_user)
if __name__ == "__main__":
    # 发送并接收数据
    try:
        # 发送数据
        send_data = str_user
        sock.send(send_data.encode('utf-8'))

        # 接收数据
        recv_data = sock.recv(1024)
        print("Message from server: %s" % recv_data.decode('utf-8'))
        sock.close()
    except socket.error as e:
        print("Socket error: %s" % str(e))
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        sock.close()
