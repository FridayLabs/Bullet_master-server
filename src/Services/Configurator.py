import os
import inject
import logging
import threading
from src.Services.Env import Env
from src.Services.Router import Router


class Configurator:
    def configure_everything(self):
        self.__load_environment()
        self.__configure_logging()
        self.__configure_environment()

    def __configure_logging(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(threadName)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if self.__is_debug_env() else logging.INFO)

    def __load_environment(self):
        env_file = os.getcwd() + '/.env'

        if os.path.isfile(env_file):
            Env(env_file).set_as_environment_variables()

    def __configure_environment(self):
        def confiigurator(binder):
            binder.bind('Version', os.getenv('VERSION'))
            binder.bind('Logger', logging.getLogger())
            binder.bind('Router', Router())
            binder.bind_to_provider('Client', lambda: getattr(threading.local(), 'client', None))
        inject.configure(confiigurator)

    def __is_debug_env(self):
        return os.getenv("ENVIRONMENT", "production") == "debug"
