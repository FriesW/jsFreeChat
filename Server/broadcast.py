import asyncio

class _Use:
    def __init__(self, channel):
        self.c = channel
        self.q = asyncio.Queue()
    def __enter__(self):
        self.c.active.append(self.q)
        return self.q
    def __exit__(self, type, value, traceback):
        self.c.active.remove(self.q)

class Channel:
    def __init__(self):
        self.active = []
    def send(self, msg):
        for q in self.active:
            try: q.put_nowait(msg)
            except: pass
    def recv(self):
        return _Use(self)
