"""
The event machine is something like nodejs's event machine modules which provide on and emit,
in fact, there is no difference between on/emit and function call.

In Node, you use anonymous function to bind an event while you must use a named function in Python.

Duplicate `on` event will trigger by the defined order
"""
import functools
from collections import defaultdict
from .singleton import singleton
from .response import WebSocketResponse
from .exceptions import EventNotFoundException


@singleton
class EventRouter:
    def __init__(self):
        self.event_collection = defaultdict(list)

    def add_event(self, event, function):
        self.event_collection[event].append(function)

    def get_event(self, event):
        return self.event_collection[event]


class EventMachine:
    @classmethod
    def on(cls, event):
        if not isinstance(event, str):
            raise TypeError('event variable only expected string type')

        def on_wrapper(function):
            router = EventRouter()
            router.add_event(event, function)

            def _on(*args, **kwargs):
                # run on function called
                function(*args, **kwargs)

            return _on

        return on_wrapper

    @classmethod
    def emit(cls, event, data, to=None, broadcast=False, net=True, local=False, transport=None):
        if local:
            cls._emit_local(event, data, transport)
        if net:
            cls._emit_net(event, data, to, broadcast, transport)

    @classmethod
    def _emit_local(cls, event, data, transport):
        router = EventRouter()
        functions = router.get_event(event)
        if not functions:
            raise EventNotFoundException(event)
        for function in functions:
            function(dict(message=data, transport=transport))

    @classmethod
    def _emit_net(cls, event, data, to, broadcast, transport):
        WebSocketResponse({'event': event, 'data': data}, transport).send()
