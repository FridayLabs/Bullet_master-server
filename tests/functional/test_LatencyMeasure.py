from tests.functional.helpers import *
from src.Models.User import User
from protocol.Client.Pong_pb2 import Pong
from protocol.Client.Authenticate_pb2 import Authenticate
from protocol.Failure_pb2 import Failure


def test_authentication_required(migrations):
    os.environ['CLIENT_CHECK_TIMEOUT'] = '10000'
    try:
        t, server = build_server()
        t.start()
        client = build_client()
        assert server.get_clients_count() == 1

        send_packet(client, Pong(ServerTime=1, ClientTime=2))
        p = receive_packet(client)
        assert packet_is_a(Failure, p)
    finally:
        server.shutdown()
        t.join()


def test_measure(migrations):
    user = register_user('foo', 'foo')
    os.environ['CLIENT_CHECK_TIMEOUT'] = '10000'
    try:
        t, server = build_server()
        t.start()
        client = build_client()
        assert server.get_clients_count() == 1

        server_time = int(time.time())

        send_packet(client, Authenticate(UserId='foo', UserPassword='foo'))
        send_packet(client, Pong(ServerTime=1, ClientTime=2))
        time.sleep(0.1)
        assert User.get(User.user_identifier == 'foo').latency == 1

        send_packet(client, Pong(ServerTime=300, ClientTime=100))
        time.sleep(0.1)
        assert User.get(User.user_identifier == 'foo').latency == 200

        client_time = int(time.time())
        send_packet(client, Pong(ServerTime=server_time, ClientTime=client_time))
        time.sleep(0.1)
        assert User.get(User.user_identifier == 'foo').latency == client_time - server_time
    finally:
        server.shutdown()
        t.join()
