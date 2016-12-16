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
from .event_machine import EventMachine

connection_pool = ConnectionPool()


class WebSocketProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self._has_handshake = False
        self.transport = None
        self.connection = None

    def connection_made(self, transport):
        # TCP connection establish
        self.transport = transport

    def data_received(self, data):
        print(data)
        if self._has_handshake:
            r = request_factory(websocket=True, data=data, transport=self.transport)
            log.info('Incoming message: {}'.format(r.message))
            response = WebSocketResponse(self.connection)
            response.handle(r.message)
        else:
            r = request_factory(http_handshake=True, data=data, transport=self.transport)
            log.info('Server starting handshake with client at {}, port {}'.format(r.client['ip'], r.client['port']))
            response = HttpResponse(self.transport)
            try:
                response.handshake(r)
            except NotWebSocketHandShakeException:
                response.raise_error(400)
            uuid_name = ''.join([(string.ascii_letters+string.digits)[x] for x in random.sample(range(0, 62), 8)])
            # Websocket connection establish
            connection = Connection(
                name=uuid.uuid3(uuid.NAMESPACE_DNS, uuid_name),
                transport=self.transport
            )
            connection_pool.add(connection)
            log.info('Connection with {}:{} has established'.format(r.client['ip'], r.client['port']))
            self._has_handshake = True
            self.connection = connection
            # trigger websocket connection connect event
            EventMachine.emit('connect', None, net=False, local=True, connection=connection)
