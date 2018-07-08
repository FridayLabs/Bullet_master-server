import inject
import time
from tests.functional.FakeClient import FakeClient
from tests.functional.helpers import packet_is_a, register_user
from src.Models.User import User
from protocol.Hello_pb2 import Hello
from protocol.Failure_pb2 import Failure
from protocol.Success_pb2 import Success


def test_checks_version(migrations, server, client):
    client.send_packet(Hello(Version='v0.0.1-client'))
    assert packet_is_a(Failure, client.receive_packet())
    time.sleep(1)
    assert server.get_clients_count() == 0

    client = FakeClient()
    client.send_packet(Hello(Version=inject.instance('Version')))
    time.sleep(0.1)
    assert packet_is_a(Hello, client.receive_packet())
    client.close()


# def test_auth_with_user(migrations, server, client):
    # register_user('foo', 'foo')
    # client.auth_with('foo', 'bar')


def test_closes_socket_after_fail(migrations, server, client):
    client.send_packet(Hello(Version='v0.0.1-client'))
    assert packet_is_a(Failure, client.receive_packet())

    client.send_packet(Hello(Version='v0.0.1-client'))
    time.sleep(1)
    assert server.get_clients_count() == 0

    client = FakeClient()
    client.send_packet(Hello(Version=inject.instance('Version')))
    time.sleep(0.1)
    assert packet_is_a(Hello, client.receive_packet())
    client.close()
