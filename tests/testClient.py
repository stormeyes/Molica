import asyncio
from moli.client import Client, build_request_header
from moli.parser import websocket_message_framing

# c = Client('ws://127.0.0.1:8080')
#
#
# @c.on('data')
# def data_event(connection):
#     print(connection)
#
#
# c.emit('real', {'sssssssssss': 'ee'})


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print(data)
        a = websocket_message_framing('aaa')
        # self.transport.write(a)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

    def happy(self):
        print('you happy jiu ok')

loop = asyncio.get_event_loop()
message = build_request_header('127.0.0.1', '/', 'eScSjC4AiXW5EDM9XXiA1A==', 80)
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              '127.0.0.1', 8013)
men = loop.run_until_complete(coro)
print('====', men, '====')
loop.run_forever()
loop.close()

# c = Client('http://127.0.0.1:8013/')
# c.emit('user', 'aaaa')
# c.run_forever()