"""
parse used to parse the protocol such as websocket handshake or websocket message or http request
"""
import email
from io import StringIO
from .exceptions import NotWebSocketHandShakeException


def parse_factory(websocket=False, http=False, data=None):
    if websocket and data:
        pass
    elif http and data:
        return HttpParser(data)


class HttpParser:
    def __init__(self, data):
        self.socket_data = data

    @property
    def header(self):
        _, headers = self.socket_data.split('\r\n', 1)
        message = email.message_from_file(StringIO(headers))
        headers = dict(message.items())
        if 'Sec-WebSocket-Key' not in headers:
            raise NotWebSocketHandShakeException()
        return headers


class WebsocketParser:
    def __init__(self, frame_message):
        self.frame_message = frame_message

    @property
    def message(self):
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
        return ''.join(decoded_chars)