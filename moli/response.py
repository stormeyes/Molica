import json
from .parser import compute_websocket_key
from .event_machine import EventMachine
from .connection_pool import ConnectionPool
from .log import log


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
        websocket_key = request.header['Sec-WebSocket-Key']
        encrypt_key = compute_websocket_key(websocket_key)
        handshake_response_header = '\r\n'.join(self.websocket_answer)\
            .format(websocket_key=encrypt_key.decode())
        self.send(handshake_response_header.encode())

    def raise_error(self, status_code):
        pass


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
        log.info('Server sending {} to Client'.format(message))
        self.connection.send(message, encode=True)
