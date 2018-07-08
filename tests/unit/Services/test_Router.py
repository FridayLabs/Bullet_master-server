import pytest
from src.Exceptions import SocketDisconnect
from src.Services.Router import Router
from src.Transport import Transport
from tests.unit.Mocket import Mocket
from google.protobuf.any_pb2 import Any
from protocol.Hello_pb2 import Hello
from protocol.Success_pb2 import Success
from protocol.Failure_pb2 import Failure


def packet_is_a(cls, message):
    return message.DESCRIPTOR.name == cls.DESCRIPTOR.name


class PassMiddleware:
    def process(self, packet):
        return True


class RejectMiddleware:
    def process(self, packet):
        return False


class FakeProcessor:
    def process(self, msg):
        pass


def test_packets_should_flow_middlewares():
    t = Transport(Mocket())
    r = Router(t)
    r.set_middlewares({
        PassMiddleware(): [Success],
        RejectMiddleware(): [Failure]
    })
    r.set_routes({Hello: FakeProcessor()})
    with pytest.raises(SocketDisconnect):
        r.route(Hello())
    with pytest.raises(SocketDisconnect):
        r.route(Failure())
        assert packet_is_a(Failure, t.recv_packet())
    r.route(Success())
    r.route(Failure())
    r.route(Hello())
    t.close()


def test_routes_packages():
    t = Transport(Mocket())
    r = Router(t)
    called = False

    class Processor:
        def process(self, msg):
            nonlocal called
            called = True
    r.set_middlewares({})
    r.set_routes({Hello: Processor()})
    r.route(Hello(Version='kek'))
    assert called
    with pytest.raises(SocketDisconnect):
        t.close()
