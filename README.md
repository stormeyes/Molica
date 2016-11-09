# moli
A Websocket Server/Client of Python by using async/await which is based on Python3.5+. Deliver your message realtime!

###Note
Moli is still under development and the api might change in future, just take care of this and start play!

###example
+ simple `hello world`
```python
    from moli import Moli, EventMachine


    @EventMachine.on('sayhi')
    def echo(connection):
        EventMachine.emit('echo', {'message': 'Hello world!'}, connection=connection)


    Moli.blossom(host='127.0.0.1', port=8013)
```
