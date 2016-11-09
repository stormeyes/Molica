class NotWebSocketHandShakeException(Exception):
    def __str__(self):
        return 'The request is not a websocket handshake because there is no Sec-WebSocket-Key param on header'
