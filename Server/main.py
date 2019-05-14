from sanic import Sanic
from sanic import response

import asyncio, time

app = Sanic('Main')

@app.route('/send', methods=['GET', 'POST'])
async def send_post(request):
    if 'msg' in request.form:
        print(request.form.get('msg'))
    return await response.file('pages/submit.html')

@app.route('/recv')
async def recv(request):
    async def fn(response):
        await response.write('<html><head></head><body>')
        try:
            while True:
                await response.write(str(time.time())+'<br>')
                await asyncio.sleep(1)
        except:
            print('Error')
    return response.stream(fn, content_type='text/html')

@app.route('/')
async def index(request):
    return await response.file('pages/chat.html')

app.run('0.0.0.0', 8000)
