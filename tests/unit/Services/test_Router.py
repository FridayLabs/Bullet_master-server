from src.Services.Router import Router
from google.protobuf.any_pb2 import Any


def build_packet():
    p = Any()
    p.type_url = 'typeurl'
    p.value = b'value'
    return p


def test_routes_packages():
    r = Router()
    p = build_packet()
    client = 'client socket'

    def handler(x, y):
        assert x == client and y == p
    r.routes[Any] = handler
    r.route(client, p)
