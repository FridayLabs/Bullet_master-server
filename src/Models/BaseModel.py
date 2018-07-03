import inject
from peewee import Model, Proxy


class DatabaseProxy(Proxy):
    def __getattr__(self, attr):
        self.obj = inject.instance('DB')
        return getattr(self.obj, attr)


class BaseModel(Model):
    class Meta:
        database = DatabaseProxy()
