from asyncio import coroutine, start_server
from .async_utils import launch

from . import protocol

class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    def process_request(self, msg):
        end = False
        p = protocol.unpack(msg)

        response = protocol.JsonProtocol(form='response')
        if p.form == 'echo':
            response.payload = p.payload
        elif p.form == 'close':
            response.payload = "Thanks and bye!"
            end = True
        else:
            response.payload = 'Wut?!?'

        return response, end

    @coroutine
    def connected(self, reader, writer):
        while True:
            data = yield from reader.read(500)
            try:
                msg = data.decode()
            except UnicodeDecodeError:
                continue

            response, end = self.process_request(msg)

            res = protocol.pack(response)
            writer.write(bytes("-> %s\r\n" % res, "utf8"))
            yield from writer.drain()

            if end:
                break

        writer.close()

    def start(self):
        if not self.server:
            launch(start_server, self.connected,
                   self.host, self.port)

    @coroutine
    def stop(self):
        if self.server:
            self.server.close()
            yield from self.server.wait_closed()
