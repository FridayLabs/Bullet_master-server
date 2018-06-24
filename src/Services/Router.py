import inject
from protocol.Authenticate_pb2 import Authenticate


class Router:
    logger = inject.attr('Logger')

    routes = {
        Authenticate: lambda client, message: client.authenticate(message),
    }

    def route(self, client, message):
        self.logger.debug("Routing message: <" + message.DESCRIPTOR.name + "> " + str(message))

        for route, handler in self.routes.items():
            if self.__is_a(route, message):
                handler(client, message)

    def __is_a(self, cls, message):
        return message.DESCRIPTOR.name == cls.DESCRIPTOR.name
