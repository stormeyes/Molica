from moli import Moli, EventMachine


@EventMachine.on('handshake')
def on_handshake_event(connection):
    print('11111111111')


@EventMachine.on('connection')
def on_each_data_reciv(connection):
    EventMachine.emit('user', {'message': 'Hey buddy!'})


Moli.blossom(host='127.0.0.1', port=8013)

