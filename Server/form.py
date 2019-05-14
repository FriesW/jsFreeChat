from sanic import Sanic
from sanic import response

app = Sanic('Main')

@app.route('/', methods=['GET'])
async def handler(request):
    return await response.file('submit.html')

@app.route('/', methods=['POST'])
async def p_handler(request):
    if 'msg' in request.form:
        print(request.form.get('msg'))
    return response.redirect('/')

app.run('0.0.0.0',8000)
