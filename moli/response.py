import json
from .event_machine import emit


GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


class HttpResponse:
    def send(self):
        pass

    def handshake(self, websocket_key):
        pass

    def raise_error(self, status_code):
        pass

    def _compute_websocket_key(self):
        pass


class WebSocketResponse:
    def __init__(self, message, transport=None):
        self.message = message
        self.transport = transport

    def _decode_message(self):
        pass

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
                emit(self.message['event'], self.message['data'])
            else:
                raise Exception
