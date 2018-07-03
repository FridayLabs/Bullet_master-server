from src.Server import Server
from threading import Thread
import socket
import ssl
import os
import pdb
import time


def build_server():
    server = Server('0.0.0.0', 10000)
    server.initialize()

    thread = Thread(target=server.start)
    thread.daemon = True
    return (thread, server,)


def build_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    certfile = os.getcwd() + '/cert/cert.pem'
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certfile)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    conn = context.wrap_socket(sock, server_hostname='ip.krasnoperov.tk')
    conn.connect(('0.0.0.0', 10000))
    return conn


def test_start_and_stop():
    t, s = build_server()
    t.start()
    try:
        time.sleep(0.5)
        assert s.is_alive() == True
        s.shutdown()
        time.sleep(0.5)
        assert s.is_alive() == False
        assert t.is_alive() == False
    finally:
        if s.is_alive():
            s.shutdown()
        t.join()


def test_client_can_connect():
    t, s = build_server()
    t.start()
    try:
        conn = build_client()
        time.sleep(0.6)
        assert s.get_clients_count() == 1
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        time.sleep(1)
        assert s.get_clients_count() == 0
    finally:
        s.shutdown()
        t.join()
