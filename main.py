"""Copyright 2021 Eugeny Shlyagin (shlyagin@gmail.com)

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

import socket
import threading
from model import packets_bodies_process
import logging
import settings




class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):

        self.logger.debug(f'[+] New thread started: {address}')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((settings.remote_server, settings.remote_port))
        while True:
            try:
                BUFF_SIZE = 4096  # 4 KiB
                data = b''
                while True:
                    part = client.recv(BUFF_SIZE)
                    self.logger.debug(f'tracker ---> {part}')
                    data += part
                    if len(part) < BUFF_SIZE:
                        # either 0 or end of data
                        break

                if data:
                    data = packets_bodies_process(data.decode(), settings.can_name_parameters).encode()
                    self.logger.debug(f'<---- server {data}')
                    server_socket.send(data)
                else:
                    raise socket.error

                response = server_socket.recv(1024)
                if response:
                    client.send(response)
                    self.logger.debug(f'server ----> {response}')
                else:
                    raise socket.error

            except socket.error:
                client.close()
                server_socket.close()
                return False


if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(settings.log_file_name)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug('log started')

    logger.debug(f'Socket listen on port {settings.local_port}')
    ThreadedServer('', settings.local_port).listen()
