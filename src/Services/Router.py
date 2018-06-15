import inject
from protocol.Authenticate_pb2 import Authenticate


class Router:
    logger = inject.attr('Logger')

    def route(self, client, message):
        self.logger.debug("Routing message: <" + message.DESCRIPTOR.name + "> " + str(message))

        if self.__is_a(Authenticate, message):
            client.authenticate(message)

    def __is_a(self, cls, message):
        return message.DESCRIPTOR.name == cls.DESCRIPTOR.name
