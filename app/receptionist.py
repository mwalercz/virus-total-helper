import logging
import socket

from app.clienthandler import ClientHandler




class Receptionist:
    def __init__(self, dispatcher, port=5005, connection_no=5):
        self.dispatcher = dispatcher
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(connection_no)

    def accept_loop(self):
        while True:
            (client_socket, address) = self.server_socket.accept()
            client_handler = ClientHandler(dispatcher=self.dispatcher,
                                           client_socket=client_socket)
            client_handler.run()
