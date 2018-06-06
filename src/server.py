import os
import time
import socket
import logging
from threading import Thread
from src.handler import Handler
import src.events as events


class Server:
    handlers = []
    threads = []
    alive = True

    def __init__(self):
        self.__configure_logging()
        self.__configure_threads()

    def __configure_logging(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO if self.__is_production_env() else logging.DEBUG)

    def __configure_threads(self):
        def start_thread(t):
            self.threads.append(t)
            t.start()

        start_thread(Thread(name="Cleanup", target=self.__cleanup))

    def __is_production_env(self):
        return os.getenv("ENVIRONMENT") == "production"

    def start(self, host, port):
        soc = self.__build_socket(host, port)
        logging.info("Started server on " + host + ":" + str(port))
        self.alive = True
        events.on_server_start()
        while self.alive:
            conn, addr = soc.accept()
            try:
                handler = self.__build_handler_thread(conn, addr)
                self.handlers.append(handler)
                handler.start()
            except:
                logging.exception("Exception in main thread!", exc_info=True)
        soc.close()

    def shutdown(self):
        logging.info("Stopping server..")
        self.alive = False
        for handler in self.handlers:
            handler.stop()
        logging.info("Bye!")

    def __cleanup(self):
        def cleanup_handlers(self):
            for thread in self.handlers:
                if not thread.isAlive():
                    self.handlers.remove(thread)
            logging.debug("Cleanup processed. Current threads count: %d" % len(self.handlers))
        self.__periodically(lambda: cleanup_handlers(self), int(os.getenv("CLEANUP_TIMEOUT") or 5))

    def __periodically(self, fn, timeout):
        current_timeout = 0
        step = 0.5
        while self.alive:
            time.sleep(step)
            current_timeout += step
            if current_timeout >= timeout:
                current_timeout = 0
                fn()

    def __build_socket(self, host, port):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((host, port))
        soc.listen(int(os.getenv("MAX_CLIENTS") or 1000))
        return soc

    def __build_handler_thread(self, conn, addr):
        handler = Handler(conn)
        handler.setName("Client<" + str(addr[0]) + ":" + str(addr[1]) + ">")
        return handler
