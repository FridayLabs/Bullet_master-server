import inject
from peewee import DoesNotExist
from protocol.Failure_pb2 import Failure
from protocol.Success_pb2 import Success
from protocol.Hello_pb2 import Hello
from src.Models.User import User


class Client:
    authenticated = False
    user_id = None
    latency = 0
    user = None
    logger = inject.attr('Logger')

    def __init__(self, transport):
        self.transport = transport

    def authenticate(self, message):
        try:
            user = User.select().where(
                User.user_identifier == message.UserId,
                User.password == User.get_password_hash(message.UserPassword)
            ).get()
            self.user = user
            self.transport.send_packet(Success())
        except DoesNotExist:
            self.transport.send_packet(Failure())

    def set_latency(self, latency):
        if self.user is not None:
            self.user.latency = latency
            self.user.save()
        else:
            self.transport.send_packet(Failure(Message="Unauthenticated"))

    def check_version(self, version):
        if inject.instance('Version') == version:
            self.transport.send_packet(Hello())
        else:
            self.transport.send_packet(Failure(Message="Client version is not compatible"))
            self.transport.close()
