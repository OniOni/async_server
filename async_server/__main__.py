from .protocol import JsonProtocol

class MyProtocol(JsonProtocol):

    def hello(self, payload):
        return (('Cheers', payload), False)

    def quit(self, payload):
        return (('Bye', None), True)

    def error(self, payload):
        return (('Error', 'Could not process payload (%s)' % payload),
                False)


def setup():
    from .server import Server
    s = Server('127.0.0.1', 8888, MyProtocol)
    coro = s.start()

    return locals()

def run():
    from .async_utils import eventloop

    setup()
    eventloop.start()

if __name__ == "__main__":
    run()
