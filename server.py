import socket
import os

# Define a folder for storing uploaded files
UPLOAD_FOLDER = r"E:\uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define server address and port

Ip = socket.gethostbyname(socket.gethostname())
SERVER_ADDRESS = (f'{Ip}', 65432)

def handle_client_connection(client_socket, client_address):
    try:
        # Receive request from the client (text)
        request = client_socket.recv(1024).decode().strip()
        if not request:
            print(f"Empty request from {client_address}")
            return

        parts = request.split(maxsplit=1)
        if len(parts) != 2:
            print(f"Invalid request format from {client_address}: {request}")
            client_socket.sendall(b"ERROR: Invalid request format.")
            return

        command, filename = parts

        if command == "UPLOAD":
            # Receive the file in binary mode and save it to the folder
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, "wb") as f:
                while True:
                    bytes_read = client_socket.recv(4096)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            print(f"File '{filename}' uploaded successfully to '{UPLOAD_FOLDER}'.")

        elif command == "DOWNLOAD":
            # Send the file to the client
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    while True:
                        bytes_read = f.read(4096)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                print(f"File '{filename}' sent successfully.")
            else:
                client_socket.sendall(b"ERROR: File not found.")
                print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen()

        print(f"Server listening on {SERVER_ADDRESS}")
        
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")
                handle_client_connection(client_socket, client_address)
            except socket.error as e:
                print(f"Socket error: {e}")

if __name__ == "__main__":
    start_server()