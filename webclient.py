import sys
import socket


def client(
    domain, port=80, file="", method="GET", payload="", content_type="text/plain"
):
    body = payload.encode("utf-8")

    with socket.socket() as s:
        s.settimeout(10)

        print(f"Connecting to {domain} on port {port}...")
        s.connect((domain, port))

        headers = [
            f"{method} /{file} HTTP/1.1",
            f"Host: {domain}:{port}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body)}",
            "Connection: close",
            "",
            "",
        ]

        request_data = "\r\n".join(headers).encode("ISO-8859-1") + body

        s.sendall(request_data)

        response = bytearray()

        while True:
            try:
                data = s.recv(4096)
            except socket.timeout:
                print("Connection timed out.")
                return

            if not data:
                break

            response.extend(data)

        if b"\r\n\r\n" not in response:
            print("Invalid HTTP response received.")
            return

        header_end = response.index(b"\r\n\r\n")

        response_headers = response[:header_end]
        response_body = response[header_end + 4:]

        response_headers = response_headers.decode("ISO-8859-1")

        print("\n" + response_headers)

        response_type = ""

        for line in response_headers.split("\r\n"):
            if line.lower().startswith("content-type:"):
                response_type = line.split(":", 1)[1].strip().lower()
                break

        if (
            response_type.startswith("text/")
            or "json" in response_type
            or "xml" in response_type
        ):
            print("\n" + response_body.decode("utf-8", errors="replace"))
        else:
            print(
                f"\nBinary response received ({len(response_body)} bytes)"
            )


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 6:
        print(f"Usage: python {sys.argv[0]} <domain> [port] [file] [method] [payload]")
        sys.exit(1)

    domain = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 28333
    file = sys.argv[3] if len(sys.argv) > 3 else ""
    method = sys.argv[4].upper() if len(sys.argv) > 4 else "GET"
    payload = sys.argv[5] if len(sys.argv) > 5 else ""

    client(domain, port, file, method, payload)
