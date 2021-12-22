import socket as sock
import sqlite3

sck=sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
sck.bind(('0.0.0.0', 5000))
conn=sqlite3.connect('users.db')
cur=conn.cursor()
#cur.execute('''CREATE TABLE users(nickname text, address text, port real)''')
for row in cur.execute('SELECT * FROM users'):
    print(row)
while True:

    data, addr=sck.recvfrom(4096)
    text=data.decode().split(":")

    if text[0]=="Nickname":
        nick=text[1]
        cur.execute(f"INSERT INTO Users VALUES ('{nick}','{addr[0]}',{addr[1]})")
        print("Nickname saved!")
    else:
        sender=text.decode().split(",")
        nick=sender[0].split(":")
        for row in cur.execute('SELECT * FROM users'):



