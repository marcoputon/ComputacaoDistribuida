from bottle import Bottle, run, template, route, get, post, request, redirect

app = Bottle()
history = []

    
@app.get('/cliente') # or @route('/login')
def login():
	global history

	a = '''
        <form action="/servidor" method="post">
            Username: <input name="username" type="text" />
            text: <input name="text" type="text" />
            <input value="Send" type="submit" />
        </form>
    '''
		
	for i in history:
		a += i[0] + ": " + i[1] + "<br>"
		
	return a


@app.post('/servidor') # or @route('/login', method='POST')
def do_login():
	t = request.forms.get('text')
	u = request.forms.get('username')
	
	history.append([u, t])
	redirect("/cliente")

run(app, host='localhost', port=8080)
