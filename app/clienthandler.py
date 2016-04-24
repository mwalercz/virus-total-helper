import logging
from _socket import SHUT_RDWR
from threading import Thread

from app.httprequest import HTTPRequest


class ClientHandler(Thread):
    def __init__(self, dispatcher, client_socket):
        super(ClientHandler, self).__init__(name='ClientHandler')
        self.dispatcher = dispatcher
        self.client_socket = client_socket
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        self.logger.info(msg="New connection created with: " + str(self.client_socket))
        self._handle_connection()
        self.logger.info(msg="Connection closed with: " + str(self.client_socket))

    def _handle_connection(self):
        try:
            raw_data = self._read_from_socket()
            request = HTTPRequest(raw_data)
            response = self.dispatcher.dispatch(request)
            self._write_to_socket(response)
        finally:
            self._close_connection()

    def _read_from_socket(self):
        data_array = []
        while True:
            data = self.client_socket.recv(4096)
            if self._is_finished(data):
                self.logger.debug(msg="received all data")
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
        binary_response = response.encode('utf-8')
        self.client_socket.sendall(binary_response)

    def _close_connection(self):
        self.client_socket.shutdown(SHUT_RDWR)
        self.client_socket.close()
