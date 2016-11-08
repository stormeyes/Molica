import json
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

    def update(self):
        pass


class Connection:
    def __init__(self, name, transport):
        self.name = name
        self.transport = transport
        self.data = None

    # @property
    # def name(self):
    #     pass
    #
    # @name.setter
    # def name(self):
    #     pass

    def send(self, message, encode=True):
        if isinstance(message, dict):
            message = json.dumps(message)
        elif isinstance(message, str):
            pass
        else:
            raise Exception
        message = websocket_message_framing(message) if encode else message
        self.transport.write(message)

