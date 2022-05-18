# @Time    : 2022/5/11 11:26
# @Author  : Nisky
# @File    : demo_client.py
# @Software: PyCharm
import socket
import argparse

# 创建socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 目的信息
server_ip = '192.168.43.229'
server_port = 7788

# 链接服务器
sock.connect((server_ip, server_port))

if __name__ == "__main__":
    # 发送并接收数据
    try:
        while True:
            # 发送数据
            send_data = input("请输入要发送的数据：")
            sock.send(send_data.encode('gbk'))
            if send_data == "quit" or send_data == "exit":
                break
            # 接收数据
            recv_data = sock.recv(1024)
            print("Message from server: %s" % recv_data.decode('gbk'))
        sock.close()
    except socket.error as e:
        print("Socket error: %s" % str(e))
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        sock.close()
