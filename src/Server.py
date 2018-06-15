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
    handlers = []
    threads = []
    alive = True
    logger = inject.attr('Logger')

    def __init__(self):
        configurator = Configurator()
        configurator.configure_everything()

    def start(self, host, port):
        context = self.__build_socket_context()
        soc = self.__build_socket(host, port, context)
        self.logger.info("Started server on " + host + ":" + str(port))
        self.alive = True
        self.__start_sanity_threads()
        while self.alive:
            conn, addr = soc.accept()
            try:
                handler = self.__build_handler_thread(context, conn, addr)
                self.handlers.append(handler)
                handler.start()
            except:
                self.logger.exception("Exception in main thread!", exc_info=True)
        soc.close()

    def shutdown(self):
        self.logger.info("Stopping server..")
        self.alive = False
        for handler in self.handlers:
            handler.stop()
        self.logger.info("Bye!")

    def __cleanup(self):
        def cleanup_handlers(self):
            for thread in self.handlers:
                if not thread.isAlive():
                    self.handlers.remove(thread)
            self.logger.debug("Cleanup processed. Current threads count: %d" % len(self.handlers))
        util.periodically(lambda: cleanup_handlers(self), lambda: self.alive, int(os.getenv("CLEANUP_TIMEOUT") or 5))

    def __start_sanity_threads(self):
        def start_thread(t):
            self.threads.append(t)
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
        soc.listen(int(os.getenv("MAX_CLIENTS", 1000)))
        return soc

    def __build_handler_thread(self, context, conn, addr):
        conn = context.wrap_socket(conn, server_side=True)
        handler = Handler(conn)
        handler.setName("Client<" + str(addr[0]) + ":" + str(addr[1]) + ">")
        return handler
