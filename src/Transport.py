import socket
import inject
import src.Util as util
from src.Exceptions import SocketDisconnect
from google.protobuf.any_pb2 import Any


class Transport:
    closed = False
    null_enumerator = b'\0'
    buffer = b''
    chunk_size = 1024
    logger = inject.attr('Logger')

    def __init__(self, socket):
        self.socket = socket
        self.logger.debug("Connected!")

    def send_packet(self, packet):
        any = Any()
        Any.Pack(any, packet)
        return self.__send(any.SerializeToString())

    def recv_packet(self):
        if self.closed:
            raise SocketDisconnect()
        while not self.closed:
            try:
                if self.null_enumerator in self.buffer:
                    packets = self.buffer.split(self.null_enumerator)
                    self.buffer = self.null_enumerator.join(packets[1:])
                    packet = packets[0]
                    self.logger.debug("Received packet: " + str(packet))
                    return self.__parse_packet(packet)
                else:
                    recv = self.socket.recv(self.chunk_size)
                    if recv == "":
                        self.close()
                    self.buffer += recv
            except:
                self.close()

    def __send(self, data):
        try:
            self.socket.sendall(data + self.null_enumerator)
        except:
            self.close()

    def __parse_packet(self, packet):
        any = Any()
        any.ParseFromString(packet)
        cl = util.import_procotol_class(any.type_url.split("/")[1])
        unpacked_message = cl()
        any.Unpack(unpacked_message)
        return unpacked_message

    def close(self):
        if self.closed:
            return
        self.closed = True
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        finally:
            self.logger.debug("Disconnected!")
            raise SocketDisconnect()
