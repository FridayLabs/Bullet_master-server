from src.Server import Server
from threading import Thread
from src.Models.User import User
import socket
import ssl
import os
import pdb
import time
import sys
from src.Util import import_procotol_class
from google.protobuf.any_pb2 import Any


def build_server():
    server = Server('0.0.0.0', 10000)
    server.initialize()

    thread = Thread(target=server.start)
    thread.daemon = True
    return (thread, server,)


def build_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    certfile = os.getcwd() + '/cert/cert.pem'
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certfile)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    conn = context.wrap_socket(sock, server_hostname='ip.krasnoperov.tk')
    conn.connect(('0.0.0.0', 10000))
    time.sleep(0.6)
    return conn


def build_server_and_client():
    t, server = build_server()
    t.start()
    client = build_client()
    assert server.get_clients_count() == 1
    return (server, client, t)


def register_user(id, password):
    return User.create(user_identifier=id, password=User.get_password_hash(password))


def receive_packet(socket):
    packet = socket.recv(1024).split(b'\0')[0]
    any = Any()
    any.ParseFromString(packet)
    cl = import_procotol_class(any.type_url.split("/")[1])
    unpacked_message = cl()
    any.Unpack(unpacked_message)
    return unpacked_message


def send_packet(socket, packet):
    any = Any()
    Any.Pack(any, packet)
    packet = any.SerializeToString()
    return socket.sendall(packet + b'\0')


def packet_is_a(cls, message):
    return message.DESCRIPTOR.name == cls.DESCRIPTOR.name
