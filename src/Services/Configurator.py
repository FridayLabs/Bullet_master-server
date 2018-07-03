import os
import inject
import logging
import threading
from peewee import *
from src.Services.Migrator import Migrator
from src.Services.Env import Env
from src.Services.Router import Router


class Configurator:
    env_file = '.env'
    __environment_configured = False

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
        logger.setLevel(logging.DEBUG if self.__is_debug_env() else logging.INFO)

    def load_environment(self):
        env_file = os.getcwd() + '/' + self.env_file
        if os.path.isfile(env_file):
            Env(env_file).set_as_environment_variables()

    def configure_environment(self):
        def configurator(binder):
            binder.bind('APP_ROOT', os.getcwd())
            binder.bind('Version', os.getenv('VERSION'))
            binder.bind('Logger', logging.getLogger())
            binder.bind('Router', Router())
            binder.bind_to_provider('Client', lambda: getattr(threading.local(), 'client', None))
            db = MySQLDatabase(
                os.getenv('DB_DATABASE'),
                host=os.getenv('DB_HOSTNAME'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                port=os.getenv('DB_PORT', 3306))
            binder.bind('DB', db)
            binder.bind('Migrator', Migrator(db, os.getcwd() + '/migrations'))

        if not Configurator.__environment_configured:
            inject.configure(configurator)
            Configurator.__environment_configured = True

    def migrate_db(self):
        migrator = inject.instance('Migrator')
        migrator.migrate()

    def __is_debug_env(self):
        env = os.getenv("ENVIRONMENT", "production")
        return env == "debug" or env == 'test'
