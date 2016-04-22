import logging
from threading import Thread


class ClientHandler(Thread):
    def __init__(self, dispatcher, client_socket):
        super(ClientHandler, self).__init__()
        self.dispatcher = dispatcher
        self.client_socket = client_socket
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        self.logger.info(msg="New connection created with: " + self.client_socket)
        self.handle_connection()
        self.logger.info(msg="Connection closed with: " + self.client_socket)

    def handle_connection(self):
        pass
