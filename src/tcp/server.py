import socket
import os
import sys

HOST = (socket.gethostname(), 10002)
MAX_TURN = 10  # Maximum number of connections
CHUNK = 1024
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(PROJECT_ROOT, "file_server.txt")


def main() -> None:
    """The main function for sending a file by the TCP server"""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        try:
            server.bind(HOST)
        except socket.error:
            print(f"Port is busy {HOST[0]}:{HOST[1]}")
            sys.exit(1)

        server.listen(MAX_TURN)
        print("Server starting...")

        while True:
            conn, addr = server.accept()

            if os.path.exists(FILENAME):
                with open(FILENAME, "rb") as file:
                    print(f"Connected to {addr[0]}:{addr[1]}")

                    data = file.read(CHUNK)
                    while data:
                        conn.sendall(data)
                        data = file.read(CHUNK)
                    conn.close()
                    print(f"Connection {addr[0]}:{addr[1]} close")
            else:
                print(f"Error: {FILENAME} does not exist")
                sys.exit(1)
    except Exception as err:
        print('Error: ' + str(err))

    finally:
        server.close()
        print("Server close")


if __name__ == "__main__":
    main()
