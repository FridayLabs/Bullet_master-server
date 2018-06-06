import os
import time
import logging
import socket
from threading import Thread
import src.events as events
from src.protocol.ping_pb2 import Ping


class Handler(Thread):
    chunk_size = 1024
    alive = True

    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        logging.debug("Connected!")
        Thread(name=self.name, target=self.__ping).start()
        while self.alive:
            try:
                data = self.__recv_all()
                if data:
                    logging.debug("Received: " + str(data))
                    response = self.__handle_message(data)
                    if response:
                        self.__send(response)
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
        while self.alive:
            logging.debug("Ping client")
            ping = Ping()
            ping.ServerVersion = "0"
            ping.ServerTime = int(time.time())
            self.__send(ping.SerializeToString())
            time.sleep(int(os.getenv("CLIENT_CHECK_TIMEOUT") or 5))

    def __send(self, data):
        try:
            self.socket.sendall(data)
        except socket.error:
            logging.debug("Disconnected!")
            self.stop()

    def __recv_all(self):
        data = b''
        while self.alive:
            part = self.socket.recv(self.chunk_size)
            data += part
            if len(part) < self.chunk_size:
                break
        return data

    def __handle_message(self, data):
        return data
