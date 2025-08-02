import socket
import os
import sys

HOST = (socket.gethostname(), 10002)
max_turn = 10
chunk = 1024
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(PROJECT_ROOT, "file_server.txt")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server.bind(HOST)
except socket.error as err:
    sys.exit(1)

server.listen(max_turn)
print("Server starting...")


while True:
    conn, addr = server.accept()

    if os.path.exists(filename):
        with open(filename, "rb") as file:
            print(f"Connected - {addr[0]}:{addr[1]}")

            data = file.read(chunk)
            while data:
                conn.sendall(data)
                data = file.read(chunk)

            conn.close()
    else:
        print(f"Ошибка, {filename} не существует")
        sys.exit(1)



