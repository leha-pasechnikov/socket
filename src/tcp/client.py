import socket
import os

HOST = (socket.gethostname(), 10002)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(PROJECT_ROOT, "file_client.txt")
chunk = 1024

try:
    os.remove(filename)
except FileNotFoundError:
    pass

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)
print(f"Connected to {HOST}")

with open(filename, "wb") as file:
    while True:
        message = client.recv(chunk)
        if not message:
            break
        print(message)
        file.write(message)

client.close()

