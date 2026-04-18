import socket
import psutil
import time
import platform
import hmac
import hashlib
from cryptography.fernet import Fernet

SERVER_IP = "127.0.0.1" # change to server IP adress for remote systems
SERVER_PORT = 9999

FERNET_KEY = b'LuzztKY-diDjRs5eADRhplwXAvdgfPD7GiO33o1GkxU='
HMAC_SECRET = b'super_secret_key_123'

cipher = Fernet(FERNET_KEY)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

node_name = platform.node()

print("Secure Client started:", node_name)

while True:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    timestamp = str(time.time())

    message = f"{node_name},CPU={cpu},MEM={mem},DISK={disk},TIME={timestamp}"

    encrypted = cipher.encrypt(message.encode())


    signature = hmac.new(
        HMAC_SECRET, encrypted, hashlib.sha256
    ).hexdigest()

    packet = encrypted + b"||" + signature.encode()

    sock.sendto(packet, (SERVER_IP, SERVER_PORT))

    print("Sent secure data")

    time.sleep(5)