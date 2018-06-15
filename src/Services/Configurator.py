import os
import inject
import logging
import threading
from src.Services.Router import Router


class Configurator:
    def configure_everything(self):
        self.__configure_logging()
        self.__configure_environment()

    def __configure_logging(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(threadName)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO if self.__is_production_env() else logging.DEBUG)

    def __configure_environment(self):
        def confiigurator(binder):
            binder.bind('Version', os.getenv('VERSION'))
            binder.bind('Logger', logging.getLogger())
            binder.bind('Router', Router())
            binder.bind_to_provider('Client', lambda: getattr(threading.local(), 'client', None))
        inject.configure(confiigurator)

    def __is_production_env(self):
        return os.getenv("ENVIRONMENT") == "production"
