from .singleton import singleton


@singleton
class ConnectionPool:
    def __init__(self):
        self.pool = dict()

    def add(self, client_ip, client_port, transport):
        # todo: check if the key exists/ add time
        key = (client_ip, client_port)
        if key in self.pool:
            raise Exception
        else:
            self.pool.update({key: transport})
