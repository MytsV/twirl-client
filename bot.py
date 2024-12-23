import argparse
import random
import threading
import time
import sys
import requests
import socket
import hmac
import hashlib
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

UDP_ADDRESS = os.getenv("UDP_ADDRESS")
UDP_PORT = int(os.getenv("UDP_PORT"))

SERVER_ADDRESS = (UDP_ADDRESS, UDP_PORT)
BUFFER_SIZE = 1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

LOGIN_URL = os.getenv("AUTH_URL") + "/login"


def calculate_hmac(contents, token):
    hmac_result = hmac.new(
        token.encode("utf-8"), contents.encode("utf-8"), hashlib.sha256
    )
    return hmac_result.hexdigest()


def jsonify(contents):
    return json.dumps(
        contents, sort_keys=False, separators=(",", ":"), ensure_ascii=False
    )


def login(username, password):
    if not username or not password:
        return None, "Username and password must be provided."

    payload = {"username": username, "password": password}

    try:
        response = requests.post(LOGIN_URL, json=payload)

        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 401:
            return None, "Invalid username or password."
        elif response.status_code == 400:
            return None, "Bad request: missing username or password."
        else:
            return None, "Unknown server error."

    except requests.exceptions.RequestException as e:
        return None, f"Error connecting to the server: {e}"


def send_hello_message(user_id, token, location_id):
    contents = location_id
    message = {
        "userId": str(user_id),
        "event": "hello",
        "contents": contents,
        "hmac": calculate_hmac(jsonify(contents), token),
    }
    client_socket.sendto(json.dumps(message).encode(), SERVER_ADDRESS)


def handle_hello(user_id, token, location_id):
    while True:
        send_hello_message(user_id, token, location_id)
        time.sleep(1)  # 1 Hz updates


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


def main():
    parser = argparse.ArgumentParser(description="Bot Client")
    parser.add_argument("location_id", type=str, help="Location ID")
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")

    args = parser.parse_args()

    location_id = args.location_id
    username = args.username
    password = args.password

    # Log in to get user_id and token
    login_response, error = login(username, password)
    if error:
        print(f"Login failed: {error}")
        sys.exit(1)

    user_id = login_response["userId"]
    token = login_response["token"]

    hello_thread = threading.Thread(
        target=handle_hello, daemon=True, args=(user_id, token, location_id)
    )
    hello_thread.start()

    # Wait for 1 second and move to a random location
    time.sleep(1)
    x = random.randint(0, 500)
    y = random.randint(0, 500)
    print(f"Moving to random location: ({x}, {y})")
    issue_move(user_id, token, x, y)

    # Wait for 1 more second and change status to dancing
    time.sleep(1)
    print("Changing status to 'dancing'")
    change_status(user_id, token, "dancing")

    while True:
        pass


if __name__ == "__main__":
    main()
