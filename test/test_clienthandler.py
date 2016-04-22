from unittest import TestCase

from app import initialize
from app.clienthandler import ClientHandler


class TestClientHandler(TestCase):
    def setUp(self):
        initialize()
        dispatcher = 'dispatcher'
        client_socket = 'client_socket'
        self.client_handler = ClientHandler(dispatcher=dispatcher,
                                            client_socket=client_socket)

    def test_simple(self):
        self.client_handler.run()
