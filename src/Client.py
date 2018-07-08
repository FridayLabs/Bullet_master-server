import inject
from protocol.Failure_pb2 import Failure
from protocol.Success_pb2 import Success
from protocol.Hello_pb2 import Hello
from src.Models.User import User


class Client:
    authenticated = False
    events = inject.attr('EventDispatcher')
    __user = None

    def __init__(self, transport):
        self.transport = transport
        self.events.add_listener('ClientAuthenticated', self.__set_user)

    def __set_user(self, args):
        self.__user = args['user']

    def get_user(self):
        return self.__user

    # def invite_to_party(self, user_id):
    #     target_in_party = self.party_manager.is_user_in_party(user_id)
    #     if target_in_party:
    #         return self.transport.send_packet(Failure(Message='User already in party'))

    #     self_in_party = self.party_manager.is_user_in_party(self.user.user_identifier)
    #     if self_in_party and not self.party_manager.is_party_leader(self.user.user_identifier):
    #         return self.transport.send_packet(Failure(Message='Current user is not party leader'))

    #     if not self_in_party and not target_in_party:
    #         party_id = self.party_manager.make_party(self.user.user_identifier, user_id)
    #         self.party_manager.set_party_leadership(party_id, self.user.user_identifier)
    #         return

    #     if self.is_in_party and self.is_party_lea:
    #         self.transport.send_packet(Failure(Message="Client version is not compatible"))
