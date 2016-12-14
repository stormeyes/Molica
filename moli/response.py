import json
import base64
import hashlib
from .event_machine import EventMachine
from .connection_pool import ConnectionPool


GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

connection_pool = ConnectionPool()


class HttpResponse:
    def __init__(self, transport=None):
        self.transport = transport
        self.websocket_key = None
        self.websocket_answer = (
            'HTTP/1.1 101 Switching Protocols',
            'Upgrade: websocket',
            'Connection: Upgrade',
            'Sec-WebSocket-Accept: {websocket_key}\r\n\r\n',
        )

    def send(self, message):
        self.transport.write(message)

    def handshake(self, request):
        self.websocket_key = request.header['Sec-WebSocket-Key']
        encrypt_key = self._compute_websocket_key()
        handshake_response_header = '\r\n'.join(self.websocket_answer)\
            .format(websocket_key=encrypt_key.decode())
        self.send(handshake_response_header.encode())

    def raise_error(self, status_code):
        pass

    def _compute_websocket_key(self):
        hash_key = hashlib.sha1((self.websocket_key + GUID).encode()).digest()
        base64_key = base64.b64encode(hash_key)
        return base64_key


class WebSocketResponse:
    def __init__(self, connection):
        self.connection = connection

    # handle request message, detect which to emit local exist event
    def handle(self, message):
        # trigger the default data event on each time client send the data
        EventMachine.emit('data', message, net=False, local=True, connection=self.connection)
        # treat as event machine format request
        if self._is_json(message) and ('event' and 'data' in self.message):
            return EventMachine.emit(self.message['event'], self.message['data'],
                                     net=False, local=True, connection=self.connection)

    def _is_json(self, message):
        try:
            self.message = json.loads(message)
        except ValueError:
            return False
        return True

    def send(self, message):
        self.connection.send(message, encode=True)
