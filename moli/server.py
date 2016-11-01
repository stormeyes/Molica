"""
server create socket and make connection on each websocket client connect
"""
import re
from .parser import ProtocolParse
try:
    import uvloop as asyncio
except ImportError:
    import asyncio


GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


class WebSocketProtocol(asyncio.protocols):
    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)
        self.hasHandShake = False
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if self.hasHandShake:
            pass
        else:
            parser = ProtocolParse(websocket=True)
            websocket_key = parser.header['Sec-WebSocket-Key']
            self.hasHandShake = True



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
