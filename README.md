# HTTP Client and Server

A low-level HTTP client and server implemented in Python using the `socket` API. The project explores network communication, HTTP request-response handling, and TCP sockets without relying on high-level HTTP libraries.

## Project Goals

- Build an HTTP client that connects to a web server, sends HTTP requests, and displays the response.
- Build an HTTP server that listens for incoming connections, receives requests, and returns HTTP responses.
- Understand TCP socket communication, byte encoding, and HTTP message structure.
- Handle partial data received over network connections.

## Components

### 1. HTTP Client — `webclient.py`

A command-line client that connects to a specified host, sends an HTTP GET request, and prints the server's response, including its headers and body.

**Requirements**

- Accept a hostname and an optional port number.
- Default to port `80` when no port is specified.
- Establish connections using Python's `socket` API.
- Send correctly formatted HTTP requests.
- Receive and display the complete HTTP response.
- Close the socket after communication.

### 2. HTTP Server — `webserver.py`

A server that listens for incoming TCP connections, receives HTTP requests, and responds with a predefined HTTP response.

**Requirements**

- Accept an optional port number, defaulting to `28333`.
- Listen for incoming client connections.
- Read incoming requests until the HTTP headers are complete.
- Send a valid HTTP response with headers and a response body.
- Handle multiple connections sequentially.
- Close each client connection after responding.

## Implementation Constraints

- Use Python's built-in `socket` module for network communication.
- Do not use `urllib` or the convenience functions `socket.create_connection()` and `socket.create_server()`.
- Handle socket data as bytes and convert between bytes and strings when necessary.
- Account for partial reads when receiving network data.

## Implementation Progress

- Initialized the Git repository and configured the primary branch as `main`.
- Client and server implementation progress will be documented as the corresponding functionality is completed.

## Running the Project

Start the client:

```bash
python webclient.py example.com
```

Specify a custom client port:

```bash
python webclient.py example.com 8088
```

Start the server:

```bash
python webserver.py
```

Specify a custom server port:

```bash
python webserver.py 12399
```

Once the server is running, connect to it using the client or a web browser at `http://localhost:12399/` when using port `12399`.

## Technologies

- Python 3
- TCP sockets
- HTTP/1.1
