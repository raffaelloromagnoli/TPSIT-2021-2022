from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import socket

porte={'FTP':[20,21], 'SSH':[22], 'Telnet':[23], 'SMTP':[25], 'DNS':[53],
       'DHCP':[67,68], 'TFTP':[69], 'HTTP':[80], 'HTTPS':[443]}
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def inserisciPorta():
    error = None
    if request.method == 'POST':
        portaminima = int(request.form['portaminima'])
        portamassima = int(request.form['portamassima'])
        website = request.form['website']
        listaporte=scanner(portaminima,portamassima,website)
        inserimentoDB(website,listaporte)
    return render_template('porte.html', error=error)

def scanner(portaminima, portamassima, website):
    n=0
    listaporte=[]
    ip=socket.gethostbyname(website)
    print('cerco')
    for port in range(portaminima, portamassima+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("socket creato")
        result = sock.connect_ex((ip, port))
        print("verifica eseguita")
        if result == 0:

            listaporte.append(port)
            print(f"porta aperta: {listaporte[n]}")
            n+=1
        sock.close()
    return listaporte

def inserimentoDB(website, listaporte):
    con = sqlite3.connect('./porte.db')
    cur = con.cursor()
    print(listaporte)
    for porta in listaporte:
        cur.execute(f"INSERT INTO scansioni (ip, porta) VALUES ('{website}', '{porta}')")
        con.commit()
        con.close()
        print("dati inseriti")


if __name__ == '__main__':
    app.run(debug=True, host='localhost')