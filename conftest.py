import os
from src.Services.Configurator import Configurator


def pytest_runtest_setup():
    configurator = Configurator()
    configurator.configure_environment()
    os.environ['CLIENT_CHECK_TIMEOUT'] = '0'
    os.environ['CLEANUP_TIMEOUT'] = '0'
