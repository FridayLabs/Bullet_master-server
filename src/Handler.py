import os
import time
import socket
import inject
import pdb
import threading
import src.Util as util
from src.Client import Client
from src.Transport import Transport
from src.Exceptions import SocketDisconnect
from protocol.Server.Ping_pb2 import Ping


class Handler(threading.Thread):
    alive = True
    router = inject.attr('Router')
    logger = inject.attr('Logger')

    def __init__(self, socket):
        super().__init__()
        self.transport = Transport(socket)
        self.client = self.__build_client(self.transport)
        threading.local().client = self.client

    def run(self):
        threading.Thread(name=self.name, target=self.__ping).start()
        while self.alive:
            try:
                packet = self.transport.recv_packet()
                if packet:
                    self.router.route(self.client, packet)
            except SocketDisconnect:
                self.stop()
            except Exception:
                self.logger.exception("Exception!", exc_info=True)

    def stop(self):
        self.logger.debug("Stopping client thread..")
        self.alive = False
        threading.local().client = None
        try:
            self.transport.close()
        except OSError:
            pass

    def __build_client(self, transport):
        return Client(transport)

    def __ping(self):
        def ping(self):
            try:
                self.logger.debug("Ping client")
                self.transport.send_packet(Ping(Time=int(time.time())))
            except SocketDisconnect:
                self.stop()
        util.periodically(lambda: ping(self), lambda: self.alive, int(os.getenv("CLIENT_CHECK_TIMEOUT", 5)))
