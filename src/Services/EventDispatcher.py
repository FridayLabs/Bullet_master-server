import inject


class EventDispatcher:
    logger = inject.attr('Logger')
    events = {}

    def add_listener(self, event, listener):
        if event in self.events:
            self.events[event].append(listener)
        else:
            self.events[event] = [listener]

    def dispatch(self, event, *args, **kwrags):
        if args:
            self.logger.warning('Do not use args in events handlers!. Event: %s' % str(event))
        if event in self.events:
            self.logger.debug('Event: %s %s' % (str(event), kwrags,))
            for handler in self.events[event]:
                handler(kwrags)
