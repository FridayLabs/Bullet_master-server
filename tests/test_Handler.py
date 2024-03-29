import os
import time
import pdb
from tests.Mocket import Mocket
from src.Handler import Handler
import logging


def test_pings_client():
    s = Mocket()
    h = Handler(s)
    h.start()
    time.sleep(0.6)
    h.stop()
    h.join()
    assert "Bullet.PingClient" in str(s.income_log)


def test_stops_on_disconnect(caplog):
    s = Mocket()
    h = Handler(s)
    h.start()
    s.close()
    time.sleep(0.5)
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
    time.sleep(0.1)
    assert h.alive == False
    try:
        assert h.alive == False
    finally:
        h.stop()
        h.join()
