# coding=utf-8
from library_db_management import *
import threading

def _main():
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind(ADDR)
    server_sock.listen(5)
    print('waiting for connection...')
    while True:
        client_sock, addr = server_sock.accept()
        print('connected from',addr)
        t = threading.Thread(target = total_process(client_sock))
        t.start()


if __name__ == '__main__':
    _main()
