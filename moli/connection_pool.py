from .singleton import singleton
from .response import WebSocketResponse


@singleton
class ConnectionPool:
    def __init__(self):
        self.pool = dict()

    def add(self, connection):
        if not isinstance(connection, Connection):
            raise Exception
        key = connection.name
        if key in self.pool:
            raise Exception
        else:
            self.pool.update({key: connection})

    def get(self, name):
        return self.pool.get(name)

    def update(self):
        pass


class Connection:
    def __init__(self, name, transport):
        self.transport = transport
        self.name = name
        self.data = None
        self.response = WebSocketResponse(self.transport)

    @property
    def name(self):
        pass

    @name.setter
    def name(self):
        pass

    def send(self, message):
        self.response.send(message)

