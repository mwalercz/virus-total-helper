import logging
from _socket import SHUT_RDWR
from threading import Thread

from app.http import HTTPRequest


class SomethingWentWrong(Exception):
    pass


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
            request = self._get_request()
            response = self.dispatcher.dispatch(request)
            self._write_to_socket(response)

    def _get_request(self):
        data_array = []
        request = None
        while True:
            raw_data = self._read_from_socket(data_array)
            request = HTTPRequest(raw_data)
            if request.is_finished():
                logging.debug(msg="received all data")
                break
        if request is None:
            raise SomethingWentWrong
        return request

    def _read_from_socket(self, data_array):
        data = self.client_socket.recv(4096)
        data_array.append(data)
        binary_data = b''.join(data_array)
        return binary_data.decode(encoding='utf-8')

    def _write_to_socket(self, response):
        binary_response = str(response).encode('utf-8')
        self.client_socket.sendall(binary_response)

    def _shutdown_socket(self):
        self.client_socket.shutdown(SHUT_RDWR)
