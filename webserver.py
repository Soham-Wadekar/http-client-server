import sys
import socket

def server(port):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", port))
        s.listen()
        
        print(f"Listening on port {port}...")
        
        while True:
            client_socket, client_addr = s.accept()
            
            with client_socket:
                print(f"Connection from {client_addr}")
                
                data = client_socket.recv(4096)
                print(data.decode("ISO-8859-1"))
                
                body = b"Hello!"
                response = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: text/plain\r\n"
                    + f"Content-Length: {len(body)}\r\n".encode()
                    + b"Connection: close\r\n"
                    + b"\r\n"
                    + body
                )
                
                client_socket.sendall(response)
    
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Usage: python {sys.argv[0]} [port]")
        sys.exit(1)
        
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 28333

    server(port)