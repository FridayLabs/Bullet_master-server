import os
import sys
import socket
import ssl
import traceback
from src.Util import import_procotol_class
from protocol.Authenticate_pb2 import Authenticate
from google.protobuf.any_pb2 import Any

container = {
    'buffer': b''
}


def main():
    while True:
        try:
            cmd = input('>')
            result = handle_command(cmd.split(" "))
            if result:
                print(result)
        except Exception as e:
            print(e)
            for l in traceback.format_tb(e.__traceback__):
                print(l)


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
    elif cmd == 'auth' or cmd == 'a':
        return authenticate(args)


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


def authenticate(args):
    auth = Authenticate()
    if len(args) == 0:
        auth.UserID = 'admin'
        auth.UserPassword = 'admin'
    else:
        auth.UserID = args[0]
        auth.UserPassword = args[1]
    auth.ClientVersion = 'v0.0.1-alpha'
    any = Any()
    Any.Pack(any, auth)
    packet = any.SerializeToString()
    return send([1, packet])


def __send_packet(packet):
    any = Any()
    Any.Pack(any, packet)
    packet = any.SerializeToString()
    return send([1, packet])


def connect(args):
    if 'connected' in container and container['connected'] is True:
        return 'Already connected'
    if len(args) > 0 and args[0] == 'prod':
        host = 'ip.krasnoperov.tk'
    else:
        host = '0.0.0.0'
    print("connecting " + host)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    certfile = os.getcwd() + '/cert/cert.pem'
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certfile)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    conn = context.wrap_socket(sock, server_hostname='ip.krasnoperov.tk')
    conn.connect((host, 9999))
    container['socket'] = conn
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
