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
        hash_key = hashlib.sha1(self.websocket_key.encode()).digest()
        base64_key = base64.b64encode(hash_key)
        return base64_key


class WebSocketResponse:
    def __init__(self, message, transport=None):
        self.message = None
        self.frame_message = message
        self.transport = transport

    def _decode_message(self):
        byte_array = self.frame_message
        datalength = byte_array[1] & 127
        index_first_mask = 2
        if datalength == 126:
            index_first_mask = 4
        elif datalength == 127:
            index_first_mask = 10
        masks = [m for m in byte_array[index_first_mask: index_first_mask + 4]]
        index_first_data_byte = index_first_mask + 4
        decoded_chars = []
        i = index_first_data_byte
        j = 0
        while i < len(byte_array):
            decoded_chars.append(chr(byte_array[i] ^ masks[j % 4]))
            i += 1
            j += 1
        self.message = ''.join(decoded_chars)

    def _is_json(self, message):
        try:
            self.frame_message = json.loads(message)
        except ValueError:
            return False
        return True

    def send(self):
        # trigger event
        if self._is_json(self.frame_message):
            if 'event' and 'data' in self.frame_message:
                EventMachine.emit(self.frame_message['event'], self.frame_message['data'])
            else:
                raise Exception
