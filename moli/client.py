import json
import base64
import random
import asyncio
from urllib.parse import urlparse
from .log import log
from .parser import parser_http_header, websocket_message_framing, websocket_message_deframing, compute_websocket_key
from .exceptions import URLNotValidException
from .event_machine import EventRouter

event_router = EventRouter()


def build_request_header(host, path, key, port):
    return 'GET {} HTTP/1.1\r\n' \
            'Host: {}:{}\r\n' \
            'Connection: Upgrade\r\n' \
            'Upgrade: websocket\r\n' \
            'Sec-WebSocket-Version: 13\r\n' \
            'Sec-WebSocket-Key: {}\r\n\r\n'.format(path, host, port or 80, key)


class WebSocketClient(asyncio.Protocol):
    def __init__(self, handshake_header, loop):
        self.websocket_key = None
        self._has_handshake = False
        self.handshake_header = handshake_header
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.handshake_header.encode())

    def data_received(self, data):
        if self._has_handshake:
            deframing_data = websocket_message_deframing(data)
            data_event_func = event_router.get_event('data')
            if data_event_func:
                for event_func in data_event_func:
                    event_func(deframing_data)
            try:
                response_data = json.loads(deframing_data)
                if response_data['event'] and response_data['data']:
                    event_list = event_router.get_event(response_data['event'])
                    for event_func in event_list:
                        event_func(response_data)
            except ValueError:
                pass
        else:
            self._has_handshake = True
            websocket_key_pair = self.generate_key_pair()
            http_header = parser_http_header(data, websocket_accept=False)
            print(http_header, websocket_key_pair)

    def connection_lost(self, exc):
        log.info('The server closed the connection so I STOP the event loop')
        self.loop.stop()

    def generate_key_pair(self):
        return compute_websocket_key(self.websocket_key)


class Client:
    def __init__(self, url):
        self.URL = url
        self.connection = None
        self.clientProtocol = None
        self.websocket_key = None
        self.loop = asyncio.get_event_loop()

        self.connect()

    @staticmethod
    def generate_key():
        seed_random = int(random.random() * 10 ** 16)
        return base64.b64encode(seed_random.__str__().encode())

    @staticmethod
    def url_validation(URL):
        parse = urlparse(URL)

        if parse.scheme not in ['http', 'https', 'ws', 'wss']:
            raise URLNotValidException('scheme')
        elif not parse.netloc:
            raise URLNotValidException('host')
        else:
            return parse

    def connect(self):
        parser = self.url_validation(self.URL)
        self.websocket_key = self.generate_key()
        header = build_request_header(parser.hostname, parser.path, self.websocket_key, parser.port)
        connection_coroutine = self.loop.create_connection(
            lambda: WebSocketClient(header, self.loop), parser.hostname, parser.port or 80)

        self.connection, self.clientProtocol = self.loop.run_until_complete(connection_coroutine)

        self.clientProtocol.websocket_key = self.websocket_key

    def run_forever(self):
        self.loop.run_forever()

    def emit(self, event, data):
        if not isinstance(event, str):
            log.error('typeError')
            raise TypeError('event variable only expected string type')

        message = json.dumps({'event': event, 'data': data})
        framing_message = websocket_message_framing(message, True)
        self.connection.write(framing_message)

    def on(self, event):
        if not isinstance(event, str):
            raise TypeError('event variable only expected string type')

        def on_wrapper(function):
            router = EventRouter()
            router.add_event(event, function)

            def _on(*args, **kwargs):
                # run on function called
                function(*args, **kwargs)

            return _on

        return on_wrapper
