import os
from src.Services.Configurator import Configurator


def pytest_runtest_setup():
    try:
        os.remove('logs/test.log')
    except OSError:
        pass
    configurator = Configurator('.env.test')
    configurator.configure_everything()
