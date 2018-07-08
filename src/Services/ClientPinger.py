import os
import time
import inject
import src.Util as util
from threading import Thread
from src.Exceptions import SocketDisconnect
from protocol.Server.Ping_pb2 import Ping


class ClientPinger:
    __events = inject.attr('EventDispatcher')
    __logger = inject.attr('Logger')

    __alive = False

    def __init__(self, transport):
        self.__transport = transport
        self.__events.add_listener('ClientVerified', self.__start)

    def __start(self, args):
        self.__alive = True
        self.__thread = Thread(target=self.__ping, name='Client Pinger')
        self.__thread.start()

    def __stop(self, args):
        self.__alive = False
        self.__thread.join()
        self.__thread = None

    def __ping(self):
        def ping(self):
            try:
                self.__logger.debug("Ping client")
                self.__transport.send_packet(Ping(Time=int(time.time())))
            except SocketDisconnect:
                self.stop()
        util.periodically(lambda: ping(self), lambda: self.__alive, int(os.getenv("CLIENT_CHECK_TIMEOUT", 5)))
