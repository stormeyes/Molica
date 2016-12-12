import json
from .log import log
from .singleton import singleton
from .parser import websocket_message_framing


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
        if name not in self.pool:
            raise Exception
        else:
            return self.pool.get(name)

    def update(self, connection, new_name):
        if new_name in self.pool:
            log.warning("duplicated name!")
        self.pool[new_name] = self.pool.pop(connection.name)


class Connection:
    def __init__(self, name, transport):
        self._name = name
        self.transport = transport
        self.data = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        connection_pool.update(self, new_name)
        self._name = new_name

    def send(self, message, encode=True):
        if isinstance(message, dict):
            message = json.dumps(message)
        elif not isinstance(message, str):
            raise Exception
        message = websocket_message_framing(message) if encode else message
        self.transport.write(message)


connection_pool = ConnectionPool()

