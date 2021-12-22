from flask import Flask, render_template, request
from Alphabot import AlphaBot

app = Flask(__name__)
alphabot = AlphaBot()

comandi_consentiti =  {"w":alphabot.avanti, "s":alphabot.indietro, "a": alphabot.sinistra
        ,"d":alphabot.destra, "q":alphabot.fermo}


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comando_ricevuto = "q"
        if request.form.get('avanti') == 'avanti':
            comando_ricevuto = "w"
            print("l'Alphabot va avanti")
        elif  request.form.get('indietro') == 'indietro':
            comando_ricevuto = "s"
            print("l'Alphabot va indietro")
        elif  request.form.get('sinistra') == 'sinistra':
            comando_ricevuto = "a"
            print("l'Alphabot va sinistra")
        elif  request.form.get('destra') == 'destra':
            comando_ricevuto = "d"
            print("l'Alphabot va destra")
        elif  request.form.get('fermo') == 'fermo':
            print("l'Alphabot è fermo")
        else:
            print("Unknown")
        comandi_consentiti[comando_ricevuto]()
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='localhost')