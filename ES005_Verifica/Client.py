import socket as sck
import threading
import time
from datetime import datetime

DELAY=15

class Receiver(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True

    def run(self):
        while self.running:
            level=input("River level in meters: ")
            now = datetime.now()

            currentTime = now.strftime("%d/%m/%Y %H:%M:%S")
            self.sock.sendall(f"1,{currentTime},{level}".encode())
            mssg = self.sock.recv(4096).decode()
            print(mssg)

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(("127.0.0.1", 5000))
    rec = Receiver(s)
    rec.start()


if __name__ == "__main__":
    main()