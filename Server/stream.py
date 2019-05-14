from sanic import Sanic
from sanic.response import stream
import asyncio
import time

app = Sanic('Main')

@app.route('/')
async def slow_load(request):
    async def fn(response):
        await response.write('<html><head></head><body>')
        try:
            while True:
                await response.write(str(time.time())+'<br>')
                await asyncio.sleep(1)
        except:
            print('Error')

    return stream(fn, content_type='text/html')

app.run('0.0.0.0',8000)
