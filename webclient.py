
import sys
import socket

def client(domain, port=80, method="GET", payload="", content_type="text/plain"):
    body = payload.encode("utf-8")

    with socket.socket() as s:
        print(f"Connecting to {domain} on port {port}...")
        s.connect((domain, port))

        headers = [
            f"{method} / HTTP/1.1",
            f"Host: {domain}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body)}",
            "Connection: close",
            "",
            "",
        ]

        request_data = (
            "\r\n".join(headers).encode("ISO-8859-1") + body
        )

        s.sendall(request_data)

        response = bytearray()
        while True:
            data = s.recv(4096)
            if not data:
                break
            response.extend(data)

        print(response.decode("ISO-8859-1"))

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print(f"Usage: python {sys.argv[0]} <domain> [port] [method] [payload]")
        sys.exit(1)

    domain = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 28333
    method = sys.argv[3].upper() if len(sys.argv) > 3 else "GET"
    payload = sys.argv[4] if len(sys.argv) > 4 else ""

    client(domain, port, method, payload)
