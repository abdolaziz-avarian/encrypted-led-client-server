from cryptography.fernet import Fernet

if __name__ == "__main__":
    key = Fernet.generate_key()
    with open("symmetric.key", "wb") as f:
        f.write(key)
    print("symmetric.key created")
