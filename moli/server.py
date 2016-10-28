"""
server create socket and make connection on each websocket client connect
"""
try:
    import uvloop as asyncio
except ImportError:
    import asyncio


class HttpProtocol
