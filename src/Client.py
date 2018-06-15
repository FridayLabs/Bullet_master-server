import inject
from protocol.Exceptions.Unauthnticated_pb2 import Unauthenticated


class Client:
    authenticated = False
    user_id = None
    logger = inject.attr('Logger')

    def __init__(self, transport):
        self.transport = transport

    def authenticate(self, message):
        if message.UserID == 'admin' and message.UserPassword == 'admin':
            self.authenticated = True
            self.user_id = message.UserID
            # TODO send user data
        else:
            self.transport.send_packet(Unauthenticated())