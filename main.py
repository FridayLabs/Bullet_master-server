from src.server import Server
import os
import signal
import sys

server = Server()


def exit():
    server.shutdown()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda x, y: exit())
    try:
        server.start(
            os.getenv("LISTEN") or "0.0.0.0",
            int(os.getenv("PORT") or 9999)
        )
    except KeyboardInterrupt:
        exit()
