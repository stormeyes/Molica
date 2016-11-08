"""
server create socket and make connection on each websocket client connect
"""
import asyncio
import uuid
import string
import random
from .request import request_factory
from .log import log
from .response import HttpResponse, WebSocketResponse
from .exceptions import NotWebSocketHandShakeException
from .connection_pool import Connection, ConnectionPool

connection_pool = ConnectionPool()


class WebSocketProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self._has_handshake = False
        self.transport = None
        self.connection = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if self._has_handshake:
            r = request_factory(websocket=True, data=data)
            log.info('Incoming message: {}'.format(r.message))
            response = WebSocketResponse(self.connection)
            response.handle(r.message)
        else:
            r = request_factory(http_handshake=True, data=data)
            # todo: bundle client ip/port info into request
            log.info('Server starting handshake with client at {}:{}')
            response = HttpResponse(self.transport)
            try:
                response.handshake(r)
            except NotWebSocketHandShakeException:
                response.raise_error(400)
            uuid_name = ''.join([(string.ascii_letters+string.digits)[x] for x in random.sample(range(0, 62), 8)])
            connection = Connection(
                name=uuid.uuid3(uuid.NAMESPACE_DNS, uuid_name),
                transport=self.transport
            )
            connection_pool.add(connection)
            self._has_handshake = True
            self.connection = connection
