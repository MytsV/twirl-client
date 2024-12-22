import os
import socket
import json
import hmac
import hashlib
import threading
import time

from dotenv import load_dotenv
from pydantic import ValidationError

from models import GameState

load_dotenv()

UDP_ADDRESS = os.getenv("UDP_ADDRESS")
UDP_PORT = int(os.getenv("UDP_PORT"))

SERVER_ADDRESS = (UDP_ADDRESS, UDP_PORT)
BUFFER_SIZE = 1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def calculate_hmac(contents, token):
    hmac_result = hmac.new(
        token.encode("utf-8"), contents.encode("utf-8"), hashlib.sha256
    )
    return hmac_result.hexdigest()


def jsonify(contents):
    return json.dumps(
        contents, sort_keys=False, separators=(",", ":"), ensure_ascii=False
    )


def send_hello_message(user_id, token):
    contents = "1"
    message = {
        "userId": str(user_id),
        "event": "hello",
        "contents": contents,
        "hmac": calculate_hmac(jsonify(contents), token),
    }
    client_socket.sendto(json.dumps(message).encode(), SERVER_ADDRESS)


def handle_hello(user_id, token):
    while True:
        send_hello_message(user_id, token)
        time.sleep(1)  # 1 Hz updates


def handle_receiving(update_state):
    while True:
        data, _ = client_socket.recvfrom(BUFFER_SIZE)
        parsed_data = json.loads(data.decode())
        try:
            game_state = GameState(**parsed_data)
            update_state(game_state)
        except ValidationError as e:
            print(f"Received faulty game state: {e}")


def initialize_client(user_id, token, update_state):
    hello_thread = threading.Thread(
        target=handle_hello, daemon=True, args=(user_id, token)
    )
    hello_thread.start()
    receive_thread = threading.Thread(
        target=handle_receiving, daemon=True, args=(update_state,)
    )
    receive_thread.start()


def issue_move(user_id, token, x, y):
    contents = {"latitude": y, "longitude": x}
    message = {
        "userId": str(user_id),
        "event": "move",
        "contents": contents,
        "hmac": calculate_hmac(jsonify(contents), token),
    }
    client_socket.sendto(json.dumps(message).encode(), SERVER_ADDRESS)


def change_status(user_id, token, status):
    contents = status
    message = {
        "userId": str(user_id),
        "event": "status",
        "contents": contents,
        "hmac": calculate_hmac(jsonify(contents), token),
    }
    client_socket.sendto(json.dumps(message).encode(), SERVER_ADDRESS)


def issue_mark(user_id, token, mark):
    contents = mark
    message = {
        "userId": str(user_id),
        "event": "mark",
        "contents": contents,
        "hmac": calculate_hmac(jsonify(contents), token),
    }
    client_socket.sendto(json.dumps(message).encode(), SERVER_ADDRESS)
