import logging
import hashlib
import socket
import threading
import random


logging.basicConfig(level=logging.INFO, format='%(threadName)s;%(message)s;')
logger = logging.getLogger(__name__)


class SocketClient(object):

    def __init__(self):
        logger.debug('Socket Client is created')
        self.user_name = input('Your name?')

    def socket_client_up(self):
        logger.debug({
            'action': 'socket_client_up',
            'status': 'created'
        })
        print('Hello, {}'.format(self.user_name))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                logger.debug({
                    'action': 'sock_connect',
                    'status': 'created'
                })
                sock.connect(('127.0.0.1', 50007))
                logger.debug({
                    'action': 'sock_connect',
                    'status': 'connected'
                })
                thread_send = threading.Thread(target=self.send_message, args=(sock, ), daemon=True)
                thread_receive = threading.Thread(target=self.recieve_message, args=(sock, ), daemon=True)
                thread_send.start()
                thread_receive.start()
                thread_send.join()
                thread_receive.join()
            except ConnectionRefusedError:
                logger.error('Connection Refused')

    def send_message(self, sock):
        while True:
            try:
                logger.debug({
                    'action': 'send_message',
                    'status': 'wait'
                })
                comment = input()
                logger.debug({
                    'action': 'send_message',
                    'status': 'message created',
                    'message': comment
                })
                msg = self.user_name + ': ' + comment
            except KeyboardInterrupt:
                print('disconnect')
                sock.close()
                break
            try:
                if msg is not None:
                    sock.sendall(msg.encode('utf-8'))
            except ConnectionResetError:
                print('disconnect')
                sock.close()
                break

    def recieve_message(self, sock):
        while True:
            try:
                logger.debug({
                    'action': 'recieve_message',
                    'status': 'wait'
                })
                data = sock.recv(1024)
                print(data.decode('utf-8'))
            except ConnectionRefusedError:
                print('Connection refused')
                sock.close()
            except KeyboardInterrupt as ex:
                logger.info({
                    'action':'receive_message',
                    'status': 'error',
                    'error': ex
                })
                sock.close()


if __name__ == '__main__':
    socket_client = SocketClient()
    socket_client.socket_client_up()
