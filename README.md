# Secure UDP System Monitor

A lightweight client-server system that monitors system metrics and transmits them securely over UDP.

## Features
- Collects CPU, memory, and disk usage
- Sends data using UDP sockets
- Encrypts messages using Fernet (cryptography)
- Ensures data integrity using HMAC (SHA-256)
- Detects tampered or replayed packets
- Supports multiple clients

## Tech Stack
- Python
- UDP sockets
- cryptography (Fernet)
- hmac, hashlib
- psutil

## File Structure
- client.py: collects system metrics and sends encrypted data
- server.py: receives, verifies, decrypts, and processes data
- crypto_utils.py: handles encryption and authentication logic (if used)

## How It Works
- The client collects system metrics periodically
- Data is encrypted using Fernet
- A HMAC signature is generated for integrity
- The packet is sent to the server via UDP
- The server verifies the signature and decrypts the data
- Metrics are processed and alerts are generated if thresholds are exceeded

## Run

### Start Server
python server.py

### Start Client
python client.py

## Notes
- Default client IP is set to 127.0.0.1 for local testing
- Update the server IP in client.py to monitor remote systems
- In production, encryption keys and secrets should be stored securely