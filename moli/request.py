from .parser import websocket_message_deframing, parser_http_header


def request_factory(http_handshake=False, websocket=False, data=None, transport=None):
    if http_handshake:
        return HttpHandshakeRequest(data, transport)
    if websocket:
        return WebSocketRequest(data, transport)


class Request:
    def __init__(self, data, transport):
        self.data = data
        self.transport = transport

    @property
    def client(self):
        ip, port = self.transport.get_extra_info('peername')
        return dict(ip=ip, port=port)


class WebSocketRequest(Request):
    @property
    def message(self):
        return websocket_message_deframing(self.data)


class HttpHandshakeRequest(Request):
    @property
    def header(self):
        return parser_http_header(self.data)

