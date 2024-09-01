import socket  # noqa: F401
from socket import create_server, socket as Socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    _HOST = "localhost"
    _PORT = 4221

    # Uncomment this to pass the first stage
    #
    server_socket: Socket = create_server(
        address=(_HOST, _PORT),
        reuse_port=True,
    )

    server_socket.accept()      # wait for client


if __name__ == "__main__":
    main()
