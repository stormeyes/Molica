"""
The client for moli
example:
    m = moli.client()
    m.on('connect', )
    m.on('message', )
    m.emit('foo', {bar: 'barbiQ'})
"""
import json
import base64
import random
import asyncio
from urllib.parse import urlparse
from .parser import parser_http_header, websocket_message_framing, websocket_message_deframing
from .exceptions import URLNotValidException


class Client:
    def __init__(self, URL):
        self.URL = URL
        self.connection = dict(reader=None, writer=None)
        self.loop = asyncio.get_event_loop()
        self.event_machine = dict()

        self.loop.run_until_complete(self.connect())

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

    def run_forever(self):
        self.loop.run_forever()

    async def connect(self):
        server_header = b''
        parser = self.url_validation(self.URL)
        key = self.generate_key()
        # 握手
        header = build_request_header(parser.netloc, parser.path, key, parser.port)
        self.connection['reader'], self.connection['writer'] = await asyncio.open_connection(
            parser.hostname, parser.port or 80, loop=self.loop)
        self.connection['writer'].write(header.encode())
        while True:
            chunk = await self.connection['reader'].readline()
            server_header += chunk
            if chunk == b'\r\n':
                break
        header_dict = parser_http_header(server_header, websocket=False)

    def emit(self, event, data):
        message = json.dumps({'event': 'user', 'data': 'sync'})
        framing_message = websocket_message_framing(message, 1)
        self.connection['writer'].write(framing_message)

    def on(self, event, data):
        pass


class LocalConnection:
    def __init__(self, reader=None, writer=None):
        self.reader = reader
        self.writer = writer


def build_request_header(host, path, key, port):
    return 'GET {} HTTP/1.1\r\n' \
            'Host: {}:{}\r\n' \
            'Connection: Upgrade\r\n' \
            'Upgrade: websocket\r\n' \
            'Sec-WebSocket-Version: 13\r\n' \
            'Sec-WebSocket-Key: {}\r\n' \
            'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36\r\n' \
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n' \
            'Accept-Encoding: gzip, deflate, sdch, br\r\n' \
            'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2\r\n\r\n'.format(path, host, port or 80, key)

