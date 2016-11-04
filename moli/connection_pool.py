from .singleton import singleton


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
    def __init__(self, name, transport, response):
        self.transport = transport
        self.name = name
        self.data = None
        self.response = response

    @property
    def name(self):
        pass

    @name.setter
    def name(self):
        pass

    def send(self, message):
        self.response.send(message)

    def handle(self, request):
        self.response.handle(request.message)

