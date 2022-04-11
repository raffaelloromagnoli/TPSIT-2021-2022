import socket as sck

sock=sck.socket(sck.AF_INET, sck.SOCK_STREAM)
sock.connect(('162.13.244.64', 80))

REQUEST="GET www.apache.org HTTP/1.1 " \
        "User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)" \
        "Accept-Language: en-us" \
        "Accept-Encoding: gzip, deflate" \
        "Connection: Keep-Alive" \
        ""

sock.sendall(REQUEST.encode())
page=sock.recv(4096).decode()
print(page)