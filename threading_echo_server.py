#!/usr/bin/env python3

"""
リクエスト処理をマルチスレッド化した実装例
リクエスト毎にスレッドを用いて複数のリクエストを並行処理する
"""

import socketserver
import socket
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s : %(threadName)s : %(module)s : %(funcName)s : %(message)s')

class EchoHandler(socketserver.BaseRequestHandler):

    def setup(self) -> None:
        logging.debug('Server accepted client - client=%s', self.client_address)

    def handle(self) -> None:
        client: socket.socket = self.request
        data = client.recv(1024).strip()
        logging.debug('Server received data from client - client=%s, data=%s', self.client_address, data)
        data = data.upper()
        client.sendall(data)
        logging.debug('Server sent data to client - client=%s, data=%s', self.client_address, data)

    def finish(self) -> None:
        logging.debug('Server disconnects client - client=%s', self.client_address)

if __name__ == '__main__':
    server_address = ('localhost', 8888)
    with socketserver.ThreadingTCPServer(server_address, EchoHandler) as server:
        server.serve_forever()
