from .server import WebSocketProtocol
from .event_machine import EventMachine
import asyncio
import logging


class Moli(EventMachine):
    @staticmethod
    def blossom(host='127.0.0.1', port=8080):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(WebSocketProtocol, host, port)
        server = loop.run_until_complete(coro)

        logging.debug('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

