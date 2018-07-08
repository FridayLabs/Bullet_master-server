import inject
from src.Middlewares.Middleware import Middleware
from src.Util import packet_is_a
from protocol.Failure_pb2 import Failure
from protocol.Hello_pb2 import Hello


class HandshakeMiddleware(Middleware):
    def process(self, packet):
        if not packet_is_a(Hello, packet):
            return self.error("Handshake aborted")
        if inject.instance('Version') == packet.Version:
            self.transport.send_packet(Hello())
            return True
        else:
            return self.error("Client version is not compatible")

    def error(self, message):
        self.transport.send_packet(Failure(Message="Client version is not compatible"))
        self.transport.close()
        return False
