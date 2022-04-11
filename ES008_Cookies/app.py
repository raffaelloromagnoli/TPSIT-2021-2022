from re import U
from flask import Flask, render_template, make_response,request



app = Flask(__name__)

@app.route('/')
def index():
    #leggere il cookie
    username = request.cookies.get('username')
    if username==None:
        print('Nuovo utente')
        resp = make_response(render_template('index.html'))
        resp.set_cookie('username', 'nuovoutente')
    elif username=="johndoe":
        resp = make_response(render_template('indexjd.html'))
        resp.set_cookie('username', 'johndoe')
    elif username=="utentegenerico":
        resp = make_response(render_template('indexug.html'))
        resp.set_cookie('username', 'utentegenerico')
    else:
        #settare il cookie
        resp = make_response(render_template('index.html'))
        resp.set_cookie('username', 'utentegenerico')
    return resp

@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='localhost')