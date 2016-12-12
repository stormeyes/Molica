"""
The client for moli
example:
    m = moli.client()
    m.on('connect', )
    m.on('message', )
    m.emit('foo', {bar: 'barbiQ'})
"""
import base64
import random
import asyncio
from urllib.parse import urlparse
from .event_machine import EventMachine
from .exceptions import URLNotValidException


class Client:
    def __init__(self, URL):
        self.coroutine = None
        self.URL = URL
        self.loop = asyncio.get_event_loop()

        self.connect()

    def generate_key(self):
        seed_random = int(random.random() * 10 ** 16)
        return base64.b64encode(seed_random.__str__().encode())

    def url_validation(self, url):
        parse = urlparse(url)

        if parse.scheme not in ['http', 'https', 'ws', 'wss']:
            raise URLNotValidException('scheme')
        elif not parse.netloc:
            raise URLNotValidException('host')
        else:
            return parse

    def connect(self):
        parse = self.url_validation(self.URL)
        key = self.generate_key()
        header = build_request_header(parse.netloc, parse.path, key, parse.port)
        self.coroutine = self.loop.create_connection(
            lambda: EchoClientProtocol(header, self.loop), parse.netloc, port=parse.port or 80)

    def emit(self, event, data):
        pass

    def on(self, event, data):
        EventMachine.on(event)


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


def build_request_header(host, path, key, port=80):
    return 'GET /{} HTTP/1.1 \r\n ' \
             'Host: {}:{} \r\n ' \
             'Upgrade: websocket \r\n ' \
             'Connection: Upgrade \r\n ' \
             'Sec-WebSocket-Key: {} \r\n ' \
             'Sec-WebSocket-Version: 13'.format(path, host, port, key)
