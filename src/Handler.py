import os
import time
import socket
import inject
import pdb
import threading
import src.Util as util
from src.Services.Router import Router
from src.Services.ClientPinger import ClientPinger
from src.Transport import Transport
from src.Exceptions import SocketDisconnect
from protocol.Server.Ping_pb2 import Ping


class Handler(threading.Thread):
    alive = True
    __logger = inject.attr('Logger')
    __ctxt = inject.attr('Context')

    def __init__(self, socket):
        super().__init__()
        self.__transport = Transport(socket)

    def run(self):
        self.__ctxt.set('Transport', self.__transport)
        self.__router = Router(self.__transport)
        self.__client_pinger = ClientPinger(self.__transport)
        while self.alive:
            try:
                packet = self.__transport.recv_packet()
                if packet:
                    self.__router.route(packet)
            except SocketDisconnect:
                self.stop()
            except Exception:
                self.__logger.exception("Exception!", exc_info=True)

    def stop(self):
        self.__logger.debug("Stopping client thread..")
        self.alive = False
        try:
            self.__transport.close()
        except OSError:
            pass
