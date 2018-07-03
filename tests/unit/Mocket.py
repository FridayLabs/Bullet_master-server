class Mocket:
    buffer = b''
    income_log = b''
    throw_error = False
    is_closed = False
    is_shutdown = False

    def sendall(self, bytes):
        if self.throw_error or self.is_closed:
            raise Exception('Error on receive from socket!')
        self.income_log += bytes
        self.buffer += bytes

    def recv(self, len):
        if self.throw_error or self.is_closed:
            raise Exception('Error on receive from socket!')
        packet = self.buffer[:len]
        self.buffer = self.buffer[len:]
        return packet

    def set_throw_error(self, v):
        self.throw_error = v

    def shutdown(self, x):
        self.is_shutdown = True

    def close(self):
        self.is_closed = True
