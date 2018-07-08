from tests.functional.helpers import *
from src.Models.User import User
from tests.functional.FakeClient import FakeClient
from protocol.Server.Ping_pb2 import Ping
from protocol.Client.Pong_pb2 import Pong
from protocol.Client.Authenticate_pb2 import Authenticate
from protocol.Failure_pb2 import Failure


def test_authentication_required(migrations, server, client):
    assert server.get_clients_count() == 1

    client.send_packet(Pong(ServerTime=1, ClientTime=2))
    assert packet_is_a(Failure, client.receive_packet())


def test_sends_ping_packets(migrations, server, client):
    user = register_user('foo', 'foo')
    client.auth_with('foo', 'foo')
    time.sleep(1)
    assert packet_is_a(Ping, client.receive_packet())


def test_measure(caplog, migrations, server, client):
    user = register_user('foo', 'foo')
    client.auth_with('foo', 'foo')
    server_time = int(time.time())
    client.send_packet(Pong(ServerTime=1, ClientTime=2))
    time.sleep(1)
    assert User.get(User.user_identifier == 'foo').latency == 1

    client.send_packet(Pong(ServerTime=300, ClientTime=100))
    time.sleep(1)
    assert User.get(User.user_identifier == 'foo').latency == 200

    client_time = int(time.time())
    client.send_packet(Pong(ServerTime=server_time, ClientTime=client_time))
    time.sleep(1)
    assert User.get(User.user_identifier == 'foo').latency == client_time - server_time
