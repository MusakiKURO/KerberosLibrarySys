# @Time    : 2022/5/11 11:28
# @Author  : Nisky
# @File    : demo_server.py
# @Software: PyCharm
import socket
import threading
import sys


def Creat_thread(sock, addr):
    print('Accept new connection from %s:%s' % addr)
    try:
        while True:
            data = sock.recv(1024)
            if data == "quit" or data == "exit":
                print("Client %s exit." % addr[0])
                break
            if data:
                print("Message from %s: %s" % (addr[0], data.decode('gbk')))

                sock.send("I have received".encode('gbk'))
        sock.close()
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        sock.close()


if __name__ == "__main__":
    # 创建TCP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
