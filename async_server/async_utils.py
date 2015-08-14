from functools import partial
import asyncio

_eventloop = asyncio.get_event_loop()
_coros = []

def launch(f, *args, **kwargs):
    _coros.append(partial(f, *args, **kwargs)())

class Loop(object):

    def __init__(self, loop):
        self.loop = loop

    def start(self):
        global _coros
        self.loop.run_until_complete(asyncio.wait(_coros))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def close(self, fs=None):
        if fs:
            self.loop.run_until_complete(asyncio.wait(fs))

        self.loop.close()

eventloop = Loop(_eventloop)
