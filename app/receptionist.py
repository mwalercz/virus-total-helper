import logging
import socket
from _socket import SHUT_RDWR
from threading import Thread

from app.clienthandler import ClientHandler


class Receptionist(Thread):
    def __init__(self, dispatcher, port=5005, connection_no=5):
        super(Receptionist, self).__init__(name="Receptionist")
        # dispatcher jest potrzebny tylko zeby podać go dalej do wątków ClientHandler (jest thread-safe),
        # mozna by zrobic z niego singletona
        self.dispatcher = dispatcher
        self.hostname = 'localhost'
        self.port = port
        self.connection_no = connection_no
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        self.configure_socket()

    def configure_socket(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.hostname, self.port))
        self.server_socket.listen(self.connection_no)

    def run(self):
        logging.info('Server started running on port: ' + str(self.port))
        self.accept_loop()
        logging.info("Receptionist finished gracefully")

    def accept_loop(self):
        while True:
            if self.running:
                (client_socket, address) = self.server_socket.accept()
                client_handler = ClientHandler(dispatcher=self.dispatcher,
                                               client_socket=client_socket)
                client_handler.setDaemon(True)
                client_handler.start()
            else:
                self.server_socket.shutdown(SHUT_RDWR)
                self.server_socket.close()
                break

    # dziwne rozwiazanie ale dziala, laczymy sie z wlasnym socketem zeby odblokowac accept()
    # należaloby zrobić sekcję krytyczną na ustawianie flagi running i na sprawdzanie tej flagi
    # ale to bardzo malo prawdopodobna sytuacja :)
    def stop(self):
        self.running = False
        socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM).connect((self.hostname, self.port))
