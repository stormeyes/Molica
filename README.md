# moli
A Websocket Server/Client of Python by using async/await which is based on Python3.5+. Deliver your message realtime!

###Note
Moli is still under development and the api might change in future, just take care of this and start play!

###Example
+ simple `hello world`
```python
    from moli import Moli, EventMachine


    @EventMachine.on('sayhi')
    def echo(connection):
        EventMachine.emit('echo', {'message': 'Hello world!'}, connection=connection)


    Moli.blossom(host='127.0.0.1', port=8013)
```

+ broadcast message to all connect client
```python
    from moli import Moli, EventMachine
    
    @EventMachine.on('broadcast_message')
    def on_handshake_event(connection):
        print(connection.data)
        EventMachine.emit('chat_message', "Hey boys, seems someone join us!", broadcast=True, connection=connection)
     
    Moli.blossom(host='127.0.0.1', port=8013)
```

+ rename connection and send message to specify client(s)
```python
    from moli import Moli, EventMachine
    
    @EventMachine.on('rename')
    def rename(connection):
        connection.name = 'john'
        EventMachine.emit(None, "John wanna to tell you that he loves you", to="Alice", connection=connection)
    
    Moli.blossom(host='127.0.0.1', port=8013)
```

You can read more examples by (example)[!example.py] and (document)[!document.py]