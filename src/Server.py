import os
import ssl
import time
import inject
import socket
import src.Util as util
from threading import Thread
from src.Handler import Handler
from src.Services.Configurator import Configurator


class Server:
    __host = '0.0.0.0'
    __port = 9999
    __socket = None
    __handlers = []
    __threads = []
    __alive = True
    __logger = inject.attr('Logger')

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def initialize(self):
        configurator = Configurator()
        configurator.configure_everything()
        self.__context = self.__build_socket_context()
        self.__socket = self.__build_socket(self.__host, self.__port, self.__context)

    def start(self):
        self.__listen()
        self.__start_sanity_threads()
        while self.__alive:
            conn, addr = self.__socket.accept()
            try:
                handler = self.__build_handler_thread(self.__context, conn, addr)
                self.__handlers.append(handler)
                handler.start()
            except:
                self.__logger.exception("Exception in main thread!", exc_info=True)

    def __listen(self):
        self.__socket.listen(int(os.getenv("MAX_CLIENTS", 1000)))
        self.__logger.info("Started server on " + self.__host + ":" + str(self.__port))
        self.__alive = True

    def shutdown(self):
        self.__logger.info("Stopping server..")
        self.__alive = False
        self.__socket.close()
        for handler in self.__handlers:
            handler.stop()
        self.__logger.info("Bye!")

    def is_alive(self):
        return self.__alive

    def get_clients_count(self):
        return len(self.__handlers)

    def __cleanup(self):
        def cleanup_handlers(self):
            for thread in self.__handlers:
                if not thread.isAlive():
                    self.__handlers.remove(thread)
            self.__logger.debug("Cleanup processed. Current threads count: %d" % len(self.__handlers))
        util.periodically(lambda: cleanup_handlers(self), lambda: self.__alive, int(os.getenv("CLEANUP_TIMEOUT") or 5))

    def __start_sanity_threads(self):
        def start_thread(t):
            self.__threads.append(t)
            t.start()

        start_thread(Thread(name="Cleanup", target=self.__cleanup))

    def __build_socket_context(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(os.getcwd() + "/" + str(os.getenv("CERT_FILE", "cert/cert.pem")),
                                os.getcwd() + "/" + str(os.getenv("KEY_FILE", "cert/key.pem")))
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        context.set_ciphers("EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH")
        return context

    def __build_socket(self, host, port, context):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((host, port))
        return soc

    def __build_handler_thread(self, context, conn, addr):
        conn = context.wrap_socket(conn, server_side=True)
        handler = Handler(conn)
        handler.setName("Client<" + str(addr[0]) + ":" + str(addr[1]) + ">")
        return handler
