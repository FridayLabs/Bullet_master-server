import os
from src.Services.Configurator import Configurator

os.environ['TESTING'] = 'True'


def pytest_runtest_setup():
    configurator = Configurator('.env.test')
    configurator.configure_everything()
