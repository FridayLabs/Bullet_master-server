import inject
from src.Middlewares.Middleware import Middleware
from src.Util import packet_is_a
from peewee import DoesNotExist
from protocol.Client.Authenticate_pb2 import Authenticate
from protocol.Success_pb2 import Success
from protocol.Failure_pb2 import Failure
from src.Models.User import User


class AuthentificationMiddleware(Middleware):
    __events = inject.attr('EventDispatcher')

    def process(self, packet):
        try:
            user = User.select().where(
                User.user_identifier == packet.UserId,
                User.password == User.get_password_hash(packet.UserPassword)
            ).get()
            self.__events.dispatch('ClientAuthenticated', user=user)
            self.transport.send_packet(Success())
            return True
        except DoesNotExist:
            self.transport.send_packet(Failure())
        return False
