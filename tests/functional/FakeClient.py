import socket
import ssl
import os
import time
import inject
from src.Util import import_procotol_class
from google.protobuf.any_pb2 import Any
import threading
import random
from tests.functional.helpers import packet_is_a
from protocol.Hello_pb2 import Hello
from protocol.Failure_pb2 import Failure
from protocol.Success_pb2 import Success
from protocol.Client.Authenticate_pb2 import Authenticate
from protocol.Server.Ping_pb2 import Ping
from protocol.Client.Pong_pb2 import Pong


class FakeClient:
    handlers = {
        Ping: lambda client, message: client.send_packet(
            Pong(ServerTime=message.Time, ClientTime=int(time.time()) + random.randint(1, 300))
        )
    }

    receiver_thread = None
    handle_incoming_packets = False

    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        certfile = os.getcwd() + '/cert/cert.pem'
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certfile)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        conn = context.wrap_socket(sock, server_hostname='ip.krasnoperov.tk')
        conn.connect(('0.0.0.0', 10000))
        time.sleep(0.6)
        return conn

    def close(self):
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
        except:
            pass

    def start_parallel_receiver(self):
        self.receiver_thread = threading.Thread(target=self.receiver)
        self.handle_incoming_packets = True
        self.receiver_thread.start()

    def stop_parallel_receiver(self):
        self.handle_incoming_packets = False
        if self.receiver_thread is not None:
            self.receiver_thread.join()
            self.receiver_thread = None

    def receiver(self):
        while self.handle_incoming_packets:
            p = self.receive_packet()
            for route, handler in self.handlers.items():
                if packet_is_a(route, p):
                    handler(self, p)

    def register_handler(self, cls, fn):
        self.handlers[cls] = fn

    def send_packet(self, packet):
        any = Any()
        Any.Pack(any, packet)
        packet = any.SerializeToString()
        return self.conn.sendall(packet + b'\0')

    def receive_packet(self):
        packet = None
        while not packet:
            buffer = self.conn.recv(1024)
            packet = [p for p in buffer.split(b'\0') if p != b'']
            if len(packet) > 0:
                packet = packet[0]
        any = Any()
        any.ParseFromString(packet)
        cl = import_procotol_class(any.type_url.split("/")[1])
        unpacked_message = cl()
        any.Unpack(unpacked_message)

        return unpacked_message

    def auth_with(self, login, password):
        self.send_packet(Hello(Version=inject.instance('Version')))
        time.sleep(0.1)
        assert packet_is_a(Hello, self.receive_packet())
        self.send_packet(Authenticate(UserId=login, UserPassword=password))
        time.sleep(0.1)
        p = self.receive_packet()
        assert packet_is_a(Success, p)
