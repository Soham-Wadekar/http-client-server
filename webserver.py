import os
import sys
import json
import socket
import mimetypes
from urllib.parse import urlsplit


FILE_PATH = "C:/git-forge/http-client-server/files"


def server(port):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", port))
        s.listen()

        print(f"Listening on port {port}...")

        while True:
            client_socket, client_addr = s.accept()

            with client_socket:
                data = bytearray()

                while b"\r\n\r\n" not in data:
                    chunk = client_socket.recv(4096)

                    if not chunk:
                        break

                    data.extend(chunk)

                if b"\r\n\r\n" not in data:
                    continue

                header_end = data.index(b"\r\n\r\n")
                header_data = data[:header_end]
                request_body = bytearray(data[header_end + 4:])

                header_lines = header_data.decode(
                    "ISO-8859-1"
                ).split("\r\n")

                request_line = header_lines[0].split()

                if len(request_line) != 3:
                    body = b"Bad Request"
                    error_code = "400 Bad Request"
                    file = ""
                    method = ""
                    payload = []
                else:
                    method, path, protocol = request_line

                    content_length = 0

                    try:
                        for line in header_lines[1:]:
                            if line.lower().startswith("content-length:"):
                                content_length = int(
                                    line.split(":", 1)[1].strip()
                                )
                                break

                        if content_length < 0:
                            raise ValueError

                    except ValueError:
                        content_length = -1

                    if content_length == -1:
                        body = b"Bad Request"
                        error_code = "400 Bad Request"
                        file = ""
                        payload = []
                    else:
                        while len(request_body) < content_length:
                            chunk = client_socket.recv(4096)

                            if not chunk:
                                break

                            request_body.extend(chunk)

                        if len(request_body) < content_length:
                            body = b"Bad Request"
                            error_code = "400 Bad Request"
                            file = ""
                            payload = []
                        else:
                            path = urlsplit(path).path
                            file = os.path.split(path)[-1]

                            payload = request_body[
                                :content_length
                            ].decode(
                                "ISO-8859-1"
                            ).splitlines()

                            if file == "":
                                body = b"Thanks for contacting the webserver!"
                                error_code = "200 OK"
                            else:
                                try:
                                    file_path = os.path.join(FILE_PATH, file)

                                    with open(file_path, "rb") as f:
                                        body = f.read()

                                    error_code = "200 OK"

                                except FileNotFoundError:
                                    body = b"File not found"
                                    error_code = "404 Not Found"

                ip, client_port = client_addr

                if file == "":
                    mime_type = "text/plain"
                else:
                    mime_type, encoding = mimetypes.guess_type(file)

                    if mime_type is None:
                        mime_type = "application/octet-stream"

                details = {
                    "ip": ip,
                    "port": client_port,
                    "file": file,
                    "method": method,
                    "payload": payload,
                    "status": error_code,
                    "content_type": mime_type,
                    "content_length": len(body),
                }

                print(json.dumps(details))

                response = (
                    f"HTTP/1.1 {error_code}\r\n".encode("ISO-8859-1")
                    + f"Content-Type: {mime_type}\r\n".encode("ISO-8859-1")
                    + f"Content-Length: {len(body)}\r\n".encode("ISO-8859-1")
                    + b"Connection: close\r\n"
                    + b"\r\n"
                    + body
                )

                client_socket.sendall(response)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Usage: python {sys.argv[0]} [port]")
        sys.exit(1)

    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 28333
    except ValueError:
        print("Port must be an integer.")
        sys.exit(1)

    server(port)
