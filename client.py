import os
import sys
import socket
from src.util import import_procotol_class

from google.protobuf.any_pb2 import Any
from protocol.hello_pb2 import Hello

container = {
    'buffer': b''
}


def main():
    while True:
        # try:
        cmd = input('>')
        result = handle_command(cmd.split(" "))
        if result:
            print(result)
        # except Exception as e:
        # print(e)


def handle_command(args):
    cmd = args[0]
    args = args[1:]
    if cmd == 'connect' or cmd == 'c':
        return connect(args)
    elif cmd == 'disconnect' or cmd == 'd':
        return disconnect(args)
    elif cmd == 'receive' or cmd == 'r':
        return receive(args)
    elif cmd == 'send' or cmd == 's':
        return send(args)
    elif cmd == 'send-packet' or cmd == 'sp':
        return send_packet(args)


def receive(args):
    if len(container['buffer']) == 0:
        container['buffer'] += container['socket'].recv(1024)
    if b'\0' in container['buffer']:
        packets = container['buffer'].split(b'\0')
        container['buffer'] = b'\0'.join(packets[1:])
        return dump_message(packets[0])


def dump_message(packet):
    any = Any()
    any.ParseFromString(packet)
    cl = import_procotol_class(any.type_url.split("/")[1])
    unpacked_message = cl()
    any.Unpack(unpacked_message)
    return (cl, unpacked_message)


def send(args):
    count = int(args[0])
    packets = b''
    for i in range(count):
        container['socket'].sendall(args[1] + b'\0')


def send_packet(args):
    hello = Hello()
    hello.Version = '123'
    hello.UserID = '123'
    hello.UserPass = '123'
    any = Any()
    Any.Pack(any, hello)
    packet = any.SerializeToString()
    return send([1, packet])


def connect(args):
    if 'connected' in container and container['connected'] is True:
        return 'Already connected'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', 9999))
    container['socket'] = s
    container['connected'] = True
    return 'Connected'


def disconnect(args):
    if 'connected' not in container or container['connected'] is False:
        return 'Already disconnected'
    try:
        container['socket'].shutdown(socket.SHUT_RDWR)
        container['socket'].close()
    except:
        pass
    container['socket'] = None
    container['connected'] = False
    return 'Disconnected'


if __name__ == "__main__":
    main()
