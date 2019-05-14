from sanic import Sanic
from sanic import response
from broadcast import Channel
import asyncio
import time

with open('pages/submit.html') as f:
    html_submit = f.read()
with open('pages/log.html') as f:
    html_log = f.read()
with open('pages/room.html') as f:
    html_room = f.read()


app = Sanic('Main')
room = Channel()


@app.route('/send', methods=['GET'])
def send_get(request):
    return response.html(html_submit)

@app.route('/send', methods=['POST'])
def send_post(request):
    if 'msg' in request.form:
        room.send(request.form.get('msg'))
    return response.redirect('/send')

@app.route('/recv')
async def recv(request):

    async def ka(response):
        start = time.monotonic()
        while True:
            elapsed = int(time.monotonic() - start) + 15
            await response.write('<style>#disconnect{{animation: fadein {}s steps(1, end);}}</style>'.format(elapsed))
            await asyncio.sleep(5)

    async def ms(response):
        with room.recv() as r:
            while True:
                msg = await r.get()
                await response.write('<div class="msg">'+msg+'</div>')

    async def fn(response):
        await response.write(html_log)
        t1 = asyncio.create_task(ka(response))
        t2 = asyncio.create_task(ms(response))
        await t1
        await t2
    return response.stream(fn, content_type='text/html')

@app.route('/')
def index(request):
    return response.html(html_room)

app.run('0.0.0.0', 8000)
