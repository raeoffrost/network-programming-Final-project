import socket


HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 4096
HTML_BODY = """<html>
<head><title>My Micro Server</title></head>
<body>
    <h1>It works!</h1>
    <p>This is a basic response from my Python socket server.</p>
</body>
</html>"""


def main():
    # Create a TCP socket for the server.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to localhost on port 8080.
    server_socket.bind((HOST, PORT))

    # Start listening for incoming client connections.
    server_socket.listen(1)

    print(f"Server listening on {HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")

    try:
        while True:
            # Wait for one client to connect.
            client_socket, client_address = server_socket.accept()
            print(f"\nConnection received from {client_address}")

            # Receive the request data from the client.
            request_data = client_socket.recv(BUFFER_SIZE)

            print("Raw HTTP request:")
            print(request_data.decode("utf-8", errors="replace"))

            # Send a basic HTTP response with a simple HTML page.
            body_bytes = HTML_BODY.encode("utf-8")
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(body_bytes)}\r\n"
                "\r\n"
            ).encode("utf-8") + body_bytes
            client_socket.sendall(response)

            # Close the client connection after sending the response.
            client_socket.close()
            print("Client connection closed.")

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    finally:
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    main()
