import socket as sock

sck = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
# sck.bind(('192.168.88.67', 5000))
nickname = input("Inserisci il tuo nickname:  ")
hello = "Nickname:" + nickname

sck.sendto(hello.encode(), ('192.168.0.117', 3000))

while True:
    dest = input("Text to:")
    msg = input("Type: ")
    stringa = f"sender:{nickname},receiver:{dest},{msg}"
    sck.sendto(stringa.encode(), ('192.168.0.117', 3000))

    data, addr = sck.recvfrom(4096)
    received = data.decode()
    print("Received: " + received)



