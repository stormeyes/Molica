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

    def _encode_frame_message(self, message):
        bytes_formatted = [129]

        bytes_raw = message.encode()
        bytes_length = len(bytes_raw)
        if bytes_length <= 125:
            bytes_formatted.append(bytes_length)
        elif 126 <= bytes_length <= 65535:
            bytes_formatted.append(126)
            bytes_formatted.append((bytes_length >> 8) & 255)
            bytes_formatted.append(bytes_length & 255)
        else:
            bytes_formatted.append(127)
            bytes_formatted.append((bytes_length >> 56) & 255)
            bytes_formatted.append((bytes_length >> 48) & 255)
            bytes_formatted.append((bytes_length >> 40) & 255)
            bytes_formatted.append((bytes_length >> 32) & 255)
            bytes_formatted.append((bytes_length >> 24) & 255)
            bytes_formatted.append((bytes_length >> 16) & 255)
            bytes_formatted.append((bytes_length >> 8) & 255)
            bytes_formatted.append(bytes_length & 255)

        bytes_formatted = bytes(bytes_formatted)
        bytes_formatted = bytes_formatted + bytes_raw
        return bytes_formatted

    def send(self):
            # trigger event
            if self._is_json(self.message):
                if 'event' and 'data' in self.message:
                    EventMachine.emit(self.message['event'], self.message['data'], transport=self.transport)
                else:
                    raise Exception
            else:
                message = self._encode_frame_message('hey you this fuck')
                self.transport.write(message)
