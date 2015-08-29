from asyncio import start_server
from .async_utils import launch

class Server(object):

    def __init__(self, host, port, protocol):
        self.host = host
        self.port = port
        self.server = None
        self.protocol = protocol()

    def process_request(self, msg):
        return self.protocol.process_request(msg)

    async def connected(self, reader, writer):
        while True:
            data = await reader.read(500)
            try:
                msg = data.decode()
            except UnicodeDecodeError:
                continue

            response, end = self.process_request(msg)

            writer.write(bytes("-> %s\r\n" % response, "utf8"))
            await writer.drain()

            if end:
                break

        writer.close()

    def start(self):
        if not self.server:
            launch(start_server, self.connected,
                   self.host, self.port)

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
