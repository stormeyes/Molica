from moli.client import Client


c = Client('http://127.0.0.1:8013/')


@c.on('ss')
def user_event(connection):
    pass
    #print('ss event is trigger', connection)


c.emit('mybaby', 'aaaa')
c.run_forever()
