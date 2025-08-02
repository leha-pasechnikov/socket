import socket
import os

HOST = (socket.gethostname(), 8080)
chunk = 1024
timeout = 5.0
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(PROJECT_ROOT, "file_client.txt")

try:
    os.remove(filename)
except FileNotFoundError:
    pass

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(timeout)

client.sendto(b"Hello", HOST)
print(f"Send to {HOST}")

with open(filename, "wb") as file:
    while True:
        try:
            message, addr = client.recvfrom(chunk)
        except socket.timeout:
            break
        file.write(message)

client.close()