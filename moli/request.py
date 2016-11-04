from .parser import websocket_message_deframing, parser_http_header


def request_factory(http_handshake=False, websocket=False, data=None):
    if http_handshake:
        return HttpHandshakeRequest(data)
    if websocket:
        return WebSocketRequest(data)


class WebSocketRequest:
    def __init__(self, data):
        self.data = data

    @property
    def message(self):
        return websocket_message_deframing(self.data)


class HttpHandshakeRequest:
    def __init__(self, data):
        self.data = data

    @property
    def header(self):
        return parser_http_header(self.data)

