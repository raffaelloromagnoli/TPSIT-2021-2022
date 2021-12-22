import socket as sck
import threading

LOCAL_HOST = '192.168.0.123'
N_PORTA = 5001

"""
Questa è la classe che permette la ricezione dei messaggi del server
"""


class Receiver(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True

    def run(self):
        while self.running:
            data = self.sock.recv(4096).decode()
            print(f"Il server dice: {data}")


"""-----------------------------------------------------"""


def main():
    # crea l'oggetto socket
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    # si connette al server e crea il thread per la ricezione dei messaggi
    s.connect((LOCAL_HOST, N_PORTA))  # tupla --> indirizzo ip, porta
    rec = Receiver(s)
    rec.start()

    while True:
        # invia i messaggi al server
        data = input("Scrivi comando:")
        s.sendall((f"Comando:{data}").encode())

    rec.join()


if __name__ == "__main__":
    main()