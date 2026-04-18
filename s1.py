import socket
import time
import hmac
import hashlib
from cryptography.fernet import Fernet

SERVER_IP = "0.0.0.0"
SERVER_PORT = 9999

CPU_THRESHOLD = 80
MEM_THRESHOLD = 80
DISK_THRESHOLD = 90

FERNET_KEY = b'LuzztKY-diDjRs5eADRhplwXAvdgfPD7GiO33o1GkxU='
HMAC_SECRET = b'super_secret_key_123'
#NOTE In production, store keys securely (env variables or config files)
cipher = Fernet(FERNET_KEY)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("Secure Monitoring Server Running on port", SERVER_PORT)

client_metrics = {}

while True:
    data, addr = sock.recvfrom(4096)

    try:

        encrypted, recv_signature = data.split(b"||")


        calc_signature = hmac.new(
            HMAC_SECRET, encrypted, hashlib.sha256
        ).hexdigest().encode()

        if not hmac.compare_digest(recv_signature, calc_signature):
            print("Tampered packet from", addr)
            continue


        message = cipher.decrypt(encrypted).decode()

        parts = message.split(",")

        node = parts[0]
        cpu = float(parts[1].split("=")[1])
        mem = float(parts[2].split("=")[1])
        disk = float(parts[3].split("=")[1])
        timestamp = float(parts[4].split("=")[1])


        if time.time() - timestamp > 10:
            print("Old packet from", node)
            continue

        client_metrics[node] = {
            "cpu": cpu,
            "mem": mem,
            "disk": disk,
            "last_update": time.time()
        }

        print(f"""
        Node: {node}
        CPU: {cpu}%
        Memory: {mem}%
        Disk: {disk}%
        """)


        if cpu > CPU_THRESHOLD:
            print(f"ALERT: {node} CPU high: {cpu}%")

        if mem > MEM_THRESHOLD:
            print(f"ALERT: {node} Memory high: {mem}%")

        if disk > DISK_THRESHOLD:
            print(f"ALERT: {node} Disk high: {disk}%")

    except Exception as e:
        print("Invalid packet received")


    print("\n--- Aggregated Metrics ---")
    for client, metrics in client_metrics.items():
        print(client, metrics)