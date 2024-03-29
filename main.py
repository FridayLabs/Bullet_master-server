import os
import sys
import signal
from src.Server import Server

server = Server(os.getenv("LISTEN", "0.0.0.0"), int(os.getenv("PORT", 9999)))


def exit():
    server.shutdown()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda x, y: exit())
    try:
        server.initialize()
        server.start()
    except KeyboardInterrupt:
        exit()
