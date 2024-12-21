import os
import socket
import json
import hmac
import hashlib
import threading
import time

from dotenv import load_dotenv

load_dotenv()

UDP_ADDRESS = os.getenv("UDP_ADDRESS")
UDP_PORT = int(os.getenv("UDP_PORT"))

SERVER_ADDRESS = (UDP_ADDRESS, UDP_PORT)
BUFFER_SIZE = 1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def calculate_hmac(contents, token):
    hmac_result = hmac.new(token.encode('utf-8'), contents.encode('utf-8'), hashlib.sha256)
    return hmac_result.hexdigest()


def send_hello_message(user_id, token):
    contents = "Hello!"
    message = {
        "userId": str(user_id),
        "event": "hello",
        "contents": contents,
        "hmac": calculate_hmac(json.dumps(contents), token)
    }
    client_socket.sendto(json.dumps(message).encode(), SERVER_ADDRESS)


def handle_hello(user_id, token):
    while True:
        send_hello_message(user_id, token)
        time.sleep(1)  # 1 Hz updates


def initialize_client(user_id, token):
    hello_thread = threading.Thread(target=handle_hello, daemon=True, args=(user_id, token))
    hello_thread.start()
