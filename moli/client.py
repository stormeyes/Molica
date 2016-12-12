"""
The client for moli
example:
    m = moli.client()
    m.on('connect', )
    m.on('message', )
    m.emit('foo', {bar: 'barbiQ'})
"""
from .event_machine import EventMachine


class Client:
    def __init__(self, URL):
        self.URL = URL

        self.connect()

    def connect(self):
        pass

    def emit(self, event, data):
        pass

    def on(self, event, data):
        EventMachine.on(event)