import inject
from hashlib import md5
from peewee import *
from src.Models.BaseModel import BaseModel


class User(BaseModel):
    id = AutoField()
    user_identifier = CharField(unique=True)
    password = CharField()
    latency = IntegerField(default=0)

    def hashify_password(self):
        self.password = self.get_password_hash(self.password)

    @staticmethod
    def get_password_hash(password):
        hash = md5()
        hash.update(('SWf93nWzeXA1LcqGmCf4' + password).encode())
        return hash.hexdigest()
