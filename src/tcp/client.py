import socket
import os

HOST = (socket.gethostname(), 10002)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(PROJECT_ROOT, "file_client.txt")
CHUNK = 1024


def main() -> None:
    """The main function for receiving a file by the TCP client"""

    # удаление старого файла
    try:
        os.remove(FILENAME)
    except FileNotFoundError:
        pass

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(HOST)
        print(f"Connected to {HOST[0]}:{HOST[1]}")

        with open(FILENAME, "wb") as file:
            while True:
                message = client.recv(CHUNK)
                if not message:
                    break
                file.write(message)
    except Exception as err:
        print(f"Error: {err}")
    finally:
        client.close()
        print("Connection close")


if __name__ == "__main__":
    main()
