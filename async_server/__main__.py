def setup():
    from .server import Server
    s = Server('127.0.0.1', 8888)
    coro = s.start()

    return locals()

def run():
    from .async_utils import eventloop

    setup()
    eventloop.start()

if __name__ == "__main__":
    run()
