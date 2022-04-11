from flask import Flask, render_template, request, redirect, url_for,make_response
import random
import string
import sqlite3
import datetime

app = Flask(__name__)
token = ''.join(random.choices(string.ascii_uppercase +
                               string.digits, k=15))

def validate(username, password):
    completion = False
    con = sqlite3.connect('./social.db')
    cur = con.cursor()
    #verifica utente in DB
    cur.execute("SELECT * FROM Utenti")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser == username:
            completion = check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])
def login():
    #pagina di login, da erorre a credenziali errate
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            resp = make_response(redirect(url_for('randomSocial')))
            resp.set_cookie('username', username)
            return resp
    return render_template('login.html', error=error)

@app.route(f'/{token}', methods=['GET', 'POST']) #token diverso ad ogni accessso
def randomSocial():
    error = None
    posted=None
    #recupero user attuale dal cookie settato nel login
    user = str(request.cookies.get('username'))
    rUser=user
    while rUser==user: #verifica utente post casuale diverso da attuale
        randomUP=choosePost()
        rUser=randomUP[0]
        rPost=randomUP[1]
    if request.method == 'POST':
        post = request.form['post']
        if post == '': #verifica stinga vuota
            error = 'Scrivi qualcosa!'
        else:
            posted='Pubblicato' #comferma pubblicazione
            inserimentoDB(user, post)
    elif request.method == 'GET':
        return render_template('index.html', postUser=rUser, randomPost=rPost, user=user)
    return render_template("index.html", error=error, postUser=rUser,
                           randomPost=rPost, user=user, posted=posted)

def choosePost():
    con = sqlite3.connect('./social.db')
    cur = con.cursor()
    #selezione riga casuale da tabellastati
    cur.execute(f"SELECT * FROM Stati ORDER BY RANDOM() LIMIT 1;")
    randomUP= cur.fetchall()
    for row in randomUP:
        postUser = row[1]
        randomPost = row[2]
    con.close()
    UP=[postUser,randomPost]
    return UP


def inserimentoDB(user, post):
    print('inserisco nel db')
    #inserimento azione nel db attraverso cookies
    ora=datetime.datetime.now()
    con = sqlite3.connect('./social.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO Stati (user, post, dataora)"
                f" VALUES ('{user}','{post}','{ora}')")
    con.commit()
    con.close()
    print("dati inseriti")



if __name__ == '__main__':
    app.run(debug=True, host='localhost')