import socket as sck
import threading as thr
import sqlite3

database = {}
clients = []


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

            for op in database[self.nome]:
                self.connection.sendall(op.encode())
                receive = self.connection.recv(4096).decode()

                # print (f"{operazione} = {risultato} from {client_ip} - {client_port}")
                print(f"{op} = {receive} from {self.address[0]} - {self.address[1]}")

            self.connection.sendall("exit".encode())
            self.running = False
            self.connection.close()


def main():
    global database

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen()

    con = sqlite3.connect('./operations.db')
    cur = con.cursor()

    for row in cur.execute('SELECT * FROM operations'):
        if row[1] in database:
            database[row[1]].append(row[2])
        else:
            database[row[1]] = [row[2]]

    con.close()

    while True:
        connection, address = s.accept()
        client = ClientManager(connection, address, len(clients) + 1)
        clients.append(client)
        client.start()


if __name__ == "__main__":
    main()