from tests.functional.FakeClient import FakeClient
from tests.functional.helpers import *
from protocol.Client.InviteToParty_pb2 import InviteToParty
from protocol.Client.Accept_pb2 import Accept
from protocol.Server.PartyInvitation_pb2 import PartyInvitation
from protocol.Server.UserJoinsParty_pb2 import UserJoinsParty


# def test_user_invite_to_party(migrations, server):
#     user1 = register_user('foo', 'foo')
#     user2 = register_user('lol', 'bar')
#     os.environ['CLIENT_CHECK_TIMEOUT'] = '1000'

#     try:
#         client1 = FakeClient()
#         client2 = FakeClient()
#         client1.auth_with('foo', 'foo')
#         client2.auth_with('lol', 'bar')

#         client1.send_packet(InviteToParty(UserId='lol'))
#         invite = client2.receive_packet()
#         assert packet_is_a(PartyInvitation, invite)
#         assert 'foo' in invite.userId
#         client2.send_packet(Accept())
#         assert packet_is_a(UserJoinsParty, client1.receive_packet())
#         assert packet_is_a(UserJoinsParty, client2.receive_packet())
#     finally:
#         client1.stop_parallel_receiver()
#         client2.stop_parallel_receiver()
