import inject
from src.PacketProcessors.PacketProcessor import PacketProcessor


class LatencyProcessor(PacketProcessor):
    __client = inject.attr('Client')
    __logger = inject.attr('Logger')

    def process(self, packet):
        import threading
        user = self.__client.get_user()
        latency = abs(packet.ServerTime - packet.ClientTime)
        self.__logger.debug('Setting latency to %d ms' % latency)
        user.latency = latency
        user.save()
