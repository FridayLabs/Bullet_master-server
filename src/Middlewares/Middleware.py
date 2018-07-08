class Middleware:
    def __init__(self, transport):
        self.transport = transport

    def process(self, packet):
        return True
