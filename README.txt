# Encrypted LED Client/Server Project  

This is a small project I worked on for my CPEG 389 assignment. The idea was to build a **client/server program** in Python where all the communication is **encrypted** using a symmetric key (Fernet from the `cryptography` library). On the server side, I also connected it to a Raspberry Pi so I could control LEDs through GPIO pins.  

Basically:  
- The **server** waits for a client to connect, checks a username + password, and then listens for LED control commands.  
- The **client** takes user input, encrypts it with the shared key, and sends it over the network.  
- All replies from the server are also encrypted.  

---

## Files in this repo  
- `client.py` → the main client program  
- `server.py` → the main server program (with GPIO control for the Pi)  
- `clienttest.py` and `servertest.py` → a lighter “test” version I made just to check that encryption and sockets were working  
- `secret.key` / `symmetric.key` → the shared encryption key (⚠️ this should not be committed, just used locally)  

---

## How to run it  

### 1. Install requirements  
I used Python 3.9+ and the following packages:  
```bash
pip install cryptography RPi.GPIO
```  
(`RPi.GPIO` is only needed if you’re running the server on a Raspberry Pi.)  

### 2. Generate or share a key  
Both client and server need the same symmetric key. I usually generate it on the server and copy it over:  
```bash
from cryptography.fernet import Fernet
key = Fernet.generate_key()
open("symmetric.key", "wb").write(key)
```  
Then put `symmetric.key` next to `client.py` on the client machine.  

### 3. Run the server  
On the Pi:  
```bash
python server.py
```  
It will start listening for connections.  

### 4. Run the client  
On your laptop/desktop:  
```bash
python client.py
```  
It will ask for a username and password (the server checks them), then you can type commands like:  
- `LED 1 ON`  
- `LED 1 OFF`  
- `exit`  

The commands get encrypted before being sent, so everything going across the network is protected.  

---

## Things I’d improve if I had more time  
- Right now the `symmetric.key` file has to be copied manually — I’d like to find a safer way.  
- Error handling is pretty basic, could definitely be cleaned up.  
- Config (host, port, GPIO pins) is hard-coded. Would be nice to pass them as arguments.  
- Server only works on Raspberry Pi at the moment because of `RPi.GPIO`.  

---

## Why I liked this project  
It was fun to see both **networking** and **security** concepts come together. Also cool to actually blink real LEDs with encrypted commands. The test scripts (`clienttest.py` / `servertest.py`) helped me debug before I deployed to the Pi.  
