import json
import base64
import hashlib
from .event_machine import EventMachine
from .parser import websocket_message_framing
from .connection_pool import Connection


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
    def __init__(self, transport=None):
        self.transport = transport

    def _is_json(self, message):
        try:
            self.message = json.loads(message)
        except ValueError:
            return False
        return True

    def _encode_frame_message(self, message):
        return websocket_message_framing(message)

    def send(self, message):
            if self._is_json(self.message):
                # response by trigger local event
                if 'event' and 'data' in self.message:
                    EventMachine.emit(self.message['event'], self.message['data'], local=True, net=False)
                else:
                    raise Exception
            else:
                encode_message = self._encode_frame_message(message)
                self.transport.write(encode_message)
