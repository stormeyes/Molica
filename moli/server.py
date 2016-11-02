"""
server create socket and make connection on each websocket client connect
"""
from .parser import parse_factory
from .response import HttpResponse, WebSocketResponse
from .exceptions import NotWebSocketHandShakeException
from .connection_pool import ConnectionPool
try:
    import uvloop as asyncio
except ImportError:
    import asyncio


connection_pool = ConnectionPool()


class WebSocketProtocol(asyncio.protocols):
    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)
        self._hasHandShake = False
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if self._hasHandShake:
            websocket_parser = parse_factory(websocket=True, data=data)
            response = WebSocketResponse(websocket_parser.message)
            response.send()
        else:
            http_parser = parse_factory(http=True, data=data)
            response = HttpResponse()
            try:
                websocket_key = http_parser.header['Sec-WebSocket-Key']
                response.handshake(websocket_key)
            except NotWebSocketHandShakeException:
                response.raise_error(400)
            connection_pool.add()
            self._hasHandShake = True


loop = asyncio.get_event_loop()
coro = loop.create_server(WebSocketProtocol, '0.0.0.0', 8080)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
