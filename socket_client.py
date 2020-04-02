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
        print('Hello, {}'.format(self.user_name))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect(('127.0.0.1', 50007))
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
                comment = input()
                msg = self.user_name + ': ' + comment
            except KeyboardInterrupt:
                print('disconnect')
                break
            try:
                if msg is not None:
                    sock.send(msg.encode('utf-8'))
            except ConnectionResetError:
                break

    def recieve_message(self, sock):
        while True:
            try:
                logger.debug('waiting for message')
                data = sock.recv(1024)
                print(data.decode('utf-8'))
            except ConnectionRefusedError:
                print('Connection refused')


if __name__ == '__main__':
    socket_client = SocketClient()
    socket_client.socket_client_up()
