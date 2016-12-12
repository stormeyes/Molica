class NotWebSocketHandShakeException(Exception):
    def __str__(self):
        return 'The request is not a websocket handshake because there is no Sec-WebSocket-Key param on header'


class URLNotValidException(Exception):
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return 'The websocket URL {} is valid'.format(self.param)
