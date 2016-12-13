from moli import Moli, EventMachine


@EventMachine.on('data')
def data_event(connection):
    print('data event', connection.data)


@EventMachine.on('connect')
def connect_event(connection):
    print('connect event', connection.data)


Moli.blossom('127.0.0.1', 8013)
