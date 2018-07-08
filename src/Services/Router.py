import inject
import threading
from src.Client import Client
from protocol.Client.Authenticate_pb2 import Authenticate
from protocol.Client.Pong_pb2 import Pong
from protocol.Hello_pb2 import Hello
from protocol.Failure_pb2 import Failure
from protocol.Client.InviteToParty_pb2 import InviteToParty
from src.Middlewares.AuthentificationMiddleware import AuthentificationMiddleware
from src.Middlewares.HandshakeMiddleware import HandshakeMiddleware
from src.PacketProcessors.LatencyProcessor import LatencyProcessor


class Router:
    __logger = inject.attr('Logger')
    __ctxt = inject.attr('Context')
    __events = inject.attr('EventDispatcher')

    def __init__(self, transport):
        self.__client = Client(transport)
        self.__ctxt.set('Client', self.__client)
        self.__transport = transport
        self.__middlewares = {
            HandshakeMiddleware(self.__transport): [Hello],
            AuthentificationMiddleware(self.__transport): [Authenticate],
        }
        self.__routes = {
            Pong: LatencyProcessor(),
            # InviteToParty: lambda c, m: c.invite_to_party(m.UserId)
        }

    def route(self, message):
        self.__logger.debug("Routing message: " + self.__print_message(message))
        for middleware, accepts in self.__middlewares.items():
            accepts_matches = False
            for accept in accepts:
                if self.__is_a(accept, message):
                    accepts_matches = True
            if not accepts_matches:
                return self.__drop_client()
            if not middleware.process(message):
                return self.__drop_client()
            else:
                del self.__middlewares[middleware]
                if len(self.__middlewares.items()) == 0:
                    self.__events.dispatch('ClientVerified')
                return

        for route, processor in self.__routes.items():
            if self.__is_a(route, message):
                processor.process(message)

    def set_middlewares(self, middlewares):
        self.__middlewares = middlewares

    def set_routes(self, routes):
        self.__routes = routes

    def __drop_client(self):
        self.__logger.error("Invalid state. Dropping client")
        self.__transport.send_packet(Failure(Message="Verification failed"))
        self.__transport.close()

    def __is_a(self, cls, message):
        return message.DESCRIPTOR.name == cls.DESCRIPTOR.name

    def __print_message(self, message):
        return "<" + message.DESCRIPTOR.name + "> " + str(message)
