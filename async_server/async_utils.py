from functools import partial
import asyncio


class Loop(object):

    def __init__(self, loop):
        self.loop = loop
        self._coros = []

    def start(self):
        self.loop.run_until_complete(asyncio.wait(self._coros))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def launch(self, f, *a, **k):
        self._coros.append(f(*a, **k))

    def close(self, fs=None):
        if fs:
            self.loop.run_until_complete(asyncio.wait(fs))

        self.loop.close()

_eventloop = asyncio.get_event_loop()
eventloop = Loop(_eventloop)
launch = partial(eventloop.launch)
