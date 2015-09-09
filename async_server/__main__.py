from .protocol import TextProtocol, response

class MyProtocol(object):

    def do_hello(self, payload):
        return response('Cheers', payload)

    def do_quit(self, payload):
        return response('Bye', None, end=True)

    def do_error(self, payload):
        return response('Error', 'Could not process payload (%s)' % payload)

class MyTextProtocol(MyProtocol, TextProtocol):
    pass

def setup():
    from .server import Server
    s = Server('127.0.0.1', 8888, MyTextProtocol)
    coro = s.start()

    return locals()

def run():
    from .async_utils import eventloop

    setup()
    eventloop.start()

if __name__ == "__main__":
    run()
