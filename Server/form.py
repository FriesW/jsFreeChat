from sanic import Sanic
from sanic import response

app = Sanic('Main')

@app.route('/', methods=['GET','POST'])
async def handler(request):
    if 'msg' in request.form:
        print(request.form.get('msg'))
    return await response.file('submit.html')

app.run('0.0.0.0',8000)
