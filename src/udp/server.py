import socket
import os
import sys

HOST = (socket.gethostname(), 8080)
LEN_IND = 6  # length of package id
CHUNK = 1024 + LEN_IND
TIMEOUT = 5.0
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(PROJECT_ROOT, "file_server.txt")


def main() -> None:
    """The main function for sending a file by the UDP server"""

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(TIMEOUT)

    try:

        try:
            server.bind(HOST)
        except socket.error:
            print(f"Port is busy {HOST[0]}:{HOST[1]}")
            sys.exit(1)

        print("Server starting...")
        while True:
            try:
                mess, addr = server.recvfrom(CHUNK)
                print(f"Connected to {addr[0]}:{addr[1]}")
            except socket.timeout:
                continue
            except ConnectionResetError:
                print(f'Connection close')
                continue

            print("Start send data")
            if os.path.exists(filename):
                with open(filename, "rb") as file:
                    file_data = []
                    data = file.read(CHUNK)
                    while data:
                        file_data.append(data)
                        data = file.read(CHUNK)

                mess_len = b"0"  # Client message
                attempt = 0  # File size send attempt counter
                while mess_len != b'1':

                    # Sending file size to the client and waiting for confirmation from it
                    server.sendto(str(len(file_data)).encode('utf-8'), addr)
                    try:
                        mess_len, addr = server.recvfrom(CHUNK)
                        attempt += 1
                    except socket.timeout:
                        if attempt < 3:
                            continue
                        else:
                            break
                    except ConnectionResetError:
                        print(f'Connection {addr[0]}:{addr[1]} close')
                        break

                    # After confirmation, the file is sent
                    if mess_len == b"1":
                        for ind, mess in enumerate(file_data):
                            server.sendto(mess + f'{ind:0{LEN_IND}}'.encode('utf-8'), addr)

                    print("Sending is complete")

            else:
                print(f"Error: {filename} does not exist")
                sys.exit(1)
    except Exception as err:
        print(f"Error: {err}")

    finally:
        server.close()
        print("Server close")


if __name__ == "__main__":
    main()
