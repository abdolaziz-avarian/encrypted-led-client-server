import socket
import hashlib
from cryptography.fernet import Fernet

# Load the symmetric key from the file
key_file_path = 'symmetric.key'
try:
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
except FileNotFoundError:
    print("Key file not found. Please ensure the key file is present.")
    exit()

cipher_suite = Fernet(key)

# Setup the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = 'insert_ip'  # Replace 'insert_ip' with the actual server IP
port = 8888
try:
    client_socket.connect((server_ip, port))
except Exception as e:
    print(f"Failed to connect to the server {server_ip} on port {port}: {e}")
    exit()

# User input for authentication
username = input("Enter your username: ")
password = input("Enter your passcode: ")

# Password hashing
hashed_password = hashlib.sha256(password.encode()).hexdigest()
auth_message = f"{username}:{hashed_password}"
encrypted_auth_message = cipher_suite.encrypt(auth_message.encode())
client_socket.send(encrypted_auth_message)

# Response of user authentication
response = cipher_suite.decrypt(client_socket.recv(1024)).decode()
if response == "Authentication successful":
    print("Authenticated successfully!")
    while True:
        command = input("Enter command ('LED 1 ON', 'LED 1 OFF', 'LED 2 ON', 'LED 2 OFF', 'LED 3 ON', 'LED 3 OFF', 'exit' to quit): ")
        encrypted_command = cipher_suite.encrypt(command.encode())
        client_socket.send(encrypted_command)

        # Receiving and handling response from the server
        server_response = cipher_suite.decrypt(client_socket.recv(1024)).decode()
        print(server_response)

        if command == 'exit':
            break
else:
    print("Authentication failed.")

client_socket.close()