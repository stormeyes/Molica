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
from .exceptions import URLNotValidException


class Client:
    def __init__(self, URL):
        self.URL = URL
        self.connection = dict()
        self.loop = asyncio.get_event_loop()
        self.event_machine = dict()

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
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        parse = self.url_validation(self.URL)
        key = self.generate_key()
        # 握手
        header = build_request_header(parse.netloc, parse.path, key, parse.port)
        self.connection.reader, self.connection.writer = await asyncio.open_connection(
            parse.hostname, parse.port, loop=self.loop)
        self.connection['writer'].write(header)
        while True:
            data = await self.connection['reader'].read(1024)
            if not data:
                break
            print(data.decode())

    def emit(self, event, data):
        self.connection['writer'].write()

    def on(self, event, data):
        pass


def build_request_header(host, path, key, port=80):
    return 'GET {} HTTP/1.1\r\n' \
            'Host: {}:{}\r\n' \
            'Connection: keep-alive\r\n' \
            'Sec-WebSocket-Key: {} \r\n ' \
            'Sec-WebSocket-Version: 13' \
            'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36\r\n' \
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n' \
            'Accept-Encoding: gzip, deflate, sdch, br\r\n' \
            'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2\r\n\r\n'.format(path, host, port, key)

