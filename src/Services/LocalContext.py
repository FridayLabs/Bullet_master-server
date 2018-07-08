import threading


class LocalContext:
    __context_data = {}

    def get(self, key, default=None):
        return self.__context().get(key, default)

    def set(self, key, value):
        self.__context()[key] = value

    def __context(self):
        id = self.__thread_id()
        if id not in self.__context_data:
            self.__context_data[id] = {}
        return self.__context_data[id]

    def __thread_id(self):
        return id(threading.current_thread())
