"""
server create socket and make connection on each websocket client connect
"""
import logging
from .parser import parse_factory
from .response import HttpResponse, WebSocketResponse
from .exceptions import NotWebSocketHandShakeException
from .connection_pool import ConnectionPool
import asyncio


connection_pool = ConnectionPool()


class WebSocketProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self._has_handshake = False
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if self._has_handshake:
            websocket_parser = parse_factory(websocket=True, data=data)
            response = WebSocketResponse(websocket_parser.message, transport=self.transport)
            logging.info('Incoming message: {}'.format(websocket_parser.message))
            response.send()
        else:
            http_parser = parse_factory(http=True, data=data)
            response = HttpResponse(transport=self.transport)
            try:
                websocket_key = http_parser.header['Sec-WebSocket-Key']
                response.handshake(websocket_key)
            except NotWebSocketHandShakeException:
                response.raise_error(400)
            connection_pool.add(transport=self.transport)
            self._has_handshake = True
