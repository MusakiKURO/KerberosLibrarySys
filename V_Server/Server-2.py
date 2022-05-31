from library_db_management import *

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind(ADDR)
server_sock.listen(5)
while True:
    client_sock,addr = server_sock.accept()
    t = MyThread()