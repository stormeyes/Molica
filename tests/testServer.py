from moli import Moli, EventMachine


@EventMachine.on('data')
def data_event(connection):
    print('data event trigger and the data is ', connection.data)


@EventMachine.on('connect')
def connect_event(connection):
    print('connect event trigger', connection.data)


@EventMachine.on('mybaby')
def user_event(connection):
    print('mybaby event', connection.data)
    EventMachine.emit('ss', 'sirena', connection=connection)


Moli.blossom('127.0.0.1', 8013)
