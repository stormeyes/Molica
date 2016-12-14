from moli import Moli, EventMachine


@EventMachine.on('data')
def data_event(connection):
    print('data event', connection.data)


@EventMachine.on('connect')
def connect_event(connection):
    print('connect event', connection.data)


@EventMachine.on('user')
def user_event(connection):
    print('user event', connection.data)
    EventMachine.emit('ss', '111111', connection=connection)


Moli.blossom('127.0.0.1', 8013)
