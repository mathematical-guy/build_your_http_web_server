import platform
import socket  # noqa: F401
from socket import create_server, socket as Socket


class HttpResponseStatusCodes:
    SUCCESSFUL = "HTTP/1.1 200 OK"
    NOT_FOUND = "HTTP/1.1 404 Not Found"


class ResponseConstructor:
    def __init__(self, headers=None, body=None):
        if headers is None:
            self.headers = {"Content-Type": "text/plain"}
        else:
            self.headers = headers

        self.body = body
        self.response = None
        self.status_code = HttpResponseStatusCodes.SUCCESSFUL

    def __append_headers(self):
        headers = ""
        for key, value in self.headers.items():
            headers += f"{key}: {value}\r\n"

        self.response = self.response + "\r\n" + headers

    def __append_body(self):
        self.response = self.response + "\r\n" + self.body

    def __append_status_code(self):
        self.response = self.status_code

    def construct(self) -> str:
        """
        constructs response adding status code, headers and body (if needed)
        :return: str
        """

        self.__append_status_code()
        self.__append_headers()
        if self.body:
            self.__append_body()

        return self.response


class RequestAnalyzer:
    def __init__(self, request: str | bytes):
        self.headers = None
        self.method = None
        self.url_path: str | None = None
        self.response = HttpResponseStatusCodes.SUCCESSFUL

        if isinstance(request, bytes):
            request = request.decode()

        self.request = request

        request_line, *headers = request.split('\r\n')

        self.__analyze_request_line(request_line=request_line)

    def __analyze_request_line(self, request_line: str):
        self.method, self.url_path, http_version = request_line.split(' ')

    def parse_request(self):
        if self.url_path in ["/", "index.html"]:
            self.response = HttpResponseStatusCodes.SUCCESSFUL

        elif 'echo' in self.url_path:
            # HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc
            echo_string: str = self.url_path.split('/')[-1]
            response_constructor = ResponseConstructor(body=echo_string)
            self.response = response_constructor.construct()

        if END_RESPONSE not in self.response:
            self.response += END_RESPONSE

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

    request = client_socket.recv(1024)      # 1024 byte size

    request_analyzer = RequestAnalyzer(request=request)
    response = request_analyzer.parse_request()

    # HTTP version MESSAGE HEADING STATUS CODE  \r\n\r\n
    client_socket.sendall(f"{response}".encode())


if __name__ == "__main__":
    main()
