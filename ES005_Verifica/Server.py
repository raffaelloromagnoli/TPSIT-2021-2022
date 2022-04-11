import socket as sck
import threading as thr
import sqlite3

guard = {}
rivers={}
clients = []
RECEIVED="Value received!"

class ClientManager(thr.Thread):
    def __init__(self, connection, address, nome):
        thr.Thread.__init__(self)
        self.nome = nome
        self.connection = connection
        self.address = address
        self.running = True

    # OVERRIDE
    def run(self):
        while self.running:
            received = self.connection.recv(4096).decode()
            mssg = received.split(",")
            stationID = int(mssg[0])
            dateNtime = mssg[1]
            level = float(mssg[2])
            river=rivers[stationID]
            dif=level-guard[stationID]
            if dif>0:
                perc=100-(guard[stationID]*100)/level
                if perc<30:
                    self.connection.sendall(RECEIVED.encode())
                elif perc<70:
                    self.connection.sendall(RECEIVED.encode())
                    print(f"Incoming danger on river {river}: level {level}!\n"
                          f"station:{stationID}, time:{dateNtime}")
                else:
                    self.connection.sendall("Turn sirens on, DANGER!".encode())
                    print(f"Current danger on river {river}: level {level}!\n"
                          f"station:{stationID}, time:{dateNtime}")
            else:
                self.connection.sendall(RECEIVED.encode())


def main():

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen()

    con = sqlite3.connect('./fiumi.db')
    cur = con.cursor()

    for row in cur.execute('SELECT id_stazione,livello FROM livelli'):
        guard[row[0]]=row[1]
    for row in cur.execute('SELECT id_stazione, fiume FROM livelli'):
        rivers[row[0]]=row[1]
    con.close()

    while True:
        connection, address = s.accept()
        client = ClientManager(connection, address, len(clients) + 1)
        clients.append(client)
        client.start()


if __name__ == "__main__":
    main()