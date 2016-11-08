"""
The event machine is something like nodejs's event machine modules which provide on and emit,
in fact, there is no difference between on/emit and function call.

In Node, you use anonymous function to bind an event while you must use a named function in Python.

Duplicate `on` event will trigger by the defined order
"""
import functools
from collections import defaultdict
from .singleton import singleton
from .exceptions import EventNotFoundException
from .connection_pool import Connection


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
    def emit(cls, event, data, to=None, broadcast=False, net=True, local=False, connection=None):
        if local:
            '''
            In the local env, the connection is not exist in fact, we wrapper data into connection type
            '''
            if not connection:
                connection = Connection(None, None)
            connection.data = data
            cls._emit_local(event, connection)
        if net:
            if any([to, connection]):
                # todo: if to: find the named connection and send by for loop
                cls._emit_net(event, data, to, broadcast, connection)
            else:
                raise Exception

    @classmethod
    def _emit_local(cls, event, connection):
        router = EventRouter()
        functions = router.get_event(event)
        if not functions and event != 'data':
            # todo: the single thread will crash for having client send not exist event
            raise EventNotFoundException(event)
        for function in functions:
            function(connection)

    @classmethod
    def _emit_net(cls, event, data, to, broadcast, connection):
        connection.send({'event': event, 'data': data})
        del connection.data
