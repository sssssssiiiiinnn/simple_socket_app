import hashlib
import logging
import threading
import socket


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s;%(message)s;')
logger = logging.getLogger(__name__)


class SocketServer(object):

    def __init__(self):
        logger.debug('Socket Server is initialized')
        self.host = '127.0.0.1'
        self.port = 50007
        self.clients = []

    def server_up(self):
        logger.debug('Socket Server is running')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        while True:
            try:
                logger.debug('Waiting for connection')
                conn, addr = sock.accept()
                logger.debug('Connection established with {}'.format(addr))
            except KeyboardInterrupt:
                break
            self.clients.append((conn, addr))
            print('Connection established from {}'.format(addr))
            thread = threading.Thread(target=self.handler, args=(conn, addr))
            thread.start()

    def close_connection(self, conn, addr):
        conn.close()
        self.clients.remove((conn, addr))

    def handler(self, conn, addr):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    self.close_connection(conn, addr)
                    break
                else:
                    print('data : {}'.format(data))
                    for client in self.clients:
                        try:
                            client[0].sendto(data, client[1])
                        except ConnectionResetError:
                            break


if __name__ == '__main__':
    socket_server = SocketServer()
    socket_server.server_up()
