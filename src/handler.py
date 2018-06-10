import os
import time
import logging
import socket
import struct
from threading import Thread
import src.events as events
import src.util as util
from protocol.ping_pb2 import Ping
from google.protobuf.any_pb2 import Any
from src.router import Router


class Handler(Thread):
    chunk_size = 1024
    alive = True
    null_enumerator = b'\0'
    buffer = b''

    def __init__(self, socket):
        super().__init__()
        self.socket = socket
        self.router = Router()

    def run(self):
        logging.debug("Connected!")
        Thread(name=self.name, target=self.__ping).start()
        while self.alive:
            try:
                data = self.__recv_packet()
                if data:
                    logging.debug("Received: " + str(data))
                    response = self.__handle_message(data)
                    if response:
                        self.__send_packet(response)
            except socket.error:
                logging.debug("Disconnected!")
                self.stop()
            except Exception:
                logging.exception("Exception!", exc_info=True)

    def stop(self):
        logging.debug("Stopping client thread..")
        self.alive = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.join()
        except OSError:
            pass

    def __ping(self):
        def ping(self):
            logging.debug("Ping client")
            ping = Ping()
            ping.ServerVersion = "0"
            ping.ServerTime = int(time.time())
            self.__send_packet(ping)
        util.periodically(lambda: ping(self), lambda: self.alive, int(os.getenv("CLIENT_CHECK_TIMEOUT") or 5))

    def __send_packet(self, packet):
        any = Any()
        Any.Pack(any, packet)
        return self.__send(any.SerializeToString())

    def __send(self, data):
        try:
            self.socket.sendall(data + self.null_enumerator)
        except socket.error:
            logging.debug("Disconnected!")
            self.stop()

    def __recv_packet(self):
        while self.alive:
            if self.null_enumerator in self.buffer:
                packets = self.buffer.split(self.null_enumerator)
                self.buffer = self.null_enumerator.join(packets[1:])
                return packets[0]
            else:
                self.buffer += self.socket.recv(self.chunk_size)

    def __handle_message(self, packet):
        any = Any()
        any.ParseFromString(packet)
        cl = util.import_procotol_class(any.type_url.split("/")[1])
        unpacked_message = cl()
        any.Unpack(unpacked_message)
        return unpacked_message
