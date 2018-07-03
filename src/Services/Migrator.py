import inject
from peewee_migrate import Router


class Migrator:
    def __init__(self, db, path):
        self.router = Router(db, migrate_dir=path)

    def migrate(self):
        self.router.run()

    def rollback(self):
        for name in reversed(self.router.done):
            self.router.rollback(name)
