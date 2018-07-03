from src.Models.User import User
import peewee as pw


def migrate(migrator, database, fake=False, **kwargs):
    migrator.add_fields(User, latency=pw.IntegerField(default=0))


def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_fields(User, 'latency')
