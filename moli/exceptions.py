class EventNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'event `{}` not found! Please check if you had used `on` method to handler it.'.format(self.value)


class NotWebSocketHandShakeException(Exception):
    def __str__(self):
        return 'The request is not a websocket handshake because there is no Sec-WebSocket-Key param on header'
