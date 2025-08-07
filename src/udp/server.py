import socket
import os
import sys

HOST = (socket.gethostname(), 8080)
len_ind = 6
chunk = 1024 + len_ind
timeout = 5.0
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(PROJECT_ROOT, "file_server.txt")

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.settimeout(timeout)

try:
    server.bind(HOST)
except socket.error as err:
    print(f"Ошибка, порт занят ({HOST})")
    sys.exit(1)
print("Server starting...")

while True:
    try:
        mess, addr = server.recvfrom(chunk)
    except socket.timeout:
        continue
    except ConnectionResetError:
        print(f'{addr[0]}:{addr[1]} Разорвал подключение')
        continue

    print("Началась передача файла")

    if os.path.exists(filename):
        with open(filename, "rb") as file:
            file_data = []
            data = file.read(chunk)
            while data:
                file_data.append(data)
                data = file.read(chunk)

        mess_len = b"0"
        attempt = 0
        while mess_len != b'1':
            server.sendto(str(len(file_data)).encode('utf-8'), addr)

            try:
                mess_len, addr = server.recvfrom(chunk)
                attempt += 1
            except socket.timeout:
                if attempt < 3:
                    continue
                else:
                    break
            except ConnectionResetError:
                print(f'{addr[0]}:{addr[1]} Разорвал подключение')
                break

            if mess_len == b"1":
                for ind, mess in enumerate(file_data):
                    server.sendto(mess + f'{ind:0{len_ind}}'.encode('utf-8'), addr)
                    print(f"Отправлен {ind} пакет")
            print("Отправка завершена")

    else:
        print(f"Ошибка, {filename} не существует")
        sys.exit(1)
