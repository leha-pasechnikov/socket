import socket
import os
import sys

HOST = (socket.gethostname(), 8080)
len_ind = 6
chunk = 1024 + len_ind + 10
timeout = 1.0
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

try:
    message, addr = client.recvfrom(chunk)
except socket.timeout:
    print("Не удалось получить данные длины файла")
    sys.exit(1)

len_file = int(message)
print(f"длина файла {len_file}")
file_data = [b""] * len_file
client.sendto(b"1", HOST)
while True:
    try:
        message, addr = client.recvfrom(chunk)
        try:
            index = int(message[-len_ind:])
            print(f"Получен пакет {index}")
        except ValueError:
            continue

        if index < len_file:
            file_data[index] = message[:-len_ind]

    except socket.timeout:
        break

with open(filename, "wb") as file:
    for i in file_data:
        file.write(i)

client.close()
