import sqlite3

PERCORSO = "./"
NON_FARE_NIENTE = "q:0"

con = sqlite3.connect(PERCORSO+"movimenti.db")
cur = con.cursor()

def trovaSequenza(nome_movimento):
    #una  volta letto il comando
    for row in cur.execute('SELECT * FROM movimenti'):
        if nome_movimento == row[0] :
            return row[1]
    print("Il comando non è valido!")
    return NON_FARE_NIENTE

def eseguiComando(comando_da_eseguire):
    lista_comandi = comando_da_eseguire.split(",")
    for comando in lista_comandi:
        dizionario_movimenti[comando.split(":")[0]](comando.split(":")[1])

def eseguiMovimento (nome_movimento):
    if nome_movimento.split(":")[0] in dizionario_movimenti:
        eseguiComando(nome_movimento)
    else:
        eseguiComando(trovaSequenza(nome_movimento))


con.close()
