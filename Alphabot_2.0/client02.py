import socket as sck
import threading

LOCAL_HOST = '192.168.0.123'
N_PORTA = 5001

"""Classe per la ricezione dei messaggi"""
class Receiver(threading.Thread):
    def __init__(self,sock):
        #resta in attesa di messaggi dal client e li stampa
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
    def run(self):
        while self.running:
            data =  self.sock.recv(4096).decode()
            print(f"Il server dice: {data}")
"""---------------------------------------------"""
def main():
    #crea il socket
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

    #si connette al server
    s.connect((LOCAL_HOST, N_PORTA)) # tupla --> indirizzo ip, porta
    rec = Receiver(s)
    #crea un thread per la ricezione dei messaggi
    rec.start()
    while True:
            #invia il comando al server
            data = input("Scrivi comando:")
            s.sendall((f"{data}").encode())

    #chiude il thread di ricezione dei messaggi
    rec.join()
    
if __name__ == "__main__":
    main()
