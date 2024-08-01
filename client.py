import socket
import os

# הגדר כתובת ופורט של השרת
Ip = socket.gethostbyname(socket.gethostname())
SERVER_ADDRESS = (f"{Ip}", 65432)

def upload_file(filepath):
    # Check if the file exists
    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist.")
        return

    # Get the filename from the filepath
    filename = os.path.basename(filepath)

    # Create a socket connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(SERVER_ADDRESS)
            sock.sendall(f"UPLOAD {filename}".encode())

            # Open the file and send its contents to the server
            with open(filepath, "rb") as f:
                while True:
                    bytes_read = f.read(4096)
                    if not bytes_read:
                        break
                    sock.sendall(bytes_read)
            print(f"File '{filename}' uploaded successfully.")
        except Exception as e:
            print(f"Error uploading file: {e}")

def download_file(filename):
    # Get the path to the Downloads folder
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Ensure the Downloads directory exists
    os.makedirs(downloads_folder, exist_ok=True)

    # Create the full path for the downloaded file
    download_path = os.path.join(downloads_folder, filename)

    # Create a socket connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(SERVER_ADDRESS)
            sock.sendall(f"DOWNLOAD {filename}".encode())

            # Receive the file data and write it to the local file in the Downloads directory
            with open(download_path, "wb") as f:
                while True:
                    bytes_read = sock.recv(4096)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            print(f"File '{filename}' downloaded successfully to '{download_path}'.")
        except Exception as e:
            print(f"Error downloading file: {e}")

def main():
    while True:
        print("Options:")
        print("1. Upload a file")
        print("2. Download a file - it will be downloaded to the Downloads folder")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            filename = input("Enter the file path to upload: ")
            upload_file(filename)
        elif choice == "2":
            filename = input("Enter the file name to download: ")
            download_file(filename)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()