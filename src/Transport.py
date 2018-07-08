import socket
import inject
import threading
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
        self.__thread = threading.Thread(target=self.__send_noop)
        self.__thread.start()

    def send_packet(self, packet):
        any = Any()
        Any.Pack(any, packet)
        self.logger.debug('Sending packet ' + str(any))
        return self.__send(any.SerializeToString())

    def recv_packet(self):
        if self.closed:
            raise SocketDisconnect()
        while not self.closed:
            try:
                if self.null_enumerator in self.buffer:
                    packets = [p for p in self.buffer.split(self.null_enumerator) if p != b'']
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

    def __send_noop(self):
        util.periodically(lambda: self.__send(b''), lambda: not self.closed, 0.1)

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
            self.__thread.join()
            self.__thread = None
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        finally:
            self.logger.debug("Disconnected!")
            raise SocketDisconnect()
