"""
parse used to parse the protocol such as websocket handshake or websocket message or http request
"""
from random import choice
from string import ascii_uppercase
import email
import hashlib
import base64
from io import StringIO
from collections import namedtuple
from .exceptions import NotWebSocketHandShakeException

GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
opcode = namedtuple('Opcode', ['text', 'binary', 'ping', 'pong'])(1, 2, 9, 10)


def compute_websocket_key(websocket_key):
    if isinstance(websocket_key, str):
        pass
    elif isinstance(websocket_key, bytes):
        websocket_key = websocket_key.decode()
    else:
        raise TypeError('the parser only expected data as str/bytes type')

    hash_key = hashlib.sha1((websocket_key + GUID).encode()).digest()
    base64_key = base64.b64encode(hash_key)
    return base64_key


def parser_http_header(data, websocket_key=False, websocket_accept=False):
    if isinstance(data, str):
        socket_data = data
    elif isinstance(data, bytes):
        socket_data = data.decode()
    else:
        raise TypeError('the parser only expected data as str/bytes type')

    _, headers = socket_data.split('\r\n', 1)
    message = email.message_from_file(StringIO(headers))
    headers = dict(message.items())
    if 'Sec-WebSocket-Key' not in headers and websocket_key:
        raise NotWebSocketHandShakeException()
    if 'Sec-WebSocket-Accept' not in headers and websocket_accept:
        raise NotWebSocketHandShakeException()
    return headers


def websocket_message_deframing(frame_message):
    byte_array = frame_message
    datalength = byte_array[1] & 127
    mask = byte_array[1] >> 7 & 1
    index_first_mask = 2
    decoded_chars = []

    if datalength == 126:
        index_first_mask = 4
    elif datalength == 127:
        index_first_mask = 10
    if mask:
        masks = [m for m in byte_array[index_first_mask: index_first_mask + 4]]
        index_first_data_byte = index_first_mask + 4
        i = index_first_data_byte
        j = 0
        while i < len(byte_array):
            decoded_chars.append(chr(byte_array[i] ^ masks[j % 4]))
            i += 1
            j += 1
    else:
        decoded_chars = []
        index_first_data_byte = 2
        while index_first_data_byte < len(byte_array):
            decoded_chars.append(chr(byte_array[index_first_data_byte]))
            index_first_data_byte += 1

    return ''.join(decoded_chars)


def websocket_message_framing(message, mask=False):
    mask = int(mask)
    encoded_message = [129]
    if isinstance(message, str):
        message = bytes(message.encode())
    elif isinstance(message, bytes):
        pass
    else:
        raise TypeError('frame_message variable only expected string or bytes type')
    payload_length = len(message)

    # todo: default message type is `text`
    encoded_message.append((mask << 7) + payload_length)
    if mask:
        mask_key = ''.join(choice(ascii_uppercase) for i in range(4))
        [encoded_message.append(ord(key)) for key in mask_key]
        for index, byte in enumerate(message.decode()):
            encoded_message.append(ord(byte) ^ ord(mask_key[index % 4]))
    else:
        for byte in message.decode():
            encoded_message.append(ord(byte))
    return bytes(encoded_message)
