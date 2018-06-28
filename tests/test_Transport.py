from mock import Mock
import socket
import pytest
from src.Transport import Transport
from src.Exceptions import SocketDisconnect
from google.protobuf.any_pb2 import Any
from tests.Mocket import Mocket


def build_packet():
    p = Any()
    p.type_url = 'typeurl'
    p.value = b'value'
    return p


def test_sending_packet():
    s = Mocket()
    t = Transport(s)
    t.send_packet(build_packet())

    s.set_throw_error(True)
    try:
        t.send_packet(build_packet())
    except SocketDisconnect:
        assert s.is_shutdown == True
        assert s.is_closed == True


def test_receive_packet():
    s = Mocket()
    t = Transport(s)
    p = build_packet()
    t.send_packet(p)
    assert t.recv_packet() == p

    t.send_packet(p)
    s.set_throw_error(True)
    try:
        assert t.recv_packet() == p
    except SocketDisconnect:
        assert s.is_shutdown == True
        assert s.is_closed == True


def test_close_closed():
    s = Mocket()
    t = Transport(s)
    assert t.closed == False
    assert s.is_closed == False
    try:
        t.close()
    except SocketDisconnect:
        assert t.closed == True
        assert s.is_closed == True
    t.close()
