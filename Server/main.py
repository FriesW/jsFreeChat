from sanic import Sanic
from sanic import response
from broadcast import Channel

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
    async def fn(response):
        await response.write(html_log)
        with room.recv() as r:
            while True:
                msg = await r.get()
                await response.write(msg+'<br>')
    return response.stream(fn, content_type='text/html')

@app.route('/')
def index(request):
    return response.html(html_room)

app.run('0.0.0.0', 8000)
