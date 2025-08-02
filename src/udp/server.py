import socket
import os
import sys

HOST = (socket.gethostname(), 8080)
chunk = 1024
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(PROJECT_ROOT, "file_server.txt")

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind(HOST)
except socket.error as err:
    print(f"Ошибка, порт занят ({HOST})")
    sys.exit(1)
print("Server starting...")

while True:
    mess, addr = server.recvfrom(chunk)

    if os.path.exists(filename):
        with open(filename, "rb") as file:
            print(f"Connect - {addr[0]}:{addr[1]}")

            data = file.read(chunk)
            while data:
                server.sendto(data, addr)
                data = file.read(chunk)

    else:
        print(f"Ошибка, {filename} не существует")
        sys.exit(1)
