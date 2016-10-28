from moli import event_machine


@event_machine.on('handshake')
def on_handshake_event():
    print('11111111111')


event_machine.emit('handshake', 'hahahahahaha')
