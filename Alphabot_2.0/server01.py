import socket as sck
import time
from AlphaBot import AlphaBot
import threading as thr

LOCAL_HOST = '0.0.0.0'
N_PORTA = 5001
NUM_MAX_CLIENTI = 1

alphabot = AlphaBot()
comandi_consentiti = {"w": alphabot.avanti, "s": alphabot.indietro, "a": alphabot.sinistra
    , "d": alphabot.destra, "q": alphabot.fermo}
comando_ricevuto = "q"

clients = []


class Client_manager(thr.Thread):
    def __init__(self, connection, address):
        thr.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.running = True

    def run(self):
        while self.running:
            comando = self.connection.recv(4096).decode()
            self.memorizzaComando((comando.split(":"))[1])
            self.inviaMessaggio("Comando eseguito!")

    # invia il messaggio a tutti i client
    def inviaMessaggio(self, msg):
        for client in clients:
            client.connection.sendall(msg.encode())

    # memorizza il comando all'interno di una variabile globale
    def memorizzaComando(self, comando):
        global comando_ricevuto
        if comando in comandi_consentiti.keys():
            comando_ricevuto = comando
            print("Comando cambiato!")
        else:
            print("Comando non esistente")


def main():
    # crea l'oggetto socket e rimane in attesa della connessione con il client
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind((LOCAL_HOST, N_PORTA))
    s.listen(NUM_MAX_CLIENTI)

    # accetta la connessione con il client
    connection, address = s.accept()
    client = Client_manager(connection, address)
    client.start()
    clients.append(client)
    while True:
        # eseguen all'infinito il comando memorizzato nella variabile globale
        comandi_consentiti[comando_ricevuto]()


if __name__ == "__main__":
    main()