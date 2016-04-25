import logging
from _socket import SHUT_RDWR
from threading import Thread

from app.http import HTTPRequest


class ClientHandler(Thread):
    def __init__(self, dispatcher, client_socket):
        super(ClientHandler, self).__init__(name='ClientHandler')
        self.dispatcher = dispatcher
        self.client_socket = client_socket
        self.client_socket.settimeout(5)

    def run(self):
        logging.info(msg="New connection created with: " + str(self.client_socket))
        self._handle_connection()
        logging.info(msg="Connection closed with: " + str(self.client_socket))

    def _handle_connection(self):
        with self.client_socket:
            raw_data = self._read_from_socket()
            request = HTTPRequest(raw_data)
            response = self.dispatcher.dispatch(request)
            self._write_to_socket(response)
            self._shutdown_socket()

    def _read_from_socket(self):
        data_array = []
        while True:
            data = self.client_socket.recv(4096)
            if self._is_finished(data):
                logging.debug(msg="received all data")
                data_array.append(data)
                break
            else:
                data_array.append(data)
        binary_data = b''.join(data_array)
        return binary_data.decode(encoding='utf-8')

    def _is_finished(self, data):
        if data:
            length = len(data)
            last_chars = data[length - 4:length]
            return last_chars == b'\r\n\r\n'
        else:
            return False

    def _write_to_socket(self, response):
        binary_response = str(response).encode('utf-8')
        self.client_socket.sendall(binary_response)

    def _shutdown_socket(self):
        self.client_socket.shutdown(SHUT_RDWR)
