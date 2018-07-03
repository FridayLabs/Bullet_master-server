import inject
from tests.functional.helpers import *
from src.Models.User import User
from protocol.Hello_pb2 import Hello
from protocol.Failure_pb2 import Failure
from protocol.Success_pb2 import Success


def test_checks_version(migrations):
    register_user('foo', 'foo')
    os.environ['CLIENT_CHECK_TIMEOUT'] = '10'
    try:
        server, client, t = build_server_and_client()

        send_packet(client, Hello(Version='v0.0.1-client'))
        assert packet_is_a(Failure, receive_packet(client))
        time.sleep(0.5)
        assert server.get_clients_count() == 0

        client = build_client()
        send_packet(client, Hello(Version=inject.instance('Version')))
        time.sleep(0.1)
        p = receive_packet(client)
        assert packet_is_a(Hello, p)

    finally:
        server.shutdown()
        t.join()


def test_closes_socket_after_fail(migrations):
    os.environ['CLIENT_CHECK_TIMEOUT'] = '10'
    try:
        server, client, t = build_server_and_client()
        send_packet(client, Hello(Version='v0.0.1-client'))
        assert packet_is_a(Failure, receive_packet(client))

        send_packet(client, Hello(Version='v0.0.1-client'))
        time.sleep(0.5)
        assert server.get_clients_count() == 0

    finally:
        server.shutdown()
        t.join()
