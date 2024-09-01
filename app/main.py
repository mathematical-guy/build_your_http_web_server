import platform
import socket  # noqa: F401
from socket import create_server, socket as Socket


class HttpResponseStatusCodes:
    SUCCESSFUL = "HTTP/1.1 200 OK"
    NOT_FOUND = "HTTP/1.1 404 Not Found"


class RequestAnalyzer:
    def __init__(self, request: str | bytes):
        self.headers = None
        self.method = None
        self.url_path = None
        self.response = HttpResponseStatusCodes.SUCCESSFUL

        if isinstance(request, bytes):
            request = request.decode()

        self.request = request

        request_line, *headers = request.split('\r\n')

        self.__analyze_request_line(request_line=request_line)

    def __analyze_request_line(self, request_line: str):
        self.method, self.url_path, http_version = request_line.split(' ')

    def parse_request(self):
        if self.url_path not in ["/", "index.html"]:
            self.response = HttpResponseStatusCodes.NOT_FOUND

        return self.response


END_RESPONSE = "\r\n\r\n"


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    _HOST = "localhost"
    _PORT = 4221

    reuse_port = False
    if platform.system() != "Windows":
        reuse_port = True

    server_socket: Socket = create_server(
        address=(_HOST, _PORT),
        reuse_port=reuse_port,
    )

    # wait for client
    client_socket, client_address = server_socket.accept()

    request = client_socket.recv(1024)

    request_analyzer = RequestAnalyzer(request=request)
    response = request_analyzer.parse_request()

    # HTTP version MESSAGE HEADING STATUS CODE  \r\n\r\n
    client_socket.sendall(f"{response}{END_RESPONSE}".encode())


if __name__ == "__main__":
    main()
