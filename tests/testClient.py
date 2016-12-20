import asyncio
from moli.client import Client


# c = Client('ws://127.0.0.1:8080')
#
#
# @c.on('data')
# def data_event(connection):
#     print(connection)
#
#
# c.emit('real', {'sssssssssss': 'ee'})
# async def tcp_echo_client(message, loop):
#     reader, writer = await asyncio.open_connection('www.xianguo.com', 80, loop=loop)
#
#     print('Send: %r' % message)
#     writer.write(BAIDU_HEADER.encode())
#
#     while 1:
#         data = await reader.read(1024)
#         if not data: break
#         print(data.decode())
#     # print('Received: %r' % data.decode())
#
#     print('Close the socket')
#     writer.close()
#
# message = 'Hello World!'
# loop = asyncio.get_event_loop()
# loop.run_until_complete(tcp_echo_client(message, loop))
# loop.close()
c = Client('http://127.0.0.1:8013/')


@c.on('data')
def data_event(connection):
    print(connection, 'ww=======')


@c.on('ss')
def user_event(connection):
    print('ss event is trigger')

c.emit('user', 'aaaa')
c.run_forever()
