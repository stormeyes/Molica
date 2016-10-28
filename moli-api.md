server side:
```python
import moli


@moli.on('connect')
def on_connect_client(io):
    io.id
    moli.emit(event='welcome', message='Hey guys!', to='adsasxe331ds', toRoom=[], broadcast=True)


moli.blossom(host='0.0.0.0', port='8080')
```
client side:
```python
import moli

moli.connect('ws://127.0.0.1:8080')
# simple emit
moli.emit('cheer', 'Nice to see you')
# broadcast to all connection
moli.emit('cheer', 'Nice to see all of you', broadcast=True)
```
+ EventMachine style
+ user-defined named connection to reconginze
+ user-defined data parse and dispatch rules
+ broadcast/single/group
+ fit for socket.io
+ Server/Client suit
+ build with saint
+ client reconnect
+ each connection has an id which dispath by moli, and you can't change the id to your defind. I recommand you can manual the connection list and mapper by yourself
+ sessionid generator

delive your realtime message has never been so easy!
默认所有emit和on事件都是针对当前你的这条IO来说的! 因此这些事件的对象只有你
