"""
parse used to parse the protocol such as websocket handshake or websocket message or http request
"""
import email
from io import StringIO
from .exceptions import NotWebSocketHandShakeException


def parse_factory(websocket=False, http=False, data=None):
    if websocket and data:
        pass
    elif http and data:
        return HttpParser(data)


class HttpParser:
    def __init__(self, data):
        self.socket_data = data

    @property
    def header(self):
        _, headers = self.socket_data.split('\r\n', 1)
        message = email.message_from_file(StringIO(headers))
        headers = dict(message.items())
        if 'Sec-WebSocket-Key' not in headers:
            raise NotWebSocketHandShakeException()
        return headers


class WebsocketParser:
    def __init__(self):
        pass

    @property
    def message(self):
        return ''