import logging
import socket
from threading import Thread

from server.clienthandler import ClientHandler


class Receptionist(Thread):
    def __init__(self, dispatcher, hostname='localhost', port=5005, connection_no=5):
        super(Receptionist, self).__init__(name="Receptionist")
        # dispatcher jest potrzebny tylko zeby podać go dalej do wątków ClientHandler (jest thread-safe),
        # mozna by zrobic z niego singletona
        self.dispatcher = dispatcher
        self.hostname = hostname
        self.port = port
        self.connection_no = connection_no
        self.running = True
        self.server_socket = self._configure_and_get_socket()

    def _configure_and_get_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.hostname, self.port))
        server_socket.listen(self.connection_no)
        return server_socket

    def run(self):
        logging.info('Server running on: ' + str(self.hostname) + ":" + str(self.port))
        self._accept_loop()
        logging.info("Server finished running")

    def _accept_loop(self):
        with self.server_socket:
            while self.running:
                (client_socket, address) = self.server_socket.accept()
                client_handler = ClientHandler(dispatcher=self.dispatcher,
                                               client_socket=client_socket)
                client_handler.setDaemon(True)
                client_handler.start()

    # dziwne rozwiazanie ale dziala, laczymy sie z wlasnym socketem (robi to główny wątek) zeby odblokowac accept()
    # należaloby zrobić sekcję krytyczną na ustawianie flagi running i na sprawdzanie tej flagi
    # ale to bardzo malo prawdopodobna sytuacja :)
    def stop(self):
        self.running = False
        socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM).connect((self.hostname, self.port))
