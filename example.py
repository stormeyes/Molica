from moli import Moli, EventMachine


# broadcast your message to all connection!
@EventMachine.on('broadcast_message')
def on_handshake_event(connection):
    EventMachine.emit('chat_message', connection.message, broadcast=True)


# you can send message to list of friends, to="john" is ok if you only send to one client, on event name and emit name
# can be the same because event machine trigger by network default.
@EventMachine.on('point2point_talk')
def point2point_talk(connection):
    EventMachine.emit('point2point_talk', connection.message, to=['join', 'murphy'])


# The `connect` event will trigger on each time when client connect to server, named your connection
@EventMachine.on('connect')
def on_each_data_reciv(connection):
    connection.name = 'aaaaaa'
    EventMachine.emit('user', {'message': 'Hey buddy!'})


Moli.blossom(host='127.0.0.1', port=8013)

