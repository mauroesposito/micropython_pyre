import socket

addr = socket.getaddrinfo('', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    conn.close()
    print("Connection wth %s closed" % str(addr))
