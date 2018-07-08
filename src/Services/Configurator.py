import os
import inject
import logging
import threading
from peewee import *
from src.Services.Env import Env
from src.Services.Migrator import Migrator
from src.Services.LocalContext import LocalContext
from src.Services.ClientPinger import ClientPinger
from src.Services.PartyManager import PartyManager
from src.Services.EventDispatcher import EventDispatcher


class Configurator:
    env_file = '.env'

    def __init__(self, env_file='.env'):
        self.env_file = env_file

    def configure_everything(self):
        self.load_environment()
        self.configure_logging()
        self.configure_environment()

    def configure_logging(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(threadName)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if self.__is_debug_env():
            file_handler = logging.FileHandler(filename='logs/' + self.__env() + '.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG if self.__is_debug_env() else logging.INFO)

    def load_environment(self):
        env_file = os.getcwd() + '/' + self.env_file
        if os.path.isfile(env_file):
            Env(env_file).set_as_environment_variables()

    def configure_environment(self):
        def configurator(binder):
            binder.bind('APP_ROOT', os.getcwd())
            binder.bind('Version', os.getenv('VERSION'))
            ctxt = LocalContext()
            binder.bind('Context', ctxt)
            binder.bind_to_constructor('Logger', lambda: logging.getLogger())
            binder.bind_to_constructor('EventDispatcher', lambda: EventDispatcher())
            binder.bind_to_constructor('PartyManager', lambda: PartyManager())
            binder.bind_to_provider('Transport', lambda: ctxt.get('Transport'))
            binder.bind_to_provider('Client', lambda: ctxt.get('Client'))
            db = MySQLDatabase(
                os.getenv('DB_DATABASE'),
                host=os.getenv('DB_HOSTNAME'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                port=os.getenv('DB_PORT', 3306))
            binder.bind('DB', db)
            binder.bind('Migrator', Migrator(db, os.getcwd() + '/migrations'))
        inject.clear_and_configure(configurator)

    def migrate_db(self):
        migrator = inject.instance('Migrator')
        migrator.migrate()

    def __env(self):
        return os.getenv("ENVIRONMENT", "production")

    def __is_debug_env(self):
        return self.__env() in ["debug", 'test']
