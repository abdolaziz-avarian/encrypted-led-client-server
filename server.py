import socket
import hashlib
from cryptography.fernet import Fernet
import RPi.GPIO as GPIO

# Setting up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# Loading symmetric encryption key
key_file_path = 'symmetric.key'
try:
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
except FileNotFoundError:
    print("Key file not found. Please ensure the key file is present.")
    exit()

cipher_suite = Fernet(key)

# Username and hashed password storage
user_passwords = {
    "aziz": hashlib.sha256("avarian".encode()).hexdigest()
}

# Setting up socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8888))
server_socket.listen(1)

print("Server is listening for clients...")

while True:
    client, addr = server_socket.accept()
    print("A client has been connected:", addr)

    # Authenticating user
    data = client.recv(1024)
    decrypted_message = cipher_suite.decrypt(data).decode()
    username, received_hash = decrypted_message.split(':')

    # Authenticating username and passcode
    if username in user_passwords and user_passwords[username] == received_hash:
        client.send(cipher_suite.encrypt("Authentication successful".encode()))
        print("User has been authenticated. Type your commands.")
        while True:
            try:
                command = cipher_suite.decrypt(client.recv(1024)).decode()
                if command == "LED 1 ON":
                    GPIO.output(18, GPIO.HIGH)
                    response = "LED 1 is ON"
                elif command == "LED 1 OFF":
                    GPIO.output(18, GPIO.LOW)
                    response = "LED 1 is OFF"
                elif command == "LED 2 ON":
                    GPIO.output(23, GPIO.HIGH)
                    response = "LED 2 is ON"
                elif command == "LED 2 OFF":
                    GPIO.output(23, GPIO.LOW)
                    response = "LED 2 is OFF"
                elif command == "LED 3 ON":
                    GPIO.output(24, GPIO.HIGH)
                    response = "LED 3 is ON"
                elif command == "LED 3 OFF":
                    GPIO.output(24, GPIO.LOW)
                    response = "LED 3 is OFF"
                elif command == "exit":
                    response = "Exiting"
                    break
                else:
                    response = "Unrecognized command"
                client.send(cipher_suite.encrypt(response.encode()))
            except Exception as e:
                print("Error handling command:", e)
                break
    else:
        client.send(cipher_suite.encrypt("Authentication Failed".encode()))
        print("Authentication has failed.")

    client.close()

server_socket.close()
GPIO.cleanup()