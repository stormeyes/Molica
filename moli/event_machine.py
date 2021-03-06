"""
The event machine is something like nodejs's event machine modules which provide on and emit,
in fact, there is no difference between on/emit and function call.

In Node, you use anonymous function to bind an event while you must use a named function in Python.

Duplicate `on` event will trigger by the defined order
"""
import functools
from collections import defaultdict
from .log import log
from .singleton import singleton
from .connection_pool import Connection, ConnectionPool

connection_pool = ConnectionPool()


@singleton
class EventRouter:
    def __init__(self):
        self.event_collection = defaultdict(list)
        self._init_default_event()

    def _init_default_event(self):
        self.event_collection['connect'].append(lambda *args: None)
        self.event_collection['data'].append(lambda *args: None)

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
        log.info('server event {} triggered and send data {}'.format(event, data))
        if local:
            '''
            In the local env, the connection is not exist in fact, we wrapper data into connection type
            '''
            if not connection:
                connection = Connection(None, None)
            connection.data = data
            cls._emit_local(event, connection)
        if net:
            """
            :param to: means the message send to specify person / named connection
            :param broadcast: means send to all connection
            :param connection: means only current client

            !! ONLY ONE OF THEM CAN BE NOT NONE
            """
            if any([to, broadcast, connection]):
                cls._emit_net(event, data, to, broadcast, connection)
            else:
                raise Exception

    @classmethod
    def _emit_local(cls, event, connection):
        router = EventRouter()
        functions = router.get_event(event)
        if not functions and event != 'data':
            return log.warning(
                'event `{}` not found! Please check if you have `on` method to handler it.'.format(event))
        for function in functions:
            function(connection)

    @classmethod
    def _emit_net(cls, event, data, to, broadcast, connection):
        if to:
            client_list = to if isinstance(to, list) else [to]
        elif broadcast:
            client_list = connection_pool.pool.keys()
        else:
            client_list = [connection.name]
        # if event is None, regards the emit as Non event machine style and send raw data directly
        message = data if event is None else {'event': event, 'data': data}
        for connection_name in client_list:
            log.info('Server sending {} to Client'.format(message))
            connection_pool.get(connection_name).send(message)
            # del connection_pool.get(connection_name).data
