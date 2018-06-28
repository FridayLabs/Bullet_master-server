from src.Services.Configurator import Configurator


def pytest_runtest_setup():
    configurator = Configurator()
    configurator.configure_environment()
