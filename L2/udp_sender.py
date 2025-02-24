import socket
import time

# Completati cu adresa IP a platformei ESP32
PEER_IP = "192.168.89.50"
PEER_PORT = 10001

MESSAGE = b"GPIO4="
i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    try:
        TO_SEND = MESSAGE + bytes(str(0),"ascii")
        sock.sendto(TO_SEND, (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", TO_SEND)
        time.sleep(1)
        TO_SEND = MESSAGE + bytes(str(1),"ascii")
        sock.sendto(TO_SEND, (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", TO_SEND)
        time.sleep(1)
    except KeyboardInterrupt:
        break