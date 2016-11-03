import time
from .singleton import singleton


@singleton
class ConnectionPool:
    def __init__(self):
        self.pool = dict()

    def add(self, transport):
        client_ip, client_port = transport.get_extra_info('peername')
        key = (client_ip, client_port, int(time.time()))
        if key in self.pool:
            raise Exception
        else:
            self.pool.update({key: transport})

    def get(self, name):
        pass


class Connection:
    def __init__(self, transport, name):
        self.transport = transport
        self._name = name

    @property
    def name(self):
        pass

    @name.setter
    def name(self):
        pass
