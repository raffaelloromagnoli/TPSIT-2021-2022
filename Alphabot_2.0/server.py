import socket as sck
import time
from AlphaBot import AlphaBot
import threading as thr
import sqlite3

PERCORSO = "/home/pi/server1/"
NON_FARE_NIENTE = "q:0"

LOCAL_HOST = '0.0.0.0'
N_PORTA = 5001
NUM_MAX_CLIENTI = 1

# creaates alphabot object
alphabot = AlphaBot()
comandi_consentiti = {"w": alphabot.avanti_t, "s": alphabot.indietro_t, "d": alphabot.sinistra_t
    , "a": alphabot.destra_t, "q": alphabot.fermo}

clients = []


class Client_manager(thr.Thread):
    def __init__(self, connection, address):
        thr.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.running = True
        self.messaggio_di_ritorno = ""

    def run(self):
        while self.running:
            # Resta in attesa di ricevere un comando e lo memorizza nella varaibile
            comando = self.connection.recv(4096).decode()
            # esegue il movimento
            self.eseguiMovimento(comando)
            # invia al client l'esito del comando
            self.inviaMessaggio(self.messaggio_di_ritorno)

    """Cerca se il messaggio che ha inviato il client è il nome di una sequenza,
        nel caso contrario invia un messaggio di errore e non fa niente"""

    def trovaSequenza(self, nome_movimento):
        # apre la connessione con il database e crea il cursore
        con = sqlite3.connect(PERCORSO + "movimenti.db")
        cur = con.cursor()
        # verifica che il movimento sia all'interno del database
        for row in cur.execute('SELECT * FROM movimenti'):
            if nome_movimento == row[0]:
                con.close()
                return row[1]
        print("Il comando non è valido!")
        con.close()
        self.messaggio_di_ritorno = "comando non valido!"
        return NON_FARE_NIENTE

    """--------------------------------------------------------------------"""

    """Esegue la lista di comandi"""

    def eseguiComando(self, comando_da_eseguire):
        lista_comandi = comando_da_eseguire.split(",")
        for comando in lista_comandi:
            comandi_consentiti[comando.split(":")[0]](float(comando.split(":")[1]))

    """--------------------------------------------------------------------"""

    """Verifica se il movimento è 'diretto' o se è il nome di una sequenza"""

    def eseguiMovimento(self, nome_movimento):
        self.messaggio_di_ritorno = "comando eseguito!"
        if nome_movimento.split(":")[0] in comandi_consentiti:
            self.eseguiComando(nome_movimento)
        else:
            self.eseguiComando(self.trovaSequenza(nome_movimento))

    """--------------------------------------------------------------------"""

    """Invia il messaggio a tutti i client"""

    def inviaMessaggio(self, msg):
        for client in clients:
            client.connection.sendall(msg.encode())

    """--------------------------------------------------------------------"""


def main():
    # crea l'oggetto socket e lo mette in attesa di connessioni
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind((LOCAL_HOST, N_PORTA))
    s.listen(NUM_MAX_CLIENTI)
    while True:
        # accetta la connessione del server e crea un thread per ricevere i suoi messaggi
        connection, address = s.accept()
        client = Client_manager(connection, address)
        client.start()
        clients.append(client)


if __name__ == "__main__":
    main()

