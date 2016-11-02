import json
import base64
import hashlib
from .event_machine import EventMachine


GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


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

    def handshake(self, websocket_key):
        self.websocket_key = websocket_key
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
    def __init__(self, message, transport=None):
        self.message = message
        self.transport = transport

    def _is_json(self, message):
        try:
            self.message = json.loads(message)
        except ValueError:
            return False
        return True

    def send(self):
        # trigger event
        if self._is_json(self.message):
            if 'event' and 'data' in self.message:
                EventMachine.emit(self.message['event'], self.message['data'])
            else:
                raise Exception
