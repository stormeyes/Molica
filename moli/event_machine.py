"""
The event machine is something like nodejs's event machine modules which provide on and emit,
in fact, there is no difference between on/emit and function call.

In Node, you use anonymous function to bind an event while you must use a named function in Python.

Duplicate `on` event will trigger by the defined order
"""
from .singleton import singleton
from collections import defaultdict
# from .exception import eventNotFoundException


class event_router(dict):
    event_collection = defaultdict(list)

    def add_event(self, event, function):
        self.event_collection[event].append(function)

    def get_event(self, event):
        return self.event_collection[event]


def on(event):
    def on_wrapper(function):
        router = event_router()
        router.add_event(event, function)
        def on_kernel(*args, **kwargs):
            # run on function called
            function(*args, **kwargs)
        return on_kernel
    return on_wrapper


def emit(event, to=None, to_room=None, broadcast=False):
    router = event_router()
    for function in router.get_event(event):
        function()
