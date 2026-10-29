
import sys
import socket

def client(domain, port=80):
    with socket.socket() as s:
        print(f"Connecting to {domain} on port {port}...")
        s.connect((domain, port))

        request_data = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {domain}\r\n"
            f"Connection: close\r\n\r\n"
        ).encode("ISO-8859-1")

        s.sendall(request_data)

        data = s.recv(1024)
        print(data.decode("ISO-8859-1"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <domain> [port]")
        sys.exit(1)

    domain = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80

    client(domain, port)