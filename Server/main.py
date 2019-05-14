from sanic import Sanic
from sanic import response
from broadcast import Channel

import asyncio, time

app = Sanic('Main')
room = Channel()


@app.route('/send', methods=['GET', 'POST'])
async def send_post(request):
    if 'msg' in request.form:
        room.send(request.form.get('msg'))
    return await response.file('pages/submit.html')

@app.route('/recv')
async def recv(request):
    async def fn(response):
        await response.write('<html><head></head><body>')
        with room.recv() as r:
            while True:
                msg = await r.get()
                await response.write(msg+'<br>')
    return response.stream(fn, content_type='text/html')

@app.route('/')
async def index(request):
    return await response.file('pages/chat.html')

app.run('0.0.0.0', 8000)
