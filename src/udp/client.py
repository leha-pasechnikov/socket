import socket
import os
import sys

HOST = (socket.gethostname(), 8080)
LEN_IND = 6  # length of package id
CHUNK = 1024 + LEN_IND + 10
TIMEOUT = 1.0
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(PROJECT_ROOT, "file_client.txt")


def main() -> None:
    """The main function for receiving a file by the UDP client"""

    try:
        os.remove(FILENAME)
    except FileNotFoundError:
        pass

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(TIMEOUT)

    try:
        client.sendto(b"Hello", HOST)
        print(f"Connected to {HOST[0]}:{HOST[1]}")

        try:
            message, addr = client.recvfrom(CHUNK)
        except socket.timeout:
            print("Error: could not get the file length")
            sys.exit(1)

        len_file = int(message)
        file_data = [b""] * len_file
        client.sendto(b"1", HOST)
        while True:
            try:
                message, addr = client.recvfrom(CHUNK)
                try:
                    index = int(message[-LEN_IND:])
                except ValueError:
                    continue

                if 0 <= index < len_file:
                    file_data[index] = message[:-LEN_IND]

            except socket.timeout:
                break

        with open(FILENAME, "wb") as file:
            for i in file_data:
                file.write(i)
    except Exception as err:
        print(f"Error: {err}")
    finally:
        client.close()
        print("Connection close")


if __name__ == "__main__":
    main()
