import socket  # noqa: F401
from socket import create_server, socket as Socket


class HttpResponseStatusCodes:
    SUCCESSFUL = "HTTP/1.1 200 OK"


END_RESPONSE = "\r\n\r\n"


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

    client_socket, client_address = server_socket.accept()      # wait for client
    client_socket.sendall(
        __data=f"{HttpResponseStatusCodes.SUCCESSFUL}{END_RESPONSE}".encode()
    )


if __name__ == "__main__":
    main()
