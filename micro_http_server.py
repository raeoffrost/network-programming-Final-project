import os
import socket


HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 4096
NOT_FOUND_BODY = """<html>
<head><title>404 Not Found</title></head>
<body>
    <h1>404 Not Found</h1>
    <p>The file you requested was not found.</p>
</body>
</html>"""


def main():
    # Get the folder where this script is saved.
    script_directory = os.path.dirname(os.path.abspath(__file__))

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
            request_text = request_data.decode("utf-8", errors="replace")

            print("Raw HTTP request:")
            print(request_text)

            path = "/"

            # Read the first request line and pull out the method and path.
            request_lines = request_text.splitlines()
            if request_lines:
                request_parts = request_lines[0].split()
                if len(request_parts) >= 2:
                    method = request_parts[0]
                    path = request_parts[1]
                    print(f"Method: {method}")
                    print(f"Path: {path}")
                else:
                    print("Invalid or empty request")
            else:
                print("Invalid or empty request")

            # Use the request path to look for a local HTML file.
            if path == "/":
                file_name = "index.html"
            else:
                file_name = path.lstrip("/")

            file_path = os.path.join(script_directory, file_name)

            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    response_body = file.read()
                status_line = "HTTP/1.1 200 OK\r\n"
            else:
                response_body = NOT_FOUND_BODY
                status_line = "HTTP/1.1 404 Not Found\r\n"

            # Send a basic HTTP response with the file contents or 404 page.
            body_bytes = response_body.encode("utf-8")
            response_headers = (
                status_line
                + "Content-Type: text/html; charset=utf-8\r\n"
                + f"Content-Length: {len(body_bytes)}\r\n"
                + "\r\n"
            )
            response = response_headers.encode("utf-8") + body_bytes
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
