from library_db_management import *
from socketserver import BaseRequestHandler,ThreadingTCPServer


class Handler(BaseRequestHandler):
    def handle(self):
        addr,pid = self.client_address
        sock = self.request
        print("%s connectec!"% addr)
        total_process(sock)


if __name__ == '__main__':
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
    print(server)