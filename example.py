from moli import Moli, EventMachine, connection_pool

connection_pool_instance = connection_pool.ConnectionPool()


@EventMachine.on('rename')
def rename(connection):
    connection.name = connection.data
    EventMachine.emit(None, "rename ok!", connection=connection)


@EventMachine.on('emit_to_somebody')
def emit_to_somebody(connection):
    EventMachine.emit(None, 'you have some specify message', to=connection.data, connection=connection)


@EventMachine.on('sayhi')
def sayhi(connection):
    EventMachine.emit('goodTime', 'Seems great time', connection=connection)


@EventMachine.on('sayhi_again')
def sayhi_again(connection):
    EventMachine.emit('goodTime', {'message': 'what you this silly boy'}, connection=connection)


@EventMachine.on('sayhi_again')
def sayhi_again(connection):
    EventMachine.emit(None, {'message': 'Hey you this silly boy'}, connection=connection)


def trigger_by_other_side():
    EventMachine.emit('goodTime', {'message'}, to=['john', 'alice'])
    EventMachine.emit('sayhi', {'data'})


# broadcast your message to all connection!
@EventMachine.on('broadcast_message')
def on_handshake_event(connection):
    print(connection.data)
    EventMachine.emit('chat_message', connection.data, broadcast=True, connection=connection)


# you can send message to list of friends, to="john" is ok if you only send to one client, on event name and emit name
# can be the same because event machine trigger by network default.
@EventMachine.on('point2point_talk')
def point2point_talk(connection):
    EventMachine.emit('point2point_talk', connection.data, to=['join', 'murphy'], connection=connection)


# The `connect` event will trigger on each time when client connect to server, named your connection
@EventMachine.on('connect')
def on_each_data_reciv(connection):
    # connection.name = 'john'
    EventMachine.emit('user', {'message': 'Hey buddy!'}, connection=connection)


@EventMachine.on('data')
def on_each_data_reciv(connection):
    # connection.name = 'john'
    print(connection_pool_instance.pool)
    print('data event trigger', connection.data)
    # EventMachine.emit('user', {'message': 'Hey buddy!'}, connection=connection)


@EventMachine.on('disconnect')
def on_disconnect(connection):
    EventMachine.emit(None, 'Sad! someone leaves us just now', broadcast=True)


Moli.blossom(host='127.0.0.1', port=8013)

