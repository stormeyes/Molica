"""
parse used to parse the protocol such as websocket handshake or websocket message or http request
"""
import email
from io import StringIO
from .exceptions import NotWebSocketHandShakeException


def parser_http_header(data, websocket=True):
    socket_data = data.decode()

    _, headers = socket_data.split('\r\n', 1)
    message = email.message_from_file(StringIO(headers))
    headers = dict(message.items())
    if 'Sec-WebSocket-Key' not in headers and websocket:
        raise NotWebSocketHandShakeException()
    return headers


def websocket_message_deframing(frame_message):
    byte_array = frame_message
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


def websocket_message_framing(frame_message):
    bytes_formatted = [129]

    bytes_raw = frame_message.encode()
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
