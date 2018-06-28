import os
import time
import pdb
from tests.Mocket import Mocket
from src.Handler import Handler
import logging

os.environ['CLIENT_CHECK_TIMEOUT'] = '0'

check_timeout = int(os.getenv("CLIENT_CHECK_TIMEOUT", 5)) + 2


def test_pings_client():
    s = Mocket()
    h = Handler(s)
    h.start()
    time.sleep(check_timeout)
    h.stop()
    h.join()
    assert "Bullet.PingClient" in str(s.income_log)


def test_stops_on_disconnect(caplog):
    s = Mocket()
    h = Handler(s)
    h.start()
    time.sleep(0.5)
    s.close()
    time.sleep(check_timeout)
    try:
        assert h.alive == False
    finally:
        h.stop()
        h.join()


def test_stops_on_error():
    s = Mocket()
    h = Handler(s)
    h.start()
    time.sleep(0.5)
    s.set_throw_error(True)
    time.sleep(check_timeout)
    assert h.alive == False
    try:
        assert h.alive == False
    finally:
        h.stop()
        h.join()
