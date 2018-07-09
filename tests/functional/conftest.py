import os
import inject
import time
import pytest
from src.Services.Configurator import Configurator
from tests.functional.helpers import build_server
from tests.functional.FakeClient import FakeClient


@pytest.fixture()
def migrations():
    migrator = inject.instance('Migrator')
    migrator.migrate()
    yield
    migrator.rollback()


@pytest.fixture()
def server():
    t, server = build_server()
    try:
        t.start()
        time.sleep(1)
        yield server
    finally:
        server.shutdown()
        t.join()


@pytest.fixture()
def client():
    client = FakeClient()
    try:
        yield client
    finally:
        client.close()
