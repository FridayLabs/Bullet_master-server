import inject
from protocol.Client.Authenticate_pb2 import Authenticate
from protocol.Client.Pong_pb2 import Pong
from protocol.Hello_pb2 import Hello


class Router:
    logger = inject.attr('Logger')

    routes = {
        Authenticate: lambda client, message: client.authenticate(message),
        Pong: lambda client, message: client.set_latency(abs(message.ServerTime - message.ClientTime)),
        Hello: lambda client, message: client.check_version(message.Version)
    }

    def route(self, client, message):
        self.logger.debug("Routing message: <" + message.DESCRIPTOR.name + "> " + str(message))

        for route, handler in self.routes.items():
            if self.__is_a(route, message):
                handler(client, message)

    def __is_a(self, cls, message):
        return message.DESCRIPTOR.name == cls.DESCRIPTOR.name
