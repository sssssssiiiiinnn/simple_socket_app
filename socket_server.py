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
        logger.debug({
            'action': 'close_connection',
            'conn': conn,
            'addr': addr,
        })
        conn.close()
        self.clients.remove((conn, addr))
        logger.debug({
            'action': 'close_connection',
            'clients': self.clients
        })


    def handler(self, conn, addr):
        try:
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        self.close_connection(conn, addr)
                        break
                    else:
                        logger.debug({
                            'action': 'handler',
                            'data': data.decode('utf-8')
                        })
                        for client in self.clients:
                            client[0].sendall(data)
        except ConnectionResetError as ex:
            logger.debug({
                'action': 'handler',
                'error': ex
            })
            self.close_connection(conn, addr)


if __name__ == '__main__':
    socket_server = SocketServer()
    socket_server.server_up()
