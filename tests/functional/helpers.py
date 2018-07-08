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


def register_user(id, password):
    return User.create(user_identifier=id, password=User.get_password_hash(password))


def receive_packet(socket):
    packet = socket.recv(1024).split(b'\0')[0]
    if packet:
        any = Any()
        any.ParseFromString(packet)
        cl = import_procotol_class(any.type_url.split("/")[1])
        unpacked_message = cl()
        any.Unpack(unpacked_message)
        return unpacked_message
    raise Exception('Packet is empty')


def send_packet(socket, packet):
    any = Any()
    Any.Pack(any, packet)
    packet = any.SerializeToString()
    return socket.sendall(packet + b'\0')


def packet_is_a(cls, message):
    return message.DESCRIPTOR.name == cls.DESCRIPTOR.name
